"""
评测中心应用的视图
"""

from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import EvaluationTask, EvaluationReport, ModelComparison
from .serializers import EvaluationTaskSerializer, EvaluationReportSerializer, ModelComparisonSerializer
from .tasks import run_evaluation_task, generate_model_comparison

class EvaluationTaskViewSet(viewsets.ModelViewSet):
    """评测任务视图集"""
    
    queryset = EvaluationTask.objects.all()
    serializer_class = EvaluationTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'model', 'dataset']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'started_at', 'completed_at']
    
    def get_queryset(self):
        """获取查询集，只返回当前用户的评测任务"""
        # 检查是否是 swagger 文档生成
        if getattr(self, 'swagger_fake_view', False):
            return EvaluationTask.objects.none()
        return EvaluationTask.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        """创建评测任务时设置创建者"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """开始评测任务"""
        task = self.get_object()
        
        # 检查任务状态
        if task.status != 'pending':
            return Response(
                {'error': '只能启动等待中的任务'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新任务状态
        task.status = 'running'
        task.started_at = timezone.now()
        task.save()
        
        # 启动异步评测任务
        run_evaluation_task.delay(task.id)
        
        return Response(EvaluationTaskSerializer(task).data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消评测任务"""
        task = self.get_object()
        
        # 检查任务状态
        if task.status not in ['pending', 'running']:
            return Response(
                {'error': '只能取消等待中或运行中的任务'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新任务状态
        task.status = 'cancelled'
        task.completed_at = timezone.now()
        task.save()
        
        return Response(EvaluationTaskSerializer(task).data)
    
    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """获取评测任务的报告"""
        task = self.get_object()
        
        try:
            report = task.report
        except EvaluationReport.DoesNotExist:
            return Response(
                {'error': '该任务还没有生成报告'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(EvaluationReportSerializer(report).data)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """获取评测任务的进度"""
        task = self.get_object()
        
        # 根据任务状态返回进度信息
        progress_data = {
            'status': task.status,
            'progress': 0,  # 默认进度为0
            'message': ''
        }
        
        # 根据任务状态设置进度
        if task.status == 'pending':
            progress_data['progress'] = 0
            progress_data['message'] = '任务等待中'
        elif task.status == 'running':
            # 这里应该从任务执行器获取实际进度
            # 为了演示，我们根据任务创建时间和当前时间计算一个模拟进度
            if task.started_at:
                time_elapsed = (timezone.now() - task.started_at).total_seconds()
                # 假设任务需要5分钟完成
                progress = min(time_elapsed / (5 * 60) * 100, 99)
                progress_data['progress'] = round(progress, 1)
                progress_data['message'] = f'任务执行中，进度 {progress_data["progress"]}%'
            else:
                progress_data['progress'] = 10
                progress_data['message'] = '任务初始化中'
        elif task.status == 'completed':
            progress_data['progress'] = 100
            progress_data['message'] = '任务已完成'
        elif task.status == 'failed':
            progress_data['progress'] = 0
            progress_data['message'] = '任务执行失败'
        elif task.status == 'cancelled':
            progress_data['progress'] = 0
            progress_data['message'] = '任务已取消'
        
        return Response(progress_data)

class EvaluationReportViewSet(viewsets.ReadOnlyModelViewSet):
    """评测报告视图集（只读）"""
    
    queryset = EvaluationReport.objects.all()
    serializer_class = EvaluationReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['task__name', 'summary', 'suggestions']
    ordering_fields = ['created_at', 'updated_at']
    
    def get_queryset(self):
        """获取查询集，只返回当前用户的评测报告"""
        # 检查是否是 swagger 文档生成
        if getattr(self, 'swagger_fake_view', False):
            return EvaluationReport.objects.none()
        return EvaluationReport.objects.filter(task__created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """下载评测报告"""
        report = self.get_object()
        
        # 这里应该实现报告下载逻辑
        # 为了简化，我们只返回一个成功消息
        return Response({'message': '报告下载功能将在后续版本中实现'})

class ModelComparisonViewSet(viewsets.ModelViewSet):
    """模型比较视图集"""
    
    queryset = ModelComparison.objects.all()
    serializer_class = ModelComparisonSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def get_queryset(self):
        """获取查询集，只返回当前用户的模型比较"""
        # 检查是否是 swagger 文档生成
        if getattr(self, 'swagger_fake_view', False):
            return ModelComparison.objects.none()
        return ModelComparison.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        """创建模型比较时设置创建者"""
        comparison = serializer.save(created_by=self.request.user)
        
        # 启动异步比较任务
        generate_model_comparison.delay(comparison.id)
        
        return comparison 