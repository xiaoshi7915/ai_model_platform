"""
训练中心应用的模型
"""

from django.db import models
from django.contrib.auth.models import User
from data_center.models import Dataset

class Model(models.Model):
    """模型模型"""
    
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('training', '训练中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    )
    
    name = models.CharField(max_length=100, verbose_name="模型名称")
    description = models.TextField(blank=True, null=True, verbose_name="模型描述")
    version = models.CharField(max_length=20, verbose_name="模型版本")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="状态")
    parameters = models.JSONField(default=dict, verbose_name="训练参数")
    metrics = models.JSONField(default=dict, blank=True, null=True, verbose_name="性能指标")
    file = models.FileField(upload_to='models/', blank=True, null=True, verbose_name="模型文件")
    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True, related_name='models', verbose_name="训练数据集")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='models', verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    training_started_at = models.DateTimeField(blank=True, null=True, verbose_name="训练开始时间")
    training_completed_at = models.DateTimeField(blank=True, null=True, verbose_name="训练完成时间")
    
    class Meta:
        verbose_name = "模型"
        verbose_name_plural = "模型"
        ordering = ['-created_at']
        unique_together = ['name', 'version', 'created_by']
    
    def __str__(self):
        return f"{self.name} v{self.version}"

class DockerImage(models.Model):
    """Docker镜像模型"""
    
    name = models.CharField(max_length=100, verbose_name="镜像名称")
    tag = models.CharField(max_length=50, verbose_name="镜像标签")
    description = models.TextField(blank=True, null=True, verbose_name="镜像描述")
    size = models.PositiveIntegerField(verbose_name="镜像大小(MB)")
    registry = models.CharField(max_length=200, default='docker.io', verbose_name="镜像仓库")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='docker_images', verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "Docker镜像"
        verbose_name_plural = "Docker镜像"
        ordering = ['-created_at']
        unique_together = ['registry', 'name', 'tag']
    
    def __str__(self):
        return f"{self.registry}/{self.name}:{self.tag}"

class TrainingJob(models.Model):
    """训练任务模型"""
    
    STATUS_CHOICES = (
        ('pending', '等待中'),
        ('running', '运行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
        ('cancelled', '已取消'),
    )
    
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='training_jobs', verbose_name="模型")
    docker_image = models.ForeignKey(DockerImage, on_delete=models.SET_NULL, null=True, related_name='training_jobs', verbose_name="Docker镜像")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    log = models.TextField(blank=True, null=True, verbose_name="训练日志")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_jobs', verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    started_at = models.DateTimeField(blank=True, null=True, verbose_name="开始时间")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="完成时间")
    
    class Meta:
        verbose_name = "训练任务"
        verbose_name_plural = "训练任务"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"训练任务 {self.id} - {self.model}" 