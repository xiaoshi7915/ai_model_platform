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
import time

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
        """获取查询集，显示所有数据集"""
        if getattr(self, 'swagger_fake_view', False):  # 处理swagger文档生成
            return Dataset.objects.none()
        # 返回所有数据集，不限制用户
        return Dataset.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        """创建数据集时设置创建者"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def formats(self, request):
        """获取所有可用的文件格式"""
        formats = Dataset.objects.values_list('file_format', flat=True).distinct()
        return Response(list(formats))
    
    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """获取数据集预览"""
        try:
            dataset = self.get_object()
            # 这里应该实现真实的数据预览逻辑
            # 目前返回模拟数据
            preview_data = {
                'data': [
                    {'id': 1, 'text': '示例文本数据1', 'label': '类别A', 'score': 0.95},
                    {'id': 2, 'text': '示例文本数据2', 'label': '类别B', 'score': 0.87},
                    {'id': 3, 'text': '示例文本数据3', 'label': '类别A', 'score': 0.92},
                    {'id': 4, 'text': '示例文本数据4', 'label': '类别C', 'score': 0.78},
                    {'id': 5, 'text': '示例文本数据5', 'label': '类别B', 'score': 0.89}
                ],
                'total': 1000,
                'page': 1,
                'page_size': 10,
                'columns': ['id', 'text', 'label', 'score']
            }
            return Response(preview_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"获取数据集预览失败: {str(e)}")
            return Response({
                'error': '获取预览失败',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def usage(self, request, pk=None):
        """获取数据集使用情况"""
        try:
            dataset = self.get_object()
            # 这里应该实现真实的使用情况查询逻辑
            # 目前返回模拟数据
            usage_data = {
                'training_jobs': [
                    {
                        'id': 1,
                        'name': f'基于{dataset.name}的文本分类训练',
                        'status': 'completed',
                        'created_at': '2024-01-15T10:30:00Z',
                        'model_name': 'text-classifier-v1'
                    },
                    {
                        'id': 2,
                        'name': f'使用{dataset.name}的情感分析训练',
                        'status': 'running',
                        'created_at': '2024-01-20T14:15:00Z',
                        'model_name': 'sentiment-analyzer-v2'
                    }
                ],
                'applications': [
                    {
                        'id': 1,
                        'name': f'基于{dataset.name}的智能客服',
                        'status': 'running',
                        'created_at': '2024-01-10T09:00:00Z',
                        'app_type': 'chatbot'
                    }
                ],
                'evaluations': [
                    {
                        'id': 1,
                        'name': f'{dataset.name}模型性能评测',
                        'status': 'completed',
                        'created_at': '2024-01-18T16:45:00Z',
                        'test_type': 'accuracy'
                    }
                ]
            }
            return Response(usage_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"获取数据集使用情况失败: {str(e)}")
            return Response({
                'error': '获取使用情况失败',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        """获取查询集，显示所有知识库"""
        if getattr(self, 'swagger_fake_view', False):  # 处理swagger文档生成
            return KnowledgeBase.objects.none()
        # 返回所有知识库，不限制用户
        return KnowledgeBase.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        """创建知识库时设置创建者"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def usage(self, request, pk=None):
        """获取知识库使用情况"""
        try:
            knowledge_base = self.get_object()
            # 这里应该实现真实的使用情况查询逻辑
            # 目前返回模拟数据
            usage_data = {
                'training_jobs': [
                    {
                        'id': 1,
                        'name': f'基于{knowledge_base.name}的知识增强训练',
                        'status': 'completed',
                        'created_at': '2024-01-15T10:30:00Z',
                        'model_name': 'knowledge-enhanced-gpt'
                    },
                    {
                        'id': 2,
                        'name': f'使用{knowledge_base.name}的RAG模型训练',
                        'status': 'running',
                        'created_at': '2024-01-20T14:15:00Z',
                        'model_name': 'rag-model-v1'
                    }
                ],
                'applications': [
                    {
                        'id': 1,
                        'name': f'基于{knowledge_base.name}的智能问答',
                        'status': 'running',
                        'created_at': '2024-01-10T09:00:00Z',
                        'app_type': 'qa_system'
                    },
                    {
                        'id': 2,
                        'name': f'{knowledge_base.name}文档检索助手',
                        'status': 'deployed',
                        'created_at': '2024-01-12T11:20:00Z',
                        'app_type': 'search_assistant'
                    }
                ],
                'evaluations': [
                    {
                        'id': 1,
                        'name': f'{knowledge_base.name}检索准确性评测',
                        'status': 'completed',
                        'created_at': '2024-01-18T16:45:00Z',
                        'test_type': 'retrieval_accuracy'
                    },
                    {
                        'id': 2,
                        'name': f'{knowledge_base.name}响应质量评测',
                        'status': 'running',
                        'created_at': '2024-01-22T10:30:00Z',
                        'test_type': 'response_quality'
                    }
                ]
            }
            return Response(usage_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"获取知识库使用情况失败: {str(e)}")
            return Response({
                'error': '获取使用情况失败',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def vector_index(self, request, pk=None):
        """为知识库创建向量索引"""
        try:
            knowledge_base = self.get_object()
            # 这里应该实现真实的向量索引创建逻辑
            # 目前返回模拟响应
            result = {
                'message': f'已为知识库 "{knowledge_base.name}" 成功创建向量索引',
                'index_id': f'idx_{knowledge_base.id}_{int(time.time())}',
                'status': 'created',
                'dimension': 768,
                'total_vectors': len(knowledge_base.content.split('\n')) if knowledge_base.content else 0
            }
            logger.info(f"为知识库 {knowledge_base.id} 创建向量索引成功")
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"创建向量索引失败: {str(e)}")
            return Response({
                'error': '创建向量索引失败',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
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