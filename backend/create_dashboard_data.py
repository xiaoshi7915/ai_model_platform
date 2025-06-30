#!/usr/bin/env python
"""
创建仪表盘显示需要的测试数据
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction

def create_test_datasets():
    """创建测试数据集"""
    try:
        from data_center.models import Dataset
        
        print("创建测试数据集...")
        admin_user = User.objects.get(username='admin')
        
        datasets = [
            {
                "name": "客户评论数据集",
                "description": "包含5万条客户评论数据，用于情感分析训练",
                "file_format": "csv",
                "file_size": 15728640,  # 15MB
                "rows_count": 50000,
                "columns_count": 3
            },
            {
                "name": "产品图片数据集", 
                "description": "1万张产品图片，包含10个类别",
                "file_format": "zip",
                "file_size": 209715200,  # 200MB
                "rows_count": 10000,
                "columns_count": 2
            },
            {
                "name": "新闻文本数据集",
                "description": "3万条新闻文本，用于文本分类",
                "file_format": "json",
                "file_size": 134217728,  # 128MB
                "rows_count": 30000,
                "columns_count": 4
            },
            {
                "name": "语音识别数据集",
                "description": "语音转文本训练数据",
                "file_format": "wav",
                "file_size": 536870912,  # 512MB
                "rows_count": 20000,
                "columns_count": 2
            },
            {
                "name": "对话数据集",
                "description": "多轮对话数据，用于聊天机器人训练",
                "file_format": "jsonl",
                "file_size": 94371840,  # 90MB
                "rows_count": 15000,
                "columns_count": 3
            }
        ]
        
        for dataset_data in datasets:
            dataset, created = Dataset.objects.get_or_create(
                name=dataset_data["name"],
                defaults={
                    "description": dataset_data["description"],
                    "file_format": dataset_data["file_format"],
                    "file_size": dataset_data["file_size"],
                    "rows_count": dataset_data["rows_count"],
                    "columns_count": dataset_data["columns_count"],
                    "status": "ready",
                    "created_by": admin_user
                }
            )
            if created:
                print(f"  - 创建数据集: {dataset.name}")
        
        total_count = Dataset.objects.filter(created_by=admin_user).count()
        print(f"测试数据集创建完成，共{total_count}个数据集")
        return total_count
    except Exception as e:
        print(f"创建测试数据集时出现错误: {e}")
        return 0

def create_test_models():
    """创建测试模型"""
    try:
        from training_center.models import Model
        from data_center.models import Dataset
        
        print("创建测试模型...")
        admin_user = User.objects.get(username='admin')
        
        # 获取数据集
        datasets = Dataset.objects.filter(created_by=admin_user)
        first_dataset = datasets.first() if datasets.exists() else None
        
        models = [
            {
                "name": "情感分析模型",
                "version": "1.0",
                "description": "基于BERT的情感分析模型",
                "status": "completed",
                "parameters": {"epochs": 3, "batch_size": 16, "learning_rate": 2e-5},
                "metrics": {"accuracy": 0.92, "f1_score": 0.89},
                "dataset": first_dataset
            },
            {
                "name": "产品图片分类器",
                "version": "1.0",
                "description": "基于ResNet的图片分类模型",
                "status": "completed",
                "parameters": {"epochs": 10, "batch_size": 32, "learning_rate": 1e-4},
                "metrics": {"accuracy": 0.87, "precision": 0.85},
                "dataset": first_dataset
            },
            {
                "name": "新闻分类模型",
                "version": "1.0",
                "description": "多类别新闻文本分类器",
                "status": "training",
                "parameters": {"epochs": 5, "batch_size": 8, "learning_rate": 3e-5},
                "dataset": first_dataset
            },
            {
                "name": "语音识别模型",
                "version": "1.0",
                "description": "中文语音转文本模型",
                "status": "completed",
                "parameters": {"epochs": 20, "batch_size": 4, "learning_rate": 1e-4},
                "metrics": {"wer": 0.15, "cer": 0.08},
                "dataset": first_dataset
            },
            {
                "name": "对话生成模型",
                "version": "1.0",
                "description": "基于GPT的对话生成模型",
                "status": "failed",
                "parameters": {"epochs": 8, "batch_size": 4, "learning_rate": 5e-5},
                "dataset": first_dataset
            },
            {
                "name": "推荐系统模型",
                "version": "1.0",
                "description": "商品推荐算法模型",
                "status": "draft",
                "parameters": {"epochs": 15, "batch_size": 64, "learning_rate": 1e-3},
                "dataset": first_dataset
            },
            {
                "name": "OCR文字识别",
                "version": "1.0",
                "description": "图片文字识别模型",
                "status": "completed",
                "parameters": {"epochs": 12, "batch_size": 16, "learning_rate": 2e-4},
                "metrics": {"accuracy": 0.94, "precision": 0.92},
                "dataset": first_dataset
            }
        ]
        
        for model_data in models:
            model, created = Model.objects.get_or_create(
                name=model_data["name"],
                version=model_data["version"],
                created_by=admin_user,
                defaults={
                    "description": model_data["description"],
                    "status": model_data["status"],
                    "parameters": model_data["parameters"],
                    "metrics": model_data.get("metrics", {}),
                    "dataset": model_data["dataset"]
                }
            )
            if created:
                print(f"  - 创建模型: {model.name}")
        
        total_count = Model.objects.filter(created_by=admin_user).count()
        print(f"测试模型创建完成，共{total_count}个模型")
        return total_count
    except Exception as e:
        print(f"创建测试模型时出现错误: {e}")
        return 0

def create_test_applications():
    """创建测试应用"""
    try:
        from app_center.models import Application
        from training_center.models import Model
        
        print("创建测试应用...")
        admin_user = User.objects.get(username='admin')
        
        # 获取已完成的模型
        completed_models = Model.objects.filter(status='completed', created_by=admin_user)
        if not completed_models.exists():
            print("没有已完成的模型，跳过创建应用")
            return 0
        
        applications = [
            {
                "name": "智能客服系统",
                "description": "基于情感分析的智能客服应用",
                "status": "running",
                "config": {"port": 8001, "replicas": 2},
                "model": completed_models.first()
            },
            {
                "name": "商品图片识别",
                "description": "自动识别商品类别的应用",
                "status": "running",
                "config": {"port": 8002, "replicas": 1},
                "model": completed_models.first()
            },
            {
                "name": "语音助手",
                "description": "语音转文本助手应用",
                "status": "stopped",
                "config": {"port": 8003, "replicas": 1},
                "model": completed_models.last() if completed_models.count() > 1 else completed_models.first()
            },
            {
                "name": "文档OCR识别",
                "description": "自动识别文档中的文字",
                "status": "running",
                "config": {"port": 8004, "replicas": 3},
                "model": completed_models.last() if completed_models.count() > 1 else completed_models.first()
            }
        ]
        
        for app_data in applications:
            app, created = Application.objects.get_or_create(
                name=app_data["name"],
                created_by=admin_user,
                defaults={
                    "description": app_data["description"],
                    "status": app_data["status"],
                    "config": app_data["config"],
                    "model": app_data["model"]
                }
            )
            if created:
                print(f"  - 创建应用: {app.name}")
        
        total_count = Application.objects.filter(created_by=admin_user).count()
        print(f"测试应用创建完成，共{total_count}个应用")
        return total_count
    except Exception as e:
        print(f"创建测试应用时出现错误: {e}")
        return 0

def create_test_evaluation_tasks():
    """创建测试评测任务"""
    try:
        from evaluation_center.models import EvaluationTask
        from training_center.models import Model
        from data_center.models import Dataset
        
        print("创建测试评测任务...")
        admin_user = User.objects.get(username='admin')
        
        # 获取模型和数据集
        models = Model.objects.filter(created_by=admin_user)
        datasets = Dataset.objects.filter(created_by=admin_user)
        
        if not models.exists() or not datasets.exists():
            print("没有足够的模型或数据集，跳过创建评测任务")
            return 0
        
        tasks = [
            {
                "name": "情感分析模型性能评测",
                "description": "评测情感分析模型的准确率和F1分数",
                "status": "completed",
                "metrics": {"accuracy": 0.92, "f1_score": 0.89, "precision": 0.91, "recall": 0.87},
                "parameters": {"test_size": 0.2, "batch_size": 16},
                "model": models.first(),
                "dataset": datasets.first()
            },
            {
                "name": "图片分类模型评测",
                "description": "评测图片分类模型的分类精度",
                "status": "running",
                "metrics": {},
                "parameters": {"test_size": 0.2, "batch_size": 32},
                "model": models.first(),
                "dataset": datasets.first()
            },
            {
                "name": "语音识别准确率测试",
                "description": "测试语音识别的字符错误率和词错误率",
                "status": "completed",
                "metrics": {"wer": 0.15, "cer": 0.08},
                "parameters": {"test_size": 0.2, "batch_size": 8},
                "model": models.first(),
                "dataset": datasets.first()
            },
            {
                "name": "对话模型质量评估",
                "description": "评估对话生成的质量和相关性",
                "status": "pending",
                "metrics": {},
                "parameters": {"test_size": 0.2, "max_length": 512},
                "model": models.first(),
                "dataset": datasets.first()
            },
            {
                "name": "推荐系统效果测试",
                "description": "测试推荐算法的准确率和覆盖率",
                "status": "failed",
                "metrics": {},
                "parameters": {"test_size": 0.2, "top_k": 10},
                "model": models.first(),
                "dataset": datasets.first()
            },
            {
                "name": "OCR识别精度测试",
                "description": "测试文字识别的准确率",
                "status": "completed",
                "metrics": {"accuracy": 0.94, "precision": 0.92, "recall": 0.90},
                "parameters": {"test_size": 0.2, "image_size": 224},
                "model": models.first(),
                "dataset": datasets.first()
            },
            {
                "name": "多模型对比评测",
                "description": "对比多个模型在相同数据集上的性能",
                "status": "running",
                "metrics": {},
                "parameters": {"test_size": 0.2, "cross_validation": True},
                "model": models.first(),
                "dataset": datasets.first()
            }
        ]
        
        for task_data in tasks:
            task, created = EvaluationTask.objects.get_or_create(
                name=task_data["name"],
                created_by=admin_user,
                defaults={
                    "description": task_data["description"],
                    "status": task_data["status"],
                    "metrics": task_data["metrics"],
                    "parameters": task_data["parameters"],
                    "model": task_data["model"],
                    "dataset": task_data["dataset"]
                }
            )
            if created:
                print(f"  - 创建评测任务: {task.name}")
        
        total_count = EvaluationTask.objects.filter(created_by=admin_user).count()
        print(f"测试评测任务创建完成，共{total_count}个任务")
        return total_count
    except Exception as e:
        print(f"创建测试评测任务时出现错误: {e}")
        return 0

@transaction.atomic
def main():
    """主函数"""
    print("开始创建仪表盘测试数据...")
    
    dataset_count = create_test_datasets()
    model_count = create_test_models()
    app_count = create_test_applications() 
    task_count = create_test_evaluation_tasks()
    
    print("\n=== 仪表盘测试数据创建完成 ===")
    print(f"数据集: {dataset_count} 个")
    print(f"模型: {model_count} 个")
    print(f"应用: {app_count} 个")
    print(f"评测任务: {task_count} 个")
    print("=================================")

if __name__ == "__main__":
    main() 