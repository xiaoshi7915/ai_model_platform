"""
评测中心应用的序列化器
"""

from rest_framework import serializers
from .models import EvaluationTask, EvaluationReport, ModelComparison
from training_center.serializers import ModelSerializer
from data_center.serializers import DatasetSerializer

class EvaluationTaskSerializer(serializers.ModelSerializer):
    """评测任务序列化器"""
    
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    model_name = serializers.ReadOnlyField(source='model.name')
    model_version = serializers.ReadOnlyField(source='model.version')
    dataset_name = serializers.ReadOnlyField(source='dataset.name')
    
    class Meta:
        model = EvaluationTask
        fields = [
            'id', 'name', 'description', 'model', 'model_name', 
            'model_version', 'dataset', 'dataset_name', 'status', 
            'metrics', 'parameters', 'created_by', 'created_by_username', 
            'created_at', 'started_at', 'completed_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'started_at', 'completed_at', 'metrics']

class EvaluationReportSerializer(serializers.ModelSerializer):
    """评测报告序列化器"""
    
    task_name = serializers.ReadOnlyField(source='task.name')
    model_name = serializers.ReadOnlyField(source='task.model.name')
    model_version = serializers.ReadOnlyField(source='task.model.version')
    dataset_name = serializers.ReadOnlyField(source='task.dataset.name')
    
    class Meta:
        model = EvaluationReport
        fields = [
            'id', 'task', 'task_name', 'model_name', 'model_version', 
            'dataset_name', 'summary', 'details', 'charts', 
            'suggestions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ModelComparisonSerializer(serializers.ModelSerializer):
    """模型比较序列化器"""
    
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    dataset_name = serializers.ReadOnlyField(source='dataset.name')
    models_info = serializers.SerializerMethodField()
    
    class Meta:
        model = ModelComparison
        fields = [
            'id', 'name', 'description', 'model_list', 'dataset', 
            'dataset_name', 'results', 'created_by', 'created_by_username',
            'models_info', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def get_models_info(self, obj):
        """获取模型的基本信息"""
        return [
            {
                'id': model.id,
                'name': model.name,
                'version': model.version
            }
            for model in obj.model_list.all()
        ] 