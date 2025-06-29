from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import APIProvider, APIConnection

@receiver(post_save, sender=APIProvider)
def api_provider_saved(sender, instance, created, **kwargs):
    """当API提供商保存时，清除相关缓存"""
    cache.delete(f'api_provider_{instance.id}')
    cache.delete('api_providers_list')
    cache.delete('active_api_providers_list')

@receiver(post_delete, sender=APIProvider)
def api_provider_deleted(sender, instance, **kwargs):
    """当API提供商删除时，清除相关缓存"""
    cache.delete(f'api_provider_{instance.id}')
    cache.delete('api_providers_list')
    cache.delete('active_api_providers_list')

@receiver(post_save, sender=APIConnection)
def api_connection_saved(sender, instance, created, **kwargs):
    """当API连接保存时，清除相关缓存"""
    cache.delete(f'api_connection_{instance.id}')
    cache.delete(f'api_connections_provider_{instance.provider.id}')
    cache.delete('api_connections_list')
    cache.delete('default_api_connections')

@receiver(post_delete, sender=APIConnection)
def api_connection_deleted(sender, instance, **kwargs):
    """当API连接删除时，清除相关缓存"""
    cache.delete(f'api_connection_{instance.id}')
    cache.delete(f'api_connections_provider_{instance.provider.id}')
    cache.delete('api_connections_list')
    cache.delete('default_api_connections')

@receiver(pre_save, sender=APIConnection)
def encrypt_api_keys(sender, instance, **kwargs):
    """API密钥保存前进行加密处理"""
    # 通常此处应添加密钥加密逻辑，但为简化示例，此处省略
    # 在实际应用中应使用Django的加密工具或第三方库进行加密
    pass 