from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db import models
from datetime import datetime, timedelta

from .models import APIProvider, APIConnection, APIUsageLog, APIModel
from .serializers import (
    APIProviderSerializer, APIConnectionSerializer,
    APIConnectionDetailSerializer, APIUsageLogSerializer,
    APIModelSerializer
)
from .utils import call_openai_api, call_baidu_api

class APIProviderViewSet(viewsets.ModelViewSet):
    """API提供商视图集"""
    queryset = APIProvider.objects.all()
    serializer_class = APIProviderSerializer
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(60 * 15))  # 缓存15分钟
    def list(self, request, *args, **kwargs):
        """获取API提供商列表"""
        queryset = self.filter_queryset(self.get_queryset())
        # 只返回活跃的提供商，除非请求中指定了all=true
        if not request.query_params.get('all', '').lower() == 'true':
            queryset = queryset.filter(is_active=True)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(60 * 15))  # 缓存15分钟
    def types(self, request):
        """获取所有API提供商类型"""
        types = [
            {'value': choice[0], 'label': choice[1]} 
            for choice in APIProvider.PROVIDER_CHOICES
        ]
        return Response(types)


class APIModelViewSet(viewsets.ModelViewSet):
    """API模型视图集"""
    queryset = APIModel.objects.all()
    serializer_class = APIModelSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        """获取API模型列表"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # 按提供商过滤
        provider_id = request.query_params.get('provider')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
            
        # 按模型类型过滤
        model_type = request.query_params.get('model_type')
        if model_type:
            queryset = queryset.filter(model_type=model_type)
            
        # 只返回活跃的模型，除非请求中指定了all=true
        if not request.query_params.get('all', '').lower() == 'true':
            queryset = queryset.filter(is_active=True)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(60 * 15))  # 缓存15分钟
    def types(self, request):
        """获取所有API模型类型"""
        types = [
            {'value': choice[0], 'label': choice[1]} 
            for choice in APIModel.MODEL_TYPE_CHOICES
        ]
        return Response(types)
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """设置为默认模型"""
        model = self.get_object()
        model.is_default = True
        model.save()
        
        return Response({'status': 'success', 'message': '已设置为默认模型'})


class APIConnectionViewSet(viewsets.ModelViewSet):
    """API连接视图集"""
    queryset = APIConnection.objects.all()
    serializer_class = APIConnectionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """根据请求类型选择序列化器"""
        if self.action == 'retrieve':
            return APIConnectionDetailSerializer
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        """获取API连接列表"""
        queryset = self.filter_queryset(self.get_queryset())
        # 按提供商过滤
        provider_id = request.query_params.get('provider')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
            
        # 只返回活跃的连接，除非请求中指定了all=true
        if not request.query_params.get('all', '').lower() == 'true':
            queryset = queryset.filter(is_active=True)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def defaults(self, request):
        """获取每种类型的默认API连接"""
        default_connections = {}
        for provider_type, _ in APIProvider.PROVIDER_CHOICES:
            conn = APIConnection.objects.filter(
                provider__provider_type=provider_type,
                is_active=True,
                is_default=True
            ).first()
            
            if conn:
                default_connections[provider_type] = APIConnectionSerializer(conn).data
                
        return Response(default_connections)
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """设置为默认连接"""
        connection = self.get_object()
        connection.is_default = True
        connection.save()
        
        # 清除缓存
        cache.delete('default_api_connections')
        
        return Response({'status': 'success', 'message': '已设置为默认连接'})
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """测试API连接"""
        connection = self.get_object()
        provider_type = connection.provider.provider_type
        
        try:
            if provider_type == 'openai':
                result = call_openai_api(
                    prompt="Hello, I'm testing the API connection. Please respond with 'Connection successful'.",
                    connection_id=connection.id,
                    user_ip=self.get_client_ip(request)
                )
            elif provider_type == 'baidu':
                result = call_baidu_api(
                    prompt="你好，我正在测试API连接。请回复'连接成功'。",
                    connection_id=connection.id,
                    user_ip=self.get_client_ip(request)
                )
            else:
                return Response(
                    {'status': 'error', 'message': f'暂不支持测试 {provider_type} 类型的连接'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if result.get('success', False):
                return Response({
                    'status': 'success',
                    'message': '连接测试成功',
                    'data': result
                })
            else:
                return Response({
                    'status': 'error',
                    'message': f'连接测试失败: {result.get("error", "未知错误")}',
                    'data': result
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response(
                {'status': 'error', 'message': f'连接测试发生错误: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class APIUsageLogViewSet(viewsets.ReadOnlyModelViewSet):
    """API使用日志视图集，只读"""
    queryset = APIUsageLog.objects.all()
    serializer_class = APIUsageLogSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        """获取API使用日志列表"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # 按连接过滤
        connection_id = request.query_params.get('connection')
        if connection_id:
            queryset = queryset.filter(connection_id=connection_id)
            
        # 按状态过滤
        status = request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        # 按日期范围过滤
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
            
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取使用统计信息"""
        # 使用缓存减轻数据库压力
        stats = cache.get('api_usage_statistics')
        if not stats:
            # 按状态统计
            status_stats = {}
            for status_choice, _ in APIUsageLog.STATUS_CHOICES:
                status_stats[status_choice] = APIUsageLog.objects.filter(status=status_choice).count()
            
            # 获取日期范围
            period = request.query_params.get('period', 'week')
            
            if period == 'today':
                start_date = datetime.now().date()
            elif period == 'week':
                start_date = (datetime.now() - timedelta(days=7)).date()
            elif period == 'month':
                start_date = (datetime.now() - timedelta(days=30)).date()
            elif period == 'custom':
                start_date_str = request.query_params.get('start_date')
                end_date_str = request.query_params.get('end_date')
                try:
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    return Response(
                        {'error': '无效的日期格式，请使用YYYY-MM-DD格式'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                start_date = (datetime.now() - timedelta(days=7)).date()
            
            end_date = request.query_params.get('end_date')
            if not end_date and period != 'custom':
                end_date = datetime.now().date()
            elif period == 'custom':
                # 已在上面处理
                pass
            else:
                try:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    end_date = datetime.now().date()
                    
            # 按日期统计每日请求数和Token消耗
            daily_stats = []
            current_date = start_date
            while current_date <= end_date:
                next_date = current_date + timedelta(days=1)
                daily_requests = APIUsageLog.objects.filter(
                    created_at__date=current_date
                ).count()
                
                daily_tokens = APIUsageLog.objects.filter(
                    created_at__date=current_date
                ).aggregate(total=models.Sum('tokens_used'))['total'] or 0
                
                daily_stats.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'requests': daily_requests,
                    'tokens': daily_tokens
                })
                
                current_date = next_date
            
            # 按提供商统计
            provider_stats = []
            for provider in APIProvider.objects.all():
                connections = APIConnection.objects.filter(provider=provider)
                connection_ids = [conn.id for conn in connections]
                
                if connection_ids:
                    provider_logs = APIUsageLog.objects.filter(connection__id__in=connection_ids)
                    total_requests = provider_logs.count()
                    
                    if total_requests > 0:
                        success_requests = provider_logs.filter(status='success').count()
                        success_rate = success_requests / total_requests if total_requests > 0 else 0
                        
                        tokens = provider_logs.aggregate(total=models.Sum('tokens_used'))['total'] or 0
                        avg_response_time = provider_logs.aggregate(avg=models.Avg('response_time'))['avg'] or 0
                        
                        provider_stats.append({
                            'provider': provider.name,
                            'requests': total_requests,
                            'success_rate': success_rate,
                            'tokens': tokens,
                            'avg_response_time': avg_response_time
                        })
            
            # 计算总计数据
            total_requests = APIUsageLog.objects.count()
            success_requests = APIUsageLog.objects.filter(status='success').count()
            failed_requests = total_requests - success_requests
            total_tokens = APIUsageLog.objects.aggregate(total=models.Sum('tokens_used'))['total'] or 0
            
            stats = {
                'total_requests': total_requests,
                'success_requests': success_requests,
                'failed_requests': failed_requests,
                'total_tokens': total_tokens,
                'status_stats': status_stats,
                'daily_stats': daily_stats,
                'provider_stats': provider_stats
            }
            
            # 将结果缓存15分钟
            cache.set('api_usage_statistics', stats, 60 * 15)
        
        return Response(stats)
