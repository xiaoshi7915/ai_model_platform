"""
应用中心应用的模型
"""

from django.db import models
from django.contrib.auth.models import User
from training_center.models import Model
import uuid

class Application(models.Model):
    """应用模型"""
    
    STATUS_CHOICES = (
        ('created', '已创建'),
        ('running', '运行中'),
        ('stopped', '已停止'),
        ('error', '错误'),
    )
    
    # 使用自增ID，与数据库保持一致
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="应用名称")
    description = models.TextField(blank=True, null=True, verbose_name="应用描述")
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="applications", verbose_name="模型")
    api_endpoint = models.CharField(max_length=255, blank=True, null=True, verbose_name="API端点")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="状态")
    config = models.JSONField(default=dict, blank=True, verbose_name="配置信息")
    plugins = models.ManyToManyField('Plugin', blank=True, related_name="applications", verbose_name="插件")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_applications", verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    deployed_at = models.DateTimeField(blank=True, null=True, verbose_name="部署时间")
    
    class Meta:
        verbose_name = "应用"
        verbose_name_plural = "应用"
        ordering = ['-created_at']
        unique_together = ['name', 'created_by']
    
    def __str__(self):
        return self.name

class Plugin(models.Model):
    """插件模型"""
    
    STATUS_CHOICES = (
        ('active', '激活'),
        ('inactive', '未激活'),
        ('deprecated', '已弃用'),
    )
    
    # 使用自增ID，与数据库保持一致
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="插件名称")
    version = models.CharField(max_length=20, verbose_name="版本号")
    description = models.TextField(blank=True, null=True, verbose_name="插件描述")
    entry_point = models.CharField(max_length=255, blank=True, null=True, verbose_name="入口点")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="状态")
    file = models.FileField(upload_to='plugins/', verbose_name="插件文件")
    compatibility = models.JSONField(default=dict, verbose_name="兼容性信息")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_plugins", verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "插件"
        verbose_name_plural = "插件"
        ordering = ['-created_at']
        unique_together = ['name', 'version', 'created_by']
    
    def __str__(self):
        return f"{self.name} - {self.version}"

class ApplicationPlugin(models.Model):
    """应用插件关联模型"""
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='application_plugins', verbose_name="应用")
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name='application_plugins', verbose_name="插件")
    enabled = models.BooleanField(default=True, verbose_name="是否启用")
    config = models.JSONField(default=dict, blank=True, null=True, verbose_name="插件配置")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "应用插件关联"
        verbose_name_plural = "应用插件关联"
        ordering = ['-created_at']
        unique_together = ['application', 'plugin']
    
    def __str__(self):
        return f"{self.application.name} - {self.plugin.name}"

class ApplicationLog(models.Model):
    """应用日志模型"""
    LEVEL_CHOICES = (
        ('debug', 'DEBUG'),
        ('info', 'INFO'),
        ('warning', 'WARNING'),
        ('error', 'ERROR'),
        ('critical', 'CRITICAL'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="logs", verbose_name="应用")
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='info', verbose_name="日志级别")
    message = models.TextField(verbose_name="日志信息")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="时间戳")
    
    class Meta:
        verbose_name = "应用日志"
        verbose_name_plural = "应用日志"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.application.name} - {self.timestamp} - {self.level}"

class ApplicationMetric(models.Model):
    """应用指标模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="metrics", verbose_name="应用")
    cpu_usage = models.FloatField(default=0.0, verbose_name="CPU使用率")
    memory_usage = models.FloatField(default=0.0, verbose_name="内存使用率")
    total_requests = models.IntegerField(default=0, verbose_name="总请求数")
    avg_response_time = models.FloatField(default=0.0, verbose_name="平均响应时间")
    error_rate = models.FloatField(default=0.0, verbose_name="错误率")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="时间戳")
    
    class Meta:
        verbose_name = "应用指标"
        verbose_name_plural = "应用指标"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.application.name} - {self.timestamp}" 