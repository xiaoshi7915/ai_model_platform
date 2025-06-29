"""
评测中心应用的模型
"""

from django.db import models
from django.contrib.auth.models import User
from training_center.models import Model
from data_center.models import Dataset

class EvaluationTask(models.Model):
    """评测任务模型"""
    
    STATUS_CHOICES = (
        ('pending', '等待中'),
        ('running', '运行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
        ('cancelled', '已取消'),
    )
    
    name = models.CharField(max_length=100, verbose_name="任务名称")
    description = models.TextField(blank=True, null=True, verbose_name="任务描述")
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='evaluation_tasks', verbose_name="评测模型")
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='evaluation_tasks', verbose_name="评测数据集")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    metrics = models.JSONField(default=dict, blank=True, null=True, verbose_name="评测指标")
    parameters = models.JSONField(default=dict, verbose_name="评测参数")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluation_tasks', verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    started_at = models.DateTimeField(blank=True, null=True, verbose_name="开始时间")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="完成时间")
    
    class Meta:
        verbose_name = "评测任务"
        verbose_name_plural = "评测任务"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class EvaluationReport(models.Model):
    """评测报告模型"""
    
    task = models.OneToOneField(EvaluationTask, on_delete=models.CASCADE, related_name='report', verbose_name="评测任务")
    summary = models.TextField(verbose_name="报告摘要")
    details = models.JSONField(default=dict, verbose_name="详细结果")
    charts = models.JSONField(default=dict, blank=True, null=True, verbose_name="图表数据")
    suggestions = models.TextField(blank=True, null=True, verbose_name="改进建议")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "评测报告"
        verbose_name_plural = "评测报告"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.task.name} 的评测报告"

class ModelComparison(models.Model):
    """模型比较模型"""
    
    name = models.CharField(max_length=100, verbose_name="比较名称")
    description = models.TextField(blank=True, null=True, verbose_name="比较描述")
    model_list = models.ManyToManyField('training_center.Model', related_name='comparisons', verbose_name="比较的模型")
    dataset = models.ForeignKey('data_center.Dataset', on_delete=models.CASCADE, related_name='model_comparisons', verbose_name="评测数据集")
    results = models.JSONField(default=dict, verbose_name="比较结果")
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='model_comparisons', verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "模型比较"
        verbose_name_plural = "模型比较"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name 