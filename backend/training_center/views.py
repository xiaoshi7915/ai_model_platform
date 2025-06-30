"""
训练中心应用的视图
"""

from rest_framework import viewsets, filters, status, pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import Model, DockerImage, TrainingJob
from .serializers import ModelSerializer, DockerImageSerializer, TrainingJobSerializer
from .tasks import start_training_job

class StandardResultsSetPagination(pagination.PageNumberPagination):
    """标准分页器"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """自定义分页响应格式"""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class ModelViewSet(viewsets.ModelViewSet):
    """模型视图集"""
    
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'version']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """获取查询集，显示所有模型"""
        if getattr(self, 'swagger_fake_view', False):  # 处理swagger文档生成
            return Model.objects.none()
        # 返回所有模型，不限制用户
        return Model.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        """创建模型时设置创建者"""
        serializer.save(created_by=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """重写列表方法，确保响应格式一致"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # 使用分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        # 返回统一格式的响应
        return Response({'results': serializer.data})
    
    def retrieve(self, request, *args, **kwargs):
        """重写详情方法，确保响应格式一致"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def train(self, request, pk=None):
        """开始训练模型"""
        model = self.get_object()
        
        # 检查模型状态
        if model.status == 'training':
            return Response(
                {'error': '模型已经在训练中'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取Docker镜像
        docker_image_id = request.data.get('docker_image_id')
        if not docker_image_id:
            return Response(
                {'error': '必须指定Docker镜像'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            docker_image = DockerImage.objects.get(id=docker_image_id)
        except DockerImage.DoesNotExist:
            return Response(
                {'error': '指定的Docker镜像不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 更新模型状态
        model.status = 'training'
        model.training_started_at = timezone.now()
        model.save()
        
        # 创建训练任务
        training_job = TrainingJob.objects.create(
            model=model,
            docker_image=docker_image,
            status='pending',
            created_by=request.user
        )
        
        # 启动异步训练任务
        start_training_job.delay(training_job.id)
        
        return Response(
            TrainingJobSerializer(training_job).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """获取模型的所有版本"""
        model = self.get_object()
        versions = Model.objects.filter(
            name=model.name,
            created_by=request.user
        ).values_list('version', flat=True)
        
        return Response({'results': list(versions)})

class DockerImageViewSet(viewsets.ModelViewSet):
    """Docker镜像视图集"""
    
    queryset = DockerImage.objects.all()
    serializer_class = DockerImageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'tag', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """获取查询集，显示所有Docker镜像"""
        if getattr(self, 'swagger_fake_view', False):  # 处理swagger文档生成
            return DockerImage.objects.none()
        # 返回所有Docker镜像，不限制用户
        return DockerImage.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        """创建Docker镜像时设置创建者"""
        serializer.save(created_by=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """重写列表方法，确保响应格式一致"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # 使用分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        # 返回统一格式的响应
        return Response({'results': serializer.data})

class TrainingJobViewSet(viewsets.ReadOnlyModelViewSet):
    """训练任务视图集（只读）"""
    
    queryset = TrainingJob.objects.all()
    serializer_class = TrainingJobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'model']
    ordering_fields = ['created_at', 'started_at', 'completed_at']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """获取查询集，只返回当前用户的训练任务"""
        if getattr(self, 'swagger_fake_view', False):
            return TrainingJob.objects.none()
        return TrainingJob.objects.filter(created_by=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """重写列表方法，确保响应格式一致"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # 使用分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        # 返回统一格式的响应
        return Response({'results': serializer.data})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消训练任务"""
        training_job = self.get_object()
        
        # 检查任务状态
        if training_job.status not in ['pending', 'running']:
            return Response(
                {'error': '只能取消等待中或运行中的任务'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新任务状态
        training_job.status = 'cancelled'
        training_job.completed_at = timezone.now()
        training_job.save()
        
        # 更新模型状态
        model = training_job.model
        model.status = 'draft'
        model.save()
        
        return Response(
            TrainingJobSerializer(training_job).data
        ) 