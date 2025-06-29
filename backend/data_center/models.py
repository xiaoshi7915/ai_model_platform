"""
数据中心应用的模型
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import os
from django.utils.text import slugify

User = get_user_model()

class Dataset(models.Model):
    """数据集模型"""
    
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('ready', '可用'),
        ('error', '错误'),
    )
    
    name = models.CharField(max_length=100, verbose_name="数据集名称")
    slug = models.SlugField(max_length=120, blank=True, verbose_name="URL别名")
    description = models.TextField(blank=True, null=True, verbose_name="数据集描述")
    file = models.FileField(upload_to='datasets/', verbose_name="数据集文件")
    file_format = models.CharField(max_length=20, verbose_name="文件格式")
    file_size = models.PositiveIntegerField(verbose_name="文件大小(字节)")
    rows_count = models.PositiveIntegerField(default=0, verbose_name="数据行数")
    columns_count = models.PositiveIntegerField(default=0, verbose_name="数据列数")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    status_message = models.TextField(blank=True, null=True, verbose_name="状态消息")
    is_public = models.BooleanField(default=False, verbose_name="是否公开")
    tags = models.CharField(max_length=255, blank=True, null=True, verbose_name="标签")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets', verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "数据集"
        verbose_name_plural = "数据集"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """保存前计算文件大小和创建slug"""
        # 生成slug
        if not self.slug:
            self.slug = slugify(self.name)
            
        # 计算文件大小
        if self.file and not self.file_size and hasattr(self.file, 'size'):
            self.file_size = self.file.size
        
        # 从文件名中提取格式
        if self.file and not self.file_format:
            _, ext = os.path.splitext(self.file.name)
            self.file_format = ext[1:] if ext else ''
        
        # 对file字段设置为非必填
        # 如果是通过代码创建数据，可能没有实际文件
        self._meta.get_field('file').blank = True
        self._meta.get_field('file').null = True
            
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """获取数据集详情页面URL"""
        return f"/data-center/datasets/{self.id}/"
    
    @property
    def file_url(self):
        """获取文件URL"""
        if self.file:
            return self.file.url
        return None
    
    @property 
    def file_size_formatted(self):
        """格式化文件大小"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0 or unit == 'GB':
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} GB"

class KnowledgeBase(models.Model):
    """知识库模型"""
    
    TYPE_CHOICES = (
        ('text', '文本知识库'),
        ('qa', '问答知识库'),
        ('structured', '结构化知识库'),
    )
    
    name = models.CharField(max_length=100, verbose_name="知识库名称")
    slug = models.SlugField(max_length=120, blank=True, verbose_name="URL别名")
    description = models.TextField(blank=True, null=True, verbose_name="知识库描述")
    content = models.TextField(verbose_name="知识库内容")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='text', verbose_name="知识库类型")
    is_public = models.BooleanField(verbose_name="是否公开", default=False)
    tags = models.CharField(max_length=255, blank=True, null=True, verbose_name="标签")
    has_vector_index = models.BooleanField(default=False, verbose_name="是否有向量索引")
    vector_index_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="向量索引路径")
    related_datasets = models.ManyToManyField(Dataset, blank=True, related_name="knowledge_bases", verbose_name="关联数据集")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledge_bases', verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "知识库"
        verbose_name_plural = "知识库"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """保存前生成slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """获取知识库详情页面URL"""
        return f"/data-center/knowledge-bases/{self.id}/"
    
    @property
    def content_preview(self):
        """获取内容预览"""
        if self.content:
            return self.content[:200] + '...' if len(self.content) > 200 else self.content
        return "" 