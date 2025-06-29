#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
训练中心测试数据初始化脚本
用于创建模型、训练任务和Docker镜像的测试数据
"""

import os
import sys
import django
import random
import json
import uuid
from datetime import datetime, timedelta
from django.utils import timezone

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

# 导入模型
from training_center.models import Model, DockerImage, TrainingJob
from data_center.models import Dataset
from django.contrib.auth.models import User

def create_docker_images():
    """创建Docker镜像测试数据"""
    print("正在创建Docker镜像测试数据...")
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    # Docker镜像模板
    image_templates = [
        # 基础框架镜像
        ('pytorch', '2.0.1', 'PyTorch深度学习框架基础镜像', 'docker.io/pytorch/pytorch'),
        ('tensorflow', '2.12.0', 'TensorFlow深度学习框架基础镜像', 'docker.io/tensorflow/tensorflow'),
        ('jax', '0.4.13', 'JAX科学计算库基础镜像', 'docker.io/jaxlib/jax'),
        
        # 预训练模型镜像
        ('llama', '2-7b', 'Meta开源大语言模型LLaMA 2-7B', 'registry.example.com/llm/llama'),
        ('bert', 'base', 'BERT基础预训练模型', 'registry.example.com/nlp/bert'),
        ('stable-diffusion', 'v2.1', 'Stable Diffusion图像生成模型', 'registry.example.com/diffusion/sd'),
        
        # 专业领域镜像
        ('medical-nlp', '1.0', '医疗领域NLP模型训练环境', 'registry.example.com/domain/medical'),
        ('financial-analytics', '2.1', '金融分析模型训练环境', 'registry.example.com/domain/finance'),
        ('vision-transformer', '1.2', 'Vision Transformer训练环境', 'registry.example.com/vision/vit'),
        
        # 自定义训练镜像
        ('custom-training', 'latest', '自定义训练环境', 'registry.example.com/custom/training'),
        ('distributed-training', 'v1.5', '分布式训练环境', 'registry.example.com/infra/distributed')
    ]
    
    images_created = []
    
    for name, tag, description, registry in image_templates:
        # 随机生成镜像大小（MB）
        size = random.randint(500, 5000)  # 直接使用MB为单位
        
        # 随机创建时间
        created_at = timezone.now() - timedelta(days=random.randint(1, 180))
        
        # 创建Docker镜像
        docker_image, created = DockerImage.objects.get_or_create(
            name=name,
            tag=tag,
            defaults={
                'description': description,
                'registry': registry,
                'size': size,
                'created_by': admin_user,
                'created_at': created_at
            }
        )
        
        if created:
            print(f"  - 创建Docker镜像: {name}:{tag}")
            print(f"    大小: {size} MB, 仓库: {registry}")
            images_created.append(docker_image)
    
    return images_created

def create_models():
    """创建模型测试数据"""
    print("\n正在创建模型测试数据...")
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    # 获取已有数据集，如果没有，则跳过
    datasets = list(Dataset.objects.all())
    if not datasets:
        print("没有找到数据集，请先运行数据中心初始化脚本")
    
    # 模型模板
    model_templates = [
        # 文本类模型
        ('通用对话模型', '基于Transformer的通用对话大模型', 'nlp', 'dialogue'),
        ('情感分析模型', '用于分析文本情感倾向的BERT变体模型', 'nlp', 'sentiment'),
        ('医疗文本理解', '医疗领域专用的文本理解模型', 'nlp', 'medical'),
        ('法律文书分析', '用于分析法律文书内容的专业模型', 'nlp', 'legal'),
        ('金融文本挖掘', '针对金融领域的文本挖掘与分析模型', 'nlp', 'finance'),
        
        # 图像类模型
        ('物体检测模型', '基于YOLO的通用物体检测模型', 'vision', 'object_detection'),
        ('医疗影像分析', '用于医疗影像诊断的深度学习模型', 'vision', 'medical'),
        ('人脸识别系统', '高精度人脸识别与验证模型', 'vision', 'facial_recognition'),
        
        # 多模态模型
        ('图文理解模型', '用于理解图像与文本关系的多模态模型', 'multimodal', 'image_text'),
        ('视频内容分析', '用于分析视频内容与字幕的多模态模型', 'multimodal', 'video_text'),
        
        # 推荐系统模型
        ('用户行为预测', '基于用户历史行为的推荐系统模型', 'recommendation', 'user_behavior'),
        ('金融风控模型', '用于金融风险控制的预测模型', 'prediction', 'finance')
    ]
    
    # 获取所有DockerImage
    docker_images = list(DockerImage.objects.all())
    
    models_created = []
    
    for name, desc, type_name, domain in model_templates:
        # 随机版本和状态
        version = f"v{random.randint(1, 5)}.{random.randint(0, 9)}"
        status = random.choice(['draft', 'training', 'trained', 'failed', 'deployed'])
        
        # 随机参数
        parameters = {}
        
        # 基础参数
        parameters.update({
            'batch_size': random.choice([8, 16, 32, 64, 128]),
            'learning_rate': random.choice([1e-5, 3e-5, 5e-5, 1e-4, 3e-4]),
            'epochs': random.randint(1, 50),
            'optimizer': random.choice(['Adam', 'SGD', 'AdamW', 'RMSprop']),
            'random_seed': random.randint(1, 10000)
        })
        
        # 根据模型类型添加特定参数
        if type_name == 'nlp':
            parameters.update({
                'model_size': random.choice(['base', 'large', 'small']),
                'vocab_size': random.choice([30000, 50000, 100000]),
                'max_seq_length': random.choice([128, 256, 512, 1024, 2048]),
                'hidden_size': random.choice([768, 1024, 2048, 4096])
            })
        elif type_name == 'vision':
            parameters.update({
                'image_size': random.choice([224, 256, 384, 512]),
                'backbone': random.choice(['ResNet50', 'ViT', 'EfficientNet', 'ConvNeXt']),
                'augmentation': random.choice(['basic', 'advanced', 'none']),
                'pretrained': random.choice([True, False])
            })
        elif type_name == 'multimodal':
            parameters.update({
                'text_encoder': random.choice(['BERT', 'RoBERTa', 'T5']),
                'vision_encoder': random.choice(['ResNet', 'ViT', 'CLIP']),
                'fusion_type': random.choice(['early', 'late', 'hybrid']),
                'modality_dims': random.choice([768, 1024, 2048])
            })
        
        # 随机指标
        metrics = {}
        
        if status in ['trained', 'deployed']:
            if type_name == 'nlp':
                metrics.update({
                    'accuracy': round(random.uniform(0.7, 0.98), 4),
                    'perplexity': round(random.uniform(5, 50), 2),
                    'f1_score': round(random.uniform(0.65, 0.95), 4)
                })
            elif type_name == 'vision':
                metrics.update({
                    'precision': round(random.uniform(0.7, 0.95), 4),
                    'recall': round(random.uniform(0.65, 0.94), 4),
                    'mAP': round(random.uniform(0.6, 0.9), 4),
                    'inference_time': round(random.uniform(5, 500), 2)
                })
            elif type_name == 'multimodal':
                metrics.update({
                    'retrieval_r@1': round(random.uniform(0.5, 0.9), 4),
                    'retrieval_r@5': round(random.uniform(0.7, 0.95), 4),
                    'alignment_score': round(random.uniform(0.6, 0.9), 4)
                })
            elif type_name in ['recommendation', 'prediction']:
                metrics.update({
                    'auc': round(random.uniform(0.75, 0.95), 4),
                    'precision': round(random.uniform(0.7, 0.9), 4),
                    'recall': round(random.uniform(0.65, 0.85), 4),
                    'f1_score': round(random.uniform(0.68, 0.88), 4)
                })
        
        # 随机创建和更新时间
        created_at = timezone.now() - timedelta(days=random.randint(7, 180))
        updated_at = created_at + timedelta(days=random.randint(1, 7))
        
        # 随机选择数据集
        dataset = random.choice(datasets) if datasets else None
        
        # 创建模型
        model, created = Model.objects.get_or_create(
            name=name,
            version=version,
            defaults={
                'description': f"{desc}\n类型: {type_name}\n领域: {domain}",
                'status': status,
                'parameters': parameters,
                'metrics': metrics,
                'dataset': dataset,
                'created_by': admin_user,
                'created_at': created_at,
                'updated_at': updated_at
            }
        )
        
        if created:
            print(f"  - 创建模型: {name} {version} ({type_name}/{domain})")
            print(f"    状态: {status}, 数据集: {dataset.name if dataset else 'None'}")
            models_created.append(model)
    
    return models_created

def create_training_jobs(models, docker_images):
    """创建训练任务测试数据"""
    print("\n正在创建训练任务测试数据...")
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    jobs_created = []
    
    # 为每个模型创建1-3个训练任务
    for model in models:
        num_jobs = random.randint(1, 3)
        
        for i in range(num_jobs):
            # 随机选择Docker镜像
            docker_image = random.choice(docker_images)
            
            # 随机状态
            status = random.choice(['pending', 'running', 'completed', 'failed', 'canceled'])
            
            # 随机创建时间和更新时间
            created_at = timezone.now() - timedelta(days=random.randint(1, 30))
            updated_at = created_at
            
            if status in ['running']:
                updated_at = timezone.now() - timedelta(minutes=random.randint(5, 120))
            elif status in ['completed', 'failed', 'canceled']:
                updated_at = created_at + timedelta(hours=random.randint(1, 48))
            
            # 生成训练日志
            log = ""
            
            if status != 'pending':
                log_lines = [
                    f"[{created_at.strftime('%Y-%m-%d %H:%M:%S')}] 开始训练任务",
                    f"[{created_at.strftime('%Y-%m-%d %H:%M:%S')}] 加载Docker镜像: {docker_image.name}:{docker_image.tag}",
                    f"[{created_at.strftime('%Y-%m-%d %H:%M:%S')}] 配置参数: {json.dumps(model.parameters, ensure_ascii=False)}"
                ]
                
                # 添加进度日志
                if status in ['running', 'completed', 'failed']:
                    for epoch in range(1, random.randint(2, 6)):
                        timestamp = created_at + timedelta(minutes=epoch * random.randint(10, 30))
                        loss = round(random.uniform(0.1, 2.0) / epoch, 4)
                        accuracy = round(random.uniform(0.7, 0.98), 4)
                        log_lines.append(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] Epoch {epoch}: loss={loss}, accuracy={accuracy}")
                
                # 添加完成或失败日志
                if status == 'completed':
                    log_lines.append(f"[{updated_at.strftime('%Y-%m-%d %H:%M:%S')}] 训练完成！")
                    log_lines.append(f"[{updated_at.strftime('%Y-%m-%d %H:%M:%S')}] 最终指标: {json.dumps(model.metrics, ensure_ascii=False)}")
                elif status == 'failed':
                    error_types = [
                        "内存不足",
                        "CUDA错误: out of memory",
                        "数据集加载失败",
                        "训练中断: 节点故障",
                        "梯度爆炸"
                    ]
                    error = random.choice(error_types)
                    log_lines.append(f"[{updated_at.strftime('%Y-%m-%d %H:%M:%S')}] 错误: {error}")
                    log_lines.append(f"[{updated_at.strftime('%Y-%m-%d %H:%M:%S')}] 训练失败")
                elif status == 'canceled':
                    log_lines.append(f"[{updated_at.strftime('%Y-%m-%d %H:%M:%S')}] 训练被用户取消")
                
                log = "\n".join(log_lines)
            
            # 创建训练任务
            job, created = TrainingJob.objects.get_or_create(
                model=model,
                docker_image=docker_image,
                created_at=created_at,
                defaults={
                    'status': status,
                    'log': log,
                    'created_by': admin_user
                }
            )
            
            if created:
                print(f"  - 创建训练任务: 模型 {model.name} 使用 {docker_image.name}:{docker_image.tag}")
                print(f"    状态: {status}, 创建时间: {created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                jobs_created.append(job)
    
    return jobs_created

def main():
    """主函数"""
    print("开始初始化训练中心测试数据...")
    
    # 创建Docker镜像
    docker_images = create_docker_images()
    
    # 创建模型
    models = create_models()
    
    # 创建训练任务
    jobs = create_training_jobs(models, docker_images)
    
    print("\n测试数据初始化完成！")
    print(f"创建了 {len(docker_images)} 个Docker镜像")
    print(f"创建了 {len(models)} 个模型")
    print(f"创建了 {len(jobs)} 个训练任务")

if __name__ == "__main__":
    main() 