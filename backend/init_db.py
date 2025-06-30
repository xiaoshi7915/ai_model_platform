#!/usr/bin/env python
"""
数据库初始化脚本
用于创建超级用户和初始数据
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

def create_superuser():
    """创建超级用户"""
    print("创建超级用户...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123456@'
        )
        print("超级用户创建成功")
    else:
        print("超级用户已存在，跳过创建")

def initialize_dataset_formats():
    """初始化数据集格式 - 跳过，直接使用字符串格式"""
    print("数据集格式使用字符串格式，无需初始化")

def initialize_model_templates():
    """初始化模型模板 - 跳过，无ModelTemplate模型"""
    print("无ModelTemplate模型，跳过初始化")

def initialize_docker_images():
    """初始化Docker镜像"""
    try:
        from training_center.models import DockerImage
        from django.contrib.auth.models import User
        
        print("初始化Docker镜像...")
        admin_user = User.objects.get(username='admin')
        
        images = [
            {
                "name": "pytorch", 
                "tag": "2.0.0-cuda11.7", 
                "registry": "docker.io/pytorch", 
                "description": "PyTorch深度学习框架，支持GPU加速",
                "size": 3800
            },
            {
                "name": "tensorflow", 
                "tag": "2.12.0-gpu", 
                "registry": "docker.io/tensorflow", 
                "description": "TensorFlow深度学习框架，支持GPU加速",
                "size": 4200
            },
            {
                "name": "huggingface/transformers-pytorch", 
                "tag": "latest", 
                "registry": "docker.io", 
                "description": "Hugging Face Transformers库，预安装PyTorch",
                "size": 4500
            },
            {
                "name": "nvidia/cuda", 
                "tag": "11.8-devel-ubuntu20.04", 
                "registry": "docker.io", 
                "description": "NVIDIA CUDA开发环境",
                "size": 2800
            },
            {
                "name": "python", 
                "tag": "3.9-slim", 
                "registry": "docker.io", 
                "description": "Python 3.9 精简版镜像",
                "size": 150
            }
        ]
        
        for image_data in images:
            image, created = DockerImage.objects.get_or_create(
                name=image_data["name"],
                tag=image_data["tag"],
                registry=image_data["registry"],
                defaults={
                    "description": image_data["description"],
                    "size": image_data["size"],
                    "created_by": admin_user
                }
            )
            if created:
                print(f"  - 创建Docker镜像: {image}")
        
        total_count = DockerImage.objects.filter(created_by=admin_user).count()
        print(f"Docker镜像初始化完成，共{total_count}个镜像")
    except Exception as e:
        print(f"初始化Docker镜像时出现错误: {e}")

def initialize_plugins():
    """初始化插件"""
    try:
        from app_center.models import Plugin
        from django.contrib.auth.models import User
        
        print("初始化插件...")
        admin_user = User.objects.get(username='admin')
        
        plugins = [
            {
                "name": "文本摘要", 
                "version": "1.0.0", 
                "description": "自动生成文本摘要的插件",
                "status": "active"
            },
            {
                "name": "情感分析", 
                "version": "1.0.0", 
                "description": "分析文本情感倾向的插件",
                "status": "active"
            },
            {
                "name": "图像识别", 
                "version": "1.0.0", 
                "description": "识别图像中物体的插件",
                "status": "active"
            }
        ]
        
        for plugin_data in plugins:
            plugin, created = Plugin.objects.get_or_create(
                name=plugin_data["name"],
                version=plugin_data["version"],
                defaults={
                    "description": plugin_data["description"],
                    "status": plugin_data["status"],
                    "created_by": admin_user
                }
            )
            if created:
                print(f"  - 创建插件: {plugin}")
        
        total_count = Plugin.objects.filter(created_by=admin_user).count()
        print(f"插件初始化完成，共{total_count}个插件")
    except Exception as e:
        print(f"初始化插件时出现错误: {e}")

def initialize_evaluation_metrics():
    """初始化评测指标 - 跳过，无EvaluationMetric模型"""
    print("无EvaluationMetric模型，跳过初始化")

@transaction.atomic
def main():
    print("开始初始化数据库...")
    create_superuser()
    initialize_dataset_formats()
    initialize_model_templates()
    initialize_docker_images()
    initialize_plugins()
    initialize_evaluation_metrics()
    print("数据库初始化完成")

if __name__ == "__main__":
    main() 