"""
数据中心应用的视图
"""

from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Dataset, KnowledgeBase
from .serializers import DatasetSerializer, KnowledgeBaseSerializer
import logging

logger = logging.getLogger(__name__)

class DatasetViewSet(viewsets.ModelViewSet):
    """数据集视图集"""
    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['file_format']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def get_queryset(self):
        """获取查询集，只返回当前用户的数据集"""
        if getattr(self, 'swagger_fake_view', False):  # 处理swagger文档生成
            return Dataset.objects.none()
        return Dataset.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        """创建数据集时设置创建者"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def formats(self, request):
        """获取所有可用的文件格式"""
        formats = Dataset.objects.values_list('file_format', flat=True).distinct()
        return Response(list(formats))

    def create(self, request, *args, **kwargs):
        """创建数据集"""
        try:
            logger.info(f"用户 {request.user.username} 开始创建数据集")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info("数据集创建成功")
            return Response({
                'message': '创建成功',
                'code': 200,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"创建数据集失败: {str(e)}")
            return Response({
                'message': '创建失败',
                'code': 500,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, *args, **kwargs):
        """更新数据集"""
        try:
            instance = self.get_object()
            logger.info(f"用户 {request.user.username} 开始更新数据集 {instance.id}")
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info(f"数据集 {instance.id} 更新成功")
            return Response({
                'message': '更新成功',
                'code': 200,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"更新数据集失败: {str(e)}")
            return Response({
                'message': '更新失败',
                'code': 500,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        """删除数据集"""
        try:
            instance = self.get_object()
            logger.info(f"用户 {request.user.username} 开始删除数据集 {instance.id}")
            self.perform_destroy(instance)
            logger.info(f"数据集 {instance.id} 删除成功")
            return Response({
                'message': '删除成功',
                'code': 200
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"删除数据集失败: {str(e)}")
            return Response({
                'message': '删除失败',
                'code': 500,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KnowledgeBaseViewSet(viewsets.ModelViewSet):
    """知识库视图集"""
    
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'content']
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def get_queryset(self):
        """获取查询集，只返回当前用户的知识库"""
        if getattr(self, 'swagger_fake_view', False):  # 处理swagger文档生成
            return KnowledgeBase.objects.none()
        return KnowledgeBase.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        """创建知识库时设置创建者"""
        serializer.save(created_by=self.request.user) 
    
    def create(self, request, *args, **kwargs):
        """创建知识库"""
        try:
            logger.info(f"用户 {request.user.username} 开始创建知识库")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info("知识库创建成功")
            return Response({
                'message': '创建成功',
                'code': 200,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"创建知识库失败: {str(e)}")
            return Response({
                'message': '创建失败',
                'code': 500,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        """删除知识库"""
        try:
            instance = self.get_object()
            logger.info(f"用户 {request.user.username} 开始删除知识库 {instance.id}")
            self.perform_destroy(instance)
            logger.info(f"知识库 {instance.id} 删除成功")
            return Response({
                'message': '删除成功',
                'code': 200
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"删除知识库失败: {str(e)}")
            return Response({
                'message': '删除失败',
                'code': 500,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)