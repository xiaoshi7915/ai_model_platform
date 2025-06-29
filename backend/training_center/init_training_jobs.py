#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
训练中心测试数据初始化脚本
用于创建训练任务的测试数据
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

# 导入模型
from training_center.models import Model, DockerImage, TrainingJob
from data_center.models import Dataset
from django.contrib.auth.models import User

def create_training_jobs():
    """创建训练任务测试数据"""
    print("正在创建训练任务测试数据...")
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    # 获取已存在的模型和Docker镜像
    models = Model.objects.all()
    docker_images = DockerImage.objects.all()
    
    # 如果没有Docker镜像，创建一些
    if not docker_images.exists():
        docker_images = create_docker_images(admin_user)
    
    # 如果没有模型，无法创建训练任务
    if not models.exists():
        print("  - 没有可用的模型，无法创建训练任务")
        return []
    
    # 创建训练任务
    jobs = []
    statuses = ['pending', 'running', 'completed', 'failed', 'cancelled']
    
    # 为每个模型创建1-2个训练任务
    for model in models:
        # 随机选择Docker镜像
        docker_image = random.choice(list(docker_images))
        
        # 创建1-2个训练任务
        num_jobs = random.randint(1, 2)
        for i in range(num_jobs):
            # 选择任务状态，已完成状态概率高一些
            status = random.choices(
                statuses, 
                weights=[10, 20, 50, 15, 5], 
                k=1
            )[0]
            
            # 计算时间
            created_at = datetime.now() - timedelta(days=random.randint(1, 30))
            started_at = None
            completed_at = None
            
            if status != 'pending':
                started_at = created_at + timedelta(minutes=random.randint(5, 30))
                
                if status in ['completed', 'failed', 'cancelled']:
                    hours = random.randint(1, 24)
                    completed_at = started_at + timedelta(hours=hours)
            
            # 生成日志内容
            log = generate_training_log(status, model.name)
            
            # 创建训练任务
            job, created = TrainingJob.objects.get_or_create(
                model=model,
                docker_image=docker_image,
                created_by=admin_user,
                defaults={
                    'status': status,
                    'log': log,
                    'created_at': created_at,
                    'started_at': started_at,
                    'completed_at': completed_at
                }
            )
            
            if created:
                print(f"  - 创建训练任务: 模型 {model.name}, 状态 {status}")
                jobs.append(job)
    
    return jobs

def create_docker_images(user):
    """创建Docker镜像测试数据"""
    print("正在创建Docker镜像测试数据...")
    
    images = []
    image_templates = [
        ('tensorflow', '2.9.0', 'TensorFlow 深度学习框架', 'docker.io'),
        ('pytorch', '2.0.1', 'PyTorch 深度学习框架', 'docker.io'),
        ('huggingface', 'transformers-latest', 'Hugging Face Transformers', 'docker.io'),
        ('langchain', 'latest', 'LangChain框架', 'docker.io'),
        ('custom-ml', 'v1.2', '自定义机器学习环境', 'registry.example.com')
    ]
    
    for name, tag, desc, registry in image_templates:
        size = random.randint(1000, 10000)  # MB
        image, created = DockerImage.objects.get_or_create(
            name=name,
            tag=tag,
            defaults={
                'description': desc,
                'size': size,
                'registry': registry,
                'created_by': user
            }
        )
        
        if created:
            print(f"  - 创建Docker镜像: {registry}/{name}:{tag}")
        
        images.append(image)
    
    return images

def generate_training_log(status, model_name):
    """生成训练日志"""
    
    # 开始部分
    log = f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 开始训练模型: {model_name}\n"
    log += f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 初始化训练环境...\n"
    log += f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 加载训练数据...\n"
    log += f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 开始训练过程\n\n"
    
    # 根据状态生成不同的日志内容
    if status == 'pending':
        return log + "[INFO] 任务等待中..."
    
    # 添加一些训练迭代日志
    epochs = random.randint(1, 10)
    for epoch in range(1, epochs + 1):
        loss = round(random.uniform(0.1, 2.0) / epoch, 4)
        accuracy = round(random.uniform(0.5, 0.99), 4)
        log += f"Epoch {epoch}/{epochs} - loss: {loss} - accuracy: {accuracy}\n"
    
    # 根据状态添加结束部分
    if status == 'running':
        log += "\n[INFO] 模型训练中，尚未完成..."
    elif status == 'completed':
        log += f"\n[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 训练完成！\n"
        log += f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 最终模型性能 - loss: {round(random.uniform(0.05, 0.5), 4)} - accuracy: {round(random.uniform(0.85, 0.99), 4)}\n"
        log += f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 模型已保存"
    elif status == 'failed':
        error_types = [
            "内存不足",
            "数据格式错误",
            "GPU设备不可用",
            "训练过程中断",
            "优化器不收敛"
        ]
        error_type = random.choice(error_types)
        log += f"\n[ERROR] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 训练失败: {error_type}\n"
        log += f"[ERROR] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 请检查训练参数和环境设置"
    elif status == 'cancelled':
        log += f"\n[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 训练任务已取消"
    
    return log

def main():
    """主函数"""
    print("开始初始化训练中心测试数据...")
    
    # 创建训练任务
    jobs = create_training_jobs()
    
    print("\n测试数据初始化完成！")
    print(f"创建了 {len(jobs)} 个训练任务")

if __name__ == "__main__":
    main() 