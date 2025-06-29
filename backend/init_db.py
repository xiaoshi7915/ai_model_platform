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
    """初始化数据集格式"""
    try:
        from data_center.models import DatasetFormat
        
        print("初始化数据集格式...")
        formats = [
            {"name": "CSV", "description": "逗号分隔值文件", "extension": "csv"},
            {"name": "JSON", "description": "JavaScript对象表示法", "extension": "json"},
            {"name": "TXT", "description": "文本文件", "extension": "txt"},
            {"name": "XLSX", "description": "Excel表格文件", "extension": "xlsx"},
            {"name": "JSONL", "description": "JSON Lines文件", "extension": "jsonl"},
            {"name": "XML", "description": "可扩展标记语言", "extension": "xml"},
            {"name": "YAML", "description": "YAML Ain't Markup Language", "extension": "yaml"}
        ]
        
        for format_data in formats:
            DatasetFormat.objects.get_or_create(
                name=format_data["name"],
                defaults={
                    "description": format_data["description"],
                    "extension": format_data["extension"]
                }
            )
        
        print(f"数据集格式初始化完成，共{len(formats)}种格式")
    except ImportError:
        print("数据中心模块未找到，跳过初始化数据集格式")
    except Exception as e:
        print(f"初始化数据集格式时出现错误: {e}")

def initialize_model_templates():
    """初始化模型模板"""
    try:
        from training_center.models import ModelTemplate
        
        print("初始化模型模板...")
        templates = [
            {
                "name": "GPT-2",
                "description": "基于Transformer的语言模型，适用于文本生成任务",
                "parameters": {
                    "epochs": 3,
                    "batch_size": 8,
                    "learning_rate": 5e-5
                }
            },
            {
                "name": "BERT",
                "description": "双向Transformer预训练模型，适用于文本理解任务",
                "parameters": {
                    "epochs": 5,
                    "batch_size": 16,
                    "learning_rate": 2e-5
                }
            },
            {
                "name": "ResNet",
                "description": "深度残差网络，适用于图像分类任务",
                "parameters": {
                    "epochs": 10,
                    "batch_size": 32,
                    "learning_rate": 1e-4
                }
            }
        ]
        
        for template_data in templates:
            ModelTemplate.objects.get_or_create(
                name=template_data["name"],
                defaults={
                    "description": template_data["description"],
                    "parameters": template_data["parameters"]
                }
            )
        
        print(f"模型模板初始化完成，共{len(templates)}个模板")
    except ImportError:
        print("训练中心模块未找到，跳过初始化模型模板")
    except Exception as e:
        print(f"初始化模型模板时出现错误: {e}")

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
            }
        ]
        
        for image_data in images:
            DockerImage.objects.get_or_create(
                name=image_data["name"],
                tag=image_data["tag"],
                registry=image_data["registry"],
                defaults={
                    "description": image_data["description"],
                    "size": image_data["size"],
                    "created_by": admin_user
                }
            )
        
        print(f"Docker镜像初始化完成，共{len(images)}个镜像")
    except ImportError:
        print("训练中心模块未找到，跳过初始化Docker镜像")
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
            Plugin.objects.get_or_create(
                name=plugin_data["name"],
                version=plugin_data["version"],
                defaults={
                    "description": plugin_data["description"],
                    "status": plugin_data["status"],
                    "created_by": admin_user
                }
            )
        
        print(f"插件初始化完成，共{len(plugins)}个插件")
    except ImportError:
        print("应用中心模块未找到，跳过初始化插件")
    except Exception as e:
        print(f"初始化插件时出现错误: {e}")

def initialize_evaluation_metrics():
    """初始化评测指标"""
    try:
        from evaluation_center.models import EvaluationMetric
        
        print("初始化评测指标...")
        metrics = [
            {
                "name": "准确率", 
                "code": "accuracy", 
                "description": "分类任务正确预测的比例",
                "type": "classification"
            },
            {
                "name": "F1分数", 
                "code": "f1", 
                "description": "精确率和召回率的调和平均值",
                "type": "classification"
            },
            {
                "name": "BLEU", 
                "code": "bleu", 
                "description": "机器翻译评估指标",
                "type": "text_generation"
            },
            {
                "name": "均方误差", 
                "code": "mse", 
                "description": "回归任务的均方误差",
                "type": "regression"
            }
        ]
        
        for metric_data in metrics:
            EvaluationMetric.objects.get_or_create(
                name=metric_data["name"],
                code=metric_data["code"],
                defaults={
                    "description": metric_data["description"],
                    "type": metric_data["type"]
                }
            )
        
        print(f"评测指标初始化完成，共{len(metrics)}个指标")
    except ImportError:
        print("评测中心模块未找到，跳过初始化评测指标")
    except Exception as e:
        print(f"初始化评测指标时出现错误: {e}")

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