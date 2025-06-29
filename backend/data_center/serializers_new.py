"""
数据中心应用的序列化器
"""

from rest_framework import serializers
from .models import Dataset, KnowledgeBase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']

class DatasetSerializer(serializers.ModelSerializer):
    """数据集序列化器"""
    
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    file_size_formatted = serializers.ReadOnlyField()
    file_url = serializers.ReadOnlyField()
    created_by_detail = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'slug', 'description', 'file', 'file_format', 
            'file_size', 'file_size_formatted', 'file_url', 'rows_count', 
            'columns_count', 'status', 'status_message', 'is_public', 'tags',
            'created_by', 'created_by_username', 'created_by_detail',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'slug', 'file_size', 'file_format', 'created_by', 
            'file_size_formatted', 'file_url', 'rows_count', 
            'columns_count', 'status', 'status_message',
            'created_at', 'updated_at'
        ]
        
    def validate_name(self, value):
        """验证数据集名称"""
        if len(value) < 2:
            raise serializers.ValidationError("数据集名称必须至少包含2个字符")
        return value
        
    def validate_file(self, value):
        """验证文件类型和大小"""
        if value:
            # 验证文件大小 (100MB以内)
            if value.size > 100 * 1024 * 1024:
                raise serializers.ValidationError("文件大小不能超过100MB")
                
            # 验证文件扩展名
            valid_extensions = ['csv', 'json', 'txt', 'xlsx', 'xls', 'tsv']
            extension = value.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise serializers.ValidationError(f"不支持的文件格式，请上传以下格式: {', '.join(valid_extensions)}")
        
        return value

class KnowledgeBaseSerializer(serializers.ModelSerializer):
    """知识库序列化器"""
    
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    created_by_detail = UserSerializer(source='created_by', read_only=True)
    related_datasets_detail = DatasetSerializer(source='related_datasets', many=True, read_only=True)
    content_preview = serializers.ReadOnlyField()
    
    class Meta:
        model = KnowledgeBase
        fields = [
            'id', 'name', 'slug', 'description', 'content', 'content_preview',
            'type', 'is_public', 'tags', 'has_vector_index', 'vector_index_path',
            'related_datasets', 'related_datasets_detail',
            'created_by', 'created_by_username', 'created_by_detail',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'slug', 'created_by', 'has_vector_index', 'vector_index_path',
            'content_preview', 'created_at', 'updated_at'
        ]
        
    def validate_name(self, value):
        """验证知识库名称"""
        if len(value) < 2:
            raise serializers.ValidationError("知识库名称必须至少包含2个字符")
        return value
        
    def validate_content(self, value):
        """验证知识库内容"""
        if len(value) < 10:
            raise serializers.ValidationError("知识库内容过短，请至少输入10个字符")
        return value 