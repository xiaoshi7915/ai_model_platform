"""
训练中心应用的序列化器
"""

from rest_framework import serializers
from .models import Model, DockerImage, TrainingJob
from data_center.serializers import DatasetSerializer

class ModelSerializer(serializers.ModelSerializer):
    """模型序列化器"""
    
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    dataset_name = serializers.ReadOnlyField(source='dataset.name')
    
    class Meta:
        model = Model
        fields = [
            'id', 'name', 'description', 'version', 'status', 
            'parameters', 'metrics', 'file', 'dataset', 'dataset_name',
            'created_by', 'created_by_username', 'created_at', 'updated_at',
            'training_started_at', 'training_completed_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'training_started_at', 'training_completed_at']

class DockerImageSerializer(serializers.ModelSerializer):
    """Docker镜像序列化器"""
    
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = DockerImage
        fields = [
            'id', 'name', 'tag', 'description', 'size', 'registry',
            'created_by', 'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class TrainingJobSerializer(serializers.ModelSerializer):
    """训练任务序列化器"""
    
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    model_name = serializers.ReadOnlyField(source='model.name')
    model_version = serializers.ReadOnlyField(source='model.version')
    docker_image_name = serializers.ReadOnlyField(source='docker_image.name')
    docker_image_tag = serializers.ReadOnlyField(source='docker_image.tag')
    
    class Meta:
        model = TrainingJob
        fields = [
            'id', 'model', 'model_name', 'model_version', 
            'docker_image', 'docker_image_name', 'docker_image_tag',
            'status', 'log', 'created_by', 'created_by_username',
            'created_at', 'started_at', 'completed_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'started_at', 'completed_at'] 