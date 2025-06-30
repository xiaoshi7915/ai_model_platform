"""
应用中心应用的视图
"""

from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Application, Plugin, ApplicationPlugin
from .serializers import ApplicationSerializer, PluginSerializer, ApplicationPluginSerializer
from .tasks import deploy_application, stop_application
from utils.uuid_helper import validate_and_convert_uuid
import random

class ApplicationViewSet(viewsets.ModelViewSet):
    """应用视图集"""
    
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'model']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def get_queryset(self):
        """获取查询集，显示所有应用"""
        if getattr(self, 'swagger_fake_view', False):  # 处理swagger文档生成
            return Application.objects.none()
        # 返回所有应用，不限制用户
        return Application.objects.all().order_by('-created_at')
    
    def get_object(self):
        """
        获取单个对象并处理UUID格式问题
        """
        # 获取pk
        pk = self.kwargs.get('pk')
        
        # 验证和转换UUID
        valid_uuid = validate_and_convert_uuid(pk)
        if valid_uuid:
            self.kwargs['pk'] = valid_uuid
        
        # 调用父类方法
        return super().get_object()
    
    def perform_create(self, serializer):
        """创建应用时设置创建者"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def deploy(self, request, pk=None):
        """部署应用"""
        application = self.get_object()
        
        # 检查应用状态
        if application.status == 'running':
            return Response(
                {'error': '应用已经在运行中'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查模型状态
        if application.model.status != 'completed':
            return Response(
                {'error': '只能部署使用已完成训练的模型的应用'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新应用状态
        application.status = 'running'
        application.deployed_at = timezone.now()
        application.save()
        
        # 启动异步部署任务
        deploy_application.delay(application.id)
        
        return Response(ApplicationSerializer(application).data)
    
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """停止应用"""
        application = self.get_object()
        
        # 检查应用状态
        if application.status != 'running':
            return Response(
                {'error': '只能停止运行中的应用'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新应用状态
        application.status = 'stopped'
        application.save()
        
        # 启动异步停止任务
        stop_application.delay(application.id)
        
        return Response(ApplicationSerializer(application).data)
    
    @action(detail=True, methods=['GET'])
    def monitoring(self, request, pk=None):
        """
        获取应用监控数据
        """
        try:
            application = self.get_object()
            
            # 检查应用是否正在运行
            if application.status != 'running':
                return Response({
                    'error': '应用未运行，无法获取监控数据'
                }, status=200)
            
            # 在实际环境中，这里会从监控系统获取数据
            # 这里返回模拟数据用于演示
            current_time = timezone.now()
            monitoring_data = {
                'cpu': {
                    'current': round(random.uniform(5, 60), 2),
                    'history': [round(random.uniform(5, 60), 2) for _ in range(20)],
                    'timestamps': [(current_time - timezone.timedelta(minutes=i)).isoformat() for i in range(20, 0, -1)]
                },
                'memory': {
                    'current': round(random.uniform(100, 500), 2),
                    'total': 1024,
                    'history': [round(random.uniform(100, 500), 2) for _ in range(20)],
                    'timestamps': [(current_time - timezone.timedelta(minutes=i)).isoformat() for i in range(20, 0, -1)]
                },
                'requests': {
                    'total': random.randint(1000, 5000),
                    'success_rate': round(random.uniform(90, 99.9), 2),
                    'history': [random.randint(10, 100) for _ in range(20)],
                    'timestamps': [(current_time - timezone.timedelta(minutes=i)).isoformat() for i in range(20, 0, -1)]
                },
                'response_time': {
                    'average': round(random.uniform(50, 200), 2),
                    'history': [round(random.uniform(50, 200), 2) for _ in range(20)],
                    'timestamps': [(current_time - timezone.timedelta(minutes=i)).isoformat() for i in range(20, 0, -1)]
                },
                'timestamp': current_time.isoformat(),
                'uptime': random.randint(1, 48)
            }
            
            return Response(monitoring_data)
        except Exception as e:
            return Response({
                'error': f'获取监控数据失败: {str(e)}'
            }, status=500)
    
    @action(detail=True, methods=['GET'])
    def logs(self, request, pk=None):
        """
        获取应用日志
        可选参数：
        - start_time: 开始时间
        - end_time: 结束时间
        - log_level: 日志级别 (info, warning, error)
        - limit: 返回的日志条数
        """
        try:
            application = self.get_object()
            
            # 获取查询参数
            start_time = request.query_params.get('start_time')
            end_time = request.query_params.get('end_time')
            log_level = request.query_params.get('log_level')
            limit = int(request.query_params.get('limit', 100))
            
            # 检查应用是否存在
            if not application:
                return Response({
                    'error': '应用不存在'
                }, status=404)
            
            # 在实际环境中，这里会从日志系统获取数据
            # 这里返回模拟数据用于演示
            current_time = timezone.now()
            
            # 生成模拟日志
            log_levels = ['info', 'warning', 'error']
            if log_level and log_level != 'all':
                log_levels = [log_level]
                
            logs = []
            for i in range(limit):
                random_level = random.choice(log_levels)
                log_time = current_time - timezone.timedelta(minutes=random.randint(0, 60))
                
                if start_time and log_time < timezone.datetime.fromisoformat(start_time.replace('Z', '+00:00')):
                    continue
                    
                if end_time and log_time > timezone.datetime.fromisoformat(end_time.replace('Z', '+00:00')):
                    continue
                
                log_messages = {
                    'info': [
                        f'应用 {application.name} 处理请求成功',
                        f'用户访问应用 {application.name}',
                        f'应用 {application.name} 资源使用正常',
                        f'应用 {application.name} 连接到数据库',
                        f'应用 {application.name} 缓存命中率: {random.randint(70, 99)}%'
                    ],
                    'warning': [
                        f'应用 {application.name} 响应时间较长: {random.randint(500, 2000)}ms',
                        f'应用 {application.name} 内存使用率高: {random.randint(70, 90)}%',
                        f'应用 {application.name} 请求队列积压',
                        f'应用 {application.name} 连接池接近上限',
                        f'应用 {application.name} CPU使用率高: {random.randint(70, 90)}%'
                    ],
                    'error': [
                        f'应用 {application.name} 请求处理失败: 超时',
                        f'应用 {application.name} 数据库连接失败',
                        f'应用 {application.name} 服务异常',
                        f'应用 {application.name} 内存溢出',
                        f'应用 {application.name} 依赖服务不可用'
                    ]
                }
                
                logs.append({
                    'timestamp': log_time.isoformat(),
                    'level': random_level,
                    'message': random.choice(log_messages[random_level]),
                    'service': application.name,
                    'instance': f'{application.name}-{random.randint(1, 3)}'
                })
            
            # 按时间排序
            logs.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return Response({
                'logs': logs,
                'total': len(logs)
            })
        except Exception as e:
            return Response({
                'error': f'获取日志失败: {str(e)}'
            }, status=500)
    
    @action(detail=True, methods=['post'])
    def add_plugin(self, request, pk=None):
        """为应用添加插件"""
        application = self.get_object()
        plugin_id = request.data.get('plugin_id')
        
        if not plugin_id:
            return Response(
                {'error': '必须指定插件ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            plugin = Plugin.objects.get(id=plugin_id)
        except Plugin.DoesNotExist:
            return Response(
                {'error': '指定的插件不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 检查插件是否已经添加到应用
        if ApplicationPlugin.objects.filter(application=application, plugin=plugin).exists():
            return Response(
                {'error': '该插件已经添加到应用中'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建应用插件关联
        application_plugin = ApplicationPlugin.objects.create(
            application=application,
            plugin=plugin,
            enabled=True,
            config=request.data.get('config', {})
        )
        
        return Response(
            ApplicationPluginSerializer(application_plugin).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def remove_plugin(self, request, pk=None):
        """从应用中移除插件"""
        application = self.get_object()
        plugin_id = request.data.get('plugin_id')
        
        if not plugin_id:
            return Response(
                {'error': '必须指定插件ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            application_plugin = ApplicationPlugin.objects.get(
                application=application,
                plugin_id=plugin_id
            )
        except ApplicationPlugin.DoesNotExist:
            return Response(
                {'error': '该应用未添加指定的插件'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 删除应用插件关联
        application_plugin.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class PluginViewSet(viewsets.ModelViewSet):
    """插件视图集"""
    
    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def get_queryset(self):
        """获取查询集，显示所有插件"""
        if getattr(self, 'swagger_fake_view', False):  # 处理swagger文档生成
            return Plugin.objects.none()
        # 返回所有插件，不限制用户
        return Plugin.objects.all().order_by('-created_at')
    
    def get_object(self):
        """
        获取单个对象并处理UUID格式问题
        """
        # 获取pk
        pk = self.kwargs.get('pk')
        
        # 验证和转换UUID
        valid_uuid = validate_and_convert_uuid(pk)
        if valid_uuid:
            self.kwargs['pk'] = valid_uuid
        
        # 调用父类方法
        return super().get_object()
    
    def perform_create(self, serializer):
        """创建插件时设置创建者"""
        serializer.save(created_by=self.request.user) 