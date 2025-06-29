from rest_framework import serializers
from .models import APIProvider, APIConnection, APIUsageLog, APIModel

class APIProviderSerializer(serializers.ModelSerializer):
    """API提供商序列化器"""
    
    provider_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = APIProvider
        fields = [
            'id', 'name', 'provider_type', 'provider_type_display', 'description',
            'icon', 'base_url', 'docs_url', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_provider_type_display(self, obj):
        """获取提供商类型显示名称"""
        return dict(APIProvider.PROVIDER_CHOICES).get(obj.provider_type, '')


class APIConnectionSerializer(serializers.ModelSerializer):
    """API连接序列化器"""
    
    provider_name = serializers.SerializerMethodField()
    provider_type = serializers.SerializerMethodField()
    
    class Meta:
        model = APIConnection
        fields = [
            'id', 'name', 'provider', 'provider_name', 'provider_type',
            'is_default', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_provider_name(self, obj):
        """获取提供商名称"""
        return obj.provider.name if obj.provider else ''
    
    def get_provider_type(self, obj):
        """获取提供商类型"""
        return obj.provider.provider_type if obj.provider else ''


class APIConnectionDetailSerializer(serializers.ModelSerializer):
    """API连接详细序列化器"""
    
    provider_name = serializers.SerializerMethodField()
    provider_type = serializers.SerializerMethodField()
    
    class Meta:
        model = APIConnection
        fields = [
            'id', 'name', 'provider', 'provider_name', 'provider_type',
            'api_key', 'api_secret', 'org_id', 'custom_headers', 'custom_params',
            'rate_limit', 'is_default', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'api_key': {'write_only': True},
            'api_secret': {'write_only': True},
        }
    
    def get_provider_name(self, obj):
        """获取提供商名称"""
        return obj.provider.name if obj.provider else ''
    
    def get_provider_type(self, obj):
        """获取提供商类型"""
        return obj.provider.provider_type if obj.provider else ''


class APIModelSerializer(serializers.ModelSerializer):
    """API模型序列化器"""
    
    provider_name = serializers.SerializerMethodField()
    provider_type = serializers.SerializerMethodField()
    model_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = APIModel
        fields = [
            'id', 'name', 'provider', 'provider_id', 'provider_name', 'provider_type',
            'model_type', 'model_type_display', 'model_identifier', 'description',
            'max_tokens', 'params_schema', 'is_default', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_provider_name(self, obj):
        """获取提供商名称"""
        return obj.provider.name if obj.provider else ''
    
    def get_provider_type(self, obj):
        """获取提供商类型"""
        return obj.provider.provider_type if obj.provider else ''
    
    def get_model_type_display(self, obj):
        """获取模型类型显示名称"""
        return dict(APIModel.MODEL_TYPE_CHOICES).get(obj.model_type, '')
    
    def get_provider_id(self, obj):
        """获取提供商ID"""
        return str(obj.provider.id) if obj.provider else None


class APIUsageLogSerializer(serializers.ModelSerializer):
    """API使用日志序列化器"""
    
    connection_name = serializers.SerializerMethodField()
    provider_name = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = APIUsageLog
        fields = [
            'id', 'connection', 'connection_name', 'provider_name',
            'endpoint', 'request_data', 'response_data', 'status', 'status_display',
            'error_message', 'tokens_used', 'response_time', 'user_ip', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_connection_name(self, obj):
        """获取连接名称"""
        return obj.connection.name if obj.connection else ''
    
    def get_provider_name(self, obj):
        """获取提供商名称"""
        return obj.connection.provider.name if obj.connection and obj.connection.provider else ''
    
    def get_status_display(self, obj):
        """获取状态显示名称"""
        return dict(APIUsageLog.STATUS_CHOICES).get(obj.status, '') 