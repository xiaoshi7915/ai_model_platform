from django.db import models
import uuid

class APIProvider(models.Model):
    """API提供商模型，用于存储支持的API服务提供商信息"""
    
    PROVIDER_CHOICES = [
        ('openai', 'OpenAI'),
        ('google', 'Google AI'),
        ('baidu', '百度智能云'),
        ('azure', 'Azure OpenAI'),
        ('anthropic', 'Anthropic'),
        ('huggingface', 'HuggingFace'),
        ('custom', '自定义API')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='提供商名称')
    provider_type = models.CharField(max_length=50, choices=PROVIDER_CHOICES, verbose_name='提供商类型')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    icon = models.ImageField(upload_to='api_providers/icons/', blank=True, null=True, verbose_name='图标')
    base_url = models.URLField(verbose_name='基础URL', help_text='API的基础URL，如：https://api.openai.com/v1/')
    docs_url = models.URLField(blank=True, null=True, verbose_name='文档URL')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = 'API提供商'
        verbose_name_plural = verbose_name
        ordering = ['name']
    
    def __str__(self):
        return self.name


class APIConnection(models.Model):
    """API连接配置模型，用于存储用户的API连接信息"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='连接名称')
    provider = models.ForeignKey(APIProvider, on_delete=models.CASCADE, related_name='connections', verbose_name='API提供商')
    api_key = models.CharField(max_length=255, verbose_name='API密钥')
    api_secret = models.CharField(max_length=255, blank=True, null=True, verbose_name='API密钥')
    org_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='组织ID')
    custom_headers = models.JSONField(blank=True, null=True, verbose_name='自定义请求头')
    custom_params = models.JSONField(blank=True, null=True, verbose_name='自定义参数')
    rate_limit = models.IntegerField(default=0, verbose_name='速率限制(每分钟)', help_text='0表示无限制')
    is_default = models.BooleanField(default=False, verbose_name='是否默认连接')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = 'API连接'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        unique_together = [('name', 'provider')]
    
    def __str__(self):
        return f"{self.name} ({self.provider.name})"
    
    def save(self, *args, **kwargs):
        # 如果设置为默认连接，取消同一提供商的其他默认连接
        if self.is_default:
            APIConnection.objects.filter(
                provider=self.provider, 
                is_default=True
            ).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)


class APIModel(models.Model):
    """API模型，用于存储各提供商支持的模型信息"""
    
    MODEL_TYPE_CHOICES = [
        ('text', '文本模型'),
        ('chat', '对话模型'),
        ('embedding', '嵌入模型'),
        ('image', '图像模型'),
        ('audio', '音频模型'),
        ('multimodal', '多模态模型'),
        ('other', '其他模型')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='模型名称')
    provider = models.ForeignKey(APIProvider, on_delete=models.CASCADE, related_name='models', verbose_name='API提供商')
    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES, verbose_name='模型类型')
    model_identifier = models.CharField(max_length=255, verbose_name='模型标识符', help_text='API中使用的实际模型标识符，如：gpt-4-turbo')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    max_tokens = models.IntegerField(default=4000, verbose_name='最大令牌数', help_text='模型支持的最大令牌数（上下文窗口大小）')
    params_schema = models.JSONField(default=dict, blank=True, verbose_name='参数配置', help_text='JSON格式的模型参数配置')
    is_default = models.BooleanField(default=False, verbose_name='是否默认模型')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = 'API模型'
        verbose_name_plural = verbose_name
        ordering = ['provider', 'name']
        unique_together = [('provider', 'model_identifier')]
    
    def __str__(self):
        return f"{self.name} ({self.provider.name})"
    
    def save(self, *args, **kwargs):
        # 如果设置为默认模型，取消同一提供商的其他默认模型
        if self.is_default:
            APIModel.objects.filter(
                provider=self.provider,
                model_type=self.model_type,
                is_default=True
            ).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)


class APIUsageLog(models.Model):
    """API使用日志模型，记录API调用情况"""
    
    STATUS_CHOICES = [
        ('success', '成功'),
        ('failed', '失败'),
        ('rate_limited', '超出速率限制'),
        ('error', '错误')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connection = models.ForeignKey(APIConnection, on_delete=models.CASCADE, related_name='usage_logs', verbose_name='API连接')
    endpoint = models.CharField(max_length=255, verbose_name='调用端点')
    request_data = models.JSONField(blank=True, null=True, verbose_name='请求数据')
    response_data = models.JSONField(blank=True, null=True, verbose_name='响应数据')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='状态')
    error_message = models.TextField(blank=True, null=True, verbose_name='错误信息')
    tokens_used = models.IntegerField(default=0, verbose_name='使用的令牌数')
    response_time = models.FloatField(verbose_name='响应时间(ms)')
    user_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='用户IP')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = 'API使用日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.connection.name} - {self.endpoint} - {self.status}"
