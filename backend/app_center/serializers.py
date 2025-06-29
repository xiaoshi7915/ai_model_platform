"""
应用中心应用的序列化器
"""

from rest_framework import serializers
from .models import Application, Plugin, ApplicationPlugin
from training_center.serializers import ModelSerializer

class PluginSerializer(serializers.ModelSerializer):
    """插件序列化器"""
    
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Plugin
        fields = [
            'id', 'name', 'description', 'version', 'file', 
            'compatibility', 'created_by', 'created_by_username', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class ApplicationPluginSerializer(serializers.ModelSerializer):
    """应用插件关联序列化器"""
    
    plugin_name = serializers.ReadOnlyField(source='plugin.name')
    plugin_version = serializers.ReadOnlyField(source='plugin.version')
    plugin_description = serializers.ReadOnlyField(source='plugin.description')
    
    class Meta:
        model = ApplicationPlugin
        fields = [
            'id', 'application', 'plugin', 'plugin_name', 
            'plugin_version', 'plugin_description', 'enabled', 
            'config', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ApplicationSerializer(serializers.ModelSerializer):
    """应用序列化器"""
    
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    model_name = serializers.ReadOnlyField(source='model.name')
    model_version = serializers.ReadOnlyField(source='model.version')
    plugins = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'name', 'description', 'model', 'model_name', 
            'model_version', 'status', 'api_endpoint', 'config', 
            'created_by', 'created_by_username', 
            'created_at', 'updated_at', 'deployed_at', 'plugins'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'deployed_at', 'api_endpoint']
    
    def get_plugins(self, obj):
        """获取应用关联的插件"""
        application_plugins = ApplicationPlugin.objects.filter(application=obj)
        return ApplicationPluginSerializer(application_plugins, many=True).data 