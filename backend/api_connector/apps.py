from django.apps import AppConfig


class ApiConnectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_connector'
    verbose_name = 'API连接服务'
    
    def ready(self):
        # 导入信号处理器
        import api_connector.signals
