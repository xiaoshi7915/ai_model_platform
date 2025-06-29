"""
数据中心应用的视图
"""

from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Dataset, KnowledgeBase
from .serializers import DatasetSerializer, KnowledgeBaseSerializer, UserSerializer
import logging
import pandas as pd
import json
import os
from django.conf import settings
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

logger = logging.getLogger(__name__)

class DatasetViewSet(viewsets.ModelViewSet):
    """数据集视图集"""
    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['file_format', 'status', 'is_public']
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['name', 'created_at', 'updated_at', 'file_size']
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        """获取查询集，返回当前用户的和公开的数据集"""
        if getattr(self, 'swagger_fake_view', False):  # 处理swagger文档生成
            return Dataset.objects.none()
            
        # 获取查询参数
        only_mine = self.request.query_params.get('only_mine', False)
        if only_mine and only_mine.lower() == 'true':
            # 只返回当前用户的数据集
            return Dataset.objects.filter(created_by=self.request.user)
        
        # 返回当前用户的和公开的数据集
        return Dataset.objects.filter(
            Q(created_by=self.request.user) | Q(is_public=True)
        ).distinct()
    
    def perform_create(self, serializer):
        """创建数据集时设置创建者"""
        dataset = serializer.save(created_by=self.request.user)
        
        # 异步处理数据集
        self.process_dataset(dataset)
        
    def process_dataset(self, dataset):
        """处理数据集，提取基本信息"""
        try:
            # 更新状态为处理中
            dataset.status = 'processing'
            dataset.save()
            
            file_path = os.path.join(settings.MEDIA_ROOT, dataset.file.name)
            file_ext = dataset.file_format.lower()
            
            # 根据文件类型读取数据
            if file_ext == 'csv':
                df = pd.read_csv(file_path)
            elif file_ext == 'xlsx' or file_ext == 'xls':
                df = pd.read_excel(file_path)
            elif file_ext == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                else:
                    df = pd.DataFrame([data])
            elif file_ext == 'txt' or file_ext == 'tsv':
                df = pd.read_csv(file_path, sep='\t')
            else:
                # 不支持的格式
                dataset.status = 'error'
                dataset.status_message = f"不支持的文件格式: {file_ext}"
                dataset.save()
                return
            
            # 更新数据集信息
            dataset.rows_count = len(df)
            dataset.columns_count = len(df.columns)
            dataset.status = 'ready'
            dataset.save()
            
            logger.info(f"数据集 {dataset.id} 处理完成，行数: {dataset.rows_count}, 列数: {dataset.columns_count}")
            
        except Exception as e:
            logger.error(f"处理数据集 {dataset.id} 失败: {str(e)}")
            dataset.status = 'error'
            dataset.status_message = f"处理失败: {str(e)}"
            dataset.save()
    
    @action(detail=False, methods=['get'])
    def formats(self, request):
        """获取所有可用的文件格式"""
        formats = Dataset.objects.values_list('file_format', flat=True).distinct()
        return Response(list(formats))
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """获取数据集统计信息"""
        total_count = Dataset.objects.filter(created_by=request.user).count()
        public_count = Dataset.objects.filter(created_by=request.user, is_public=True).count()
        formats = Dataset.objects.filter(created_by=request.user).values_list('file_format', flat=True)
        format_counts = {}
        for fmt in formats:
            format_counts[fmt] = format_counts.get(fmt, 0) + 1
            
        return Response({
            'total_count': total_count,
            'public_count': public_count,
            'format_counts': format_counts
        })
    
    @action(detail=True, methods=['post'])
    def toggle_public(self, request, pk=None):
        """切换数据集的公开状态"""
        dataset = self.get_object()
        dataset.is_public = not dataset.is_public
        dataset.save()
        serializer = self.get_serializer(dataset)
        return Response(serializer.data)

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_public']
    search_fields = ['name', 'description', 'content', 'tags']
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def get_queryset(self):
        """获取查询集，返回当前用户的和公开的知识库"""
        if getattr(self, 'swagger_fake_view', False):  # 处理swagger文档生成
            return KnowledgeBase.objects.none()
            
        # 获取查询参数
        only_mine = self.request.query_params.get('only_mine', False)
        if only_mine and only_mine.lower() == 'true':
            # 只返回当前用户的知识库
            return KnowledgeBase.objects.filter(created_by=self.request.user)
        
        # 返回当前用户的和公开的知识库
        return KnowledgeBase.objects.filter(
            Q(created_by=self.request.user) | Q(is_public=True)
        ).distinct()
    
    def perform_create(self, serializer):
        """创建知识库时设置创建者"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """获取知识库统计信息"""
        total_count = KnowledgeBase.objects.filter(created_by=request.user).count()
        public_count = KnowledgeBase.objects.filter(created_by=request.user, is_public=True).count()
        type_counts = {}
        types = KnowledgeBase.objects.filter(created_by=request.user).values_list('type', flat=True)
        for t in types:
            type_counts[t] = type_counts.get(t, 0) + 1
            
        return Response({
            'total_count': total_count,
            'public_count': public_count,
            'type_counts': type_counts
        })
    
    @action(detail=True, methods=['post'])
    def toggle_public(self, request, pk=None):
        """切换知识库的公开状态"""
        kb = self.get_object()
        kb.is_public = not kb.is_public
        kb.save()
        serializer = self.get_serializer(kb)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def create_vector_index(self, request, pk=None):
        """为知识库创建向量索引"""
        kb = self.get_object()
        
        # 这里应该有实际的向量索引创建逻辑，例如使用langchain
        # 为简化示例，这里只是更新状态
        kb.has_vector_index = True
        kb.vector_index_path = f"vector_indices/{kb.id}/"
        kb.save()
        
        serializer = self.get_serializer(kb)
        return Response(serializer.data)
    
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
    
    def update(self, request, *args, **kwargs):
        """更新知识库"""
        try:
            instance = self.get_object()
            logger.info(f"用户 {request.user.username} 开始更新知识库 {instance.id}")
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info(f"知识库 {instance.id} 更新成功")
            return Response({
                'message': '更新成功',
                'code': 200,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"更新知识库失败: {str(e)}")
            return Response({
                'message': '更新失败',
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