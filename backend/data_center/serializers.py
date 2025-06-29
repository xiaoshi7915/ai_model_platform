"""
数据中心应用的序列化器
"""

from rest_framework import serializers
from .models import Dataset, KnowledgeBase

class DatasetSerializer(serializers.ModelSerializer):
    """数据集序列化器"""
    
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'description', 'file', 'file_format', 
            'file_size', 'created_by', 'created_by_username', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['file_size', 'file_format', 'created_by', 'created_at', 'updated_at']

class KnowledgeBaseSerializer(serializers.ModelSerializer):
    """知识库序列化器"""
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = KnowledgeBase
        fields = ['id', 'name', 'description', 'content', 'is_public', 
                 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at'] 