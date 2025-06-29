#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
评测中心测试数据初始化脚本
用于创建评测任务、评测报告和评测对比的测试数据
"""

import os
import sys
import django
import random
import json
from datetime import datetime, timedelta

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

# 导入模型
from evaluation_center.models import EvaluationTask, EvaluationReport, ModelComparison
from training_center.models import Model
from data_center.models import Dataset

# 导入Django用户模型
from django.contrib.auth.models import User


def create_test_models():
    """创建测试模型数据"""
    print("正在创建测试模型...")
    
    models = []
    model_names = [
        "Claude 3", "GPT-4", "LLaMA 3", 
        "Gemini Pro", "Mistral 7B", "Baichuan-13B",
        "Qwen-7B", "ChatGLM-6B", "Falcon-7B"
    ]
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    for i, name in enumerate(model_names):
        # 创建参数字典，包含模型大小和类型
        params = {
            'size': random.randint(7, 70) * 1024 * 1024 * 1024,  # 7GB-70GB
            'parameters_count': random.choice([7, 13, 20, 70, 175]) * 1000000000,
            'type': random.choice(['生成式', '对话式', '理解式', '问答式']),
        }
        
        model, created = Model.objects.get_or_create(
            name=name,
            version=f"1.{i}",
            defaults={
                'description': f"{name} 是一个大型语言模型，支持多语言的文本生成和理解。",
                'status': 'completed',
                'parameters': params,
                'created_by': admin_user,
            }
        )
        if created:
            print(f"  - 创建模型: {name}")
        models.append(model)
    
    return models


def create_test_datasets():
    """创建测试数据集"""
    print("正在创建测试数据集...")
    
    datasets = []
    dataset_names = [
        "GSMK8数据集", "HumanEval数据集", "MMLU数据集", 
        "BBH数据集", "C-Eval数据集", "CMMLU数据集"
    ]
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    for name in dataset_names:
        file_format = random.choice(['csv', 'json', 'txt', 'parquet'])
        file_size = random.randint(10, 500) * 1024 * 1024  # 10MB-500MB
        rows_count = random.randint(1000, 10000)
        cols_count = random.randint(5, 50)
        
        dataset, created = Dataset.objects.get_or_create(
            name=name,
            defaults={
                'description': f"{name} 是一个用于评估大型语言模型能力的测试数据集。",
                'file_format': file_format,
                'file_size': file_size,
                'rows_count': rows_count,
                'columns_count': cols_count,
                'status': 'ready',
                'is_public': True,
                'tags': '评测,大语言模型,基准测试',
                'created_by': admin_user,
            }
        )
        if created:
            print(f"  - 创建数据集: {name}")
        datasets.append(dataset)
    
    return datasets


def create_evaluation_tasks(models, datasets):
    """创建评测任务"""
    print("正在创建评测任务...")
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    # 评测指标
    metrics_list = [
        ["accuracy", "precision", "recall"],
        ["accuracy", "f1"],
        ["accuracy", "latency"],
        ["bleu", "rouge"],
        ["accuracy"],
        ["coherence", "fluency"],
    ]
    
    tasks = []
    
    # 随机创建10个评测任务
    for i in range(1, 11):
        model = random.choice(models)
        dataset = random.choice(datasets)
        task_metrics = random.choice(metrics_list)
        
        # 生成不同状态的任务
        if i <= 3:  # 30%的任务已完成
            status = "completed"
            progress = 100
        elif i <= 7:  # 40%的任务进行中
            status = "running"
            progress = random.randint(30, 95)
        else:  # 30%的任务失败
            status = "failed"
            progress = random.randint(10, 90)
        
        task, created = EvaluationTask.objects.get_or_create(
            name=f"{model.name}性能评测",
            defaults={
                'description': f"评估{model.name}在{dataset.name}上的表现",
                'model': model,
                'dataset': dataset,
                'metrics': task_metrics,
                'status': status,
                'created_by': admin_user,
                'parameters': {'progress': progress},
            }
        )
        
        if created:
            print(f"  - 创建评测任务: {task.name} (状态: {status}, 进度: {progress}%)")
            
            # 对于已完成的任务，创建评测报告
            if status == "completed":
                results = {}
                for metric in task_metrics:
                    if metric in ["accuracy", "precision", "recall", "f1"]:
                        results[metric] = round(random.uniform(0.70, 0.98), 4)
                    elif metric == "latency":
                        results[metric] = round(random.uniform(100, 500), 2)  # ms
                    elif metric in ["bleu", "rouge"]:
                        results[metric] = round(random.uniform(0.3, 0.7), 4)
                    elif metric in ["coherence", "fluency"]:
                        results[metric] = round(random.uniform(3.0, 4.8), 2)  # 1-5分
                
                # 创建图表数据
                charts = {
                    'confusion_matrix': {
                        'labels': ['类别A', '类别B', '类别C', '类别D'],
                        'values': [
                            [85, 5, 7, 3],
                            [8, 82, 6, 4],
                            [5, 7, 81, 7],
                            [4, 6, 8, 82]
                        ]
                    },
                    'roc_curve': {
                        'fpr': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        'tpr': [0, 0.55, 0.7, 0.8, 0.85, 0.9, 0.92, 0.95, 0.97, 0.99, 1.0]
                    }
                }
                
                # 创建评测报告
                report = EvaluationReport.objects.create(
                    task=task,
                    summary=f"{model.name}在{dataset.name}上的评测结果显示其性能表现良好。",
                    details=results,
                    charts=charts,
                    suggestions="1. 增加训练数据多样性可能进一步提高模型性能\n2. 考虑使用更大的模型参数量\n3. 优化模型推理速度",
                    created_at=task.created_at + timedelta(hours=random.randint(1, 5))
                )
                print(f"    - 创建评测报告，指标: {results}")
            
        tasks.append(task)
    
    return tasks


def create_model_comparisons(models, datasets):
    """创建模型对比数据"""
    print("正在创建模型对比数据...")
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    # 随机选择数据集
    dataset = random.choice(datasets)
    
    comparisons = []
    
    # 创建3个模型对比
    for i in range(3):
        # 随机选择2-3个模型进行对比
        comparison_models = random.sample(models, random.randint(2, min(3, len(models))))
        
        # 创建比较名称
        model_names = [model.name for model in comparison_models]
        comparison_name = " vs ".join(model_names)
        
        # 创建比较结果
        results = {}
        for model in comparison_models:
            results[model.name] = {
                'accuracy': round(random.uniform(0.70, 0.98), 4),
                'latency': round(random.uniform(100, 500), 2),
                'f1': round(random.uniform(0.70, 0.95), 4),
                'bleu': round(random.uniform(0.3, 0.7), 4) if random.choice([True, False]) else None
            }
        
        comparison, created = ModelComparison.objects.get_or_create(
            name=comparison_name,
            defaults={
                'description': f"比较{comparison_name}在{dataset.name}上的表现",
                'dataset': dataset,
                'results': results,
                'created_by': admin_user,
            }
        )
        
        # 添加模型到多对多关系
        if created:
            for model in comparison_models:
                comparison.model_list.add(model)
            
            print(f"  - 创建模型对比: {comparison_name}")
            print(f"    - 包含模型: {', '.join(model_names)}")
        
        comparisons.append(comparison)
    
    return comparisons


def main():
    """主函数"""
    print("开始初始化评测中心测试数据...")
    
    # 创建测试模型和数据集
    models = create_test_models()
    datasets = create_test_datasets()
    
    # 创建评测任务
    tasks = create_evaluation_tasks(models, datasets)
    
    # 创建模型对比
    comparisons = create_model_comparisons(models, datasets)
    
    print("\n测试数据初始化完成！")
    print(f"创建了 {len(models)} 个模型")
    print(f"创建了 {len(datasets)} 个数据集")
    print(f"创建了 {len(tasks)} 个评测任务")
    print(f"创建了 {len(comparisons)} 个模型对比")


if __name__ == "__main__":
    main() 