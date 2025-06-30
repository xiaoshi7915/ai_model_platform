#!/usr/bin/env python
"""
初始化示例数据脚本
"""

import os
import sys
import django
from datetime import datetime, timezone

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

from django.contrib.auth.models import User
from data_center.models import Dataset, KnowledgeBase
from training_center.models import Model, DockerImage, TrainingJob
from app_center.models import Application
from evaluation_center.models import EvaluationTask

def create_sample_data():
    """创建示例数据"""
    print("开始创建示例数据...")
    
    # 创建管理员用户（如果不存在）
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123456')
        admin_user.save()
        print("✅ 创建管理员用户: admin")
    else:
        print("ℹ️  管理员用户已存在")
    
    # 创建示例数据集
    datasets_data = [
        {
            'name': '中文文本分类数据集',
            'description': '包含新闻、评论等多种类型的中文文本数据，用于文本分类任务训练',
            'file_format': 'JSON',
            'file_size': 1024 * 1024 * 50,  # 50MB
            'created_by': admin_user
        },
        {
            'name': '情感分析训练集',
            'description': '电商评论情感标注数据，包含正面、负面、中性三种情感标签',
            'file_format': 'CSV',
            'file_size': 1024 * 1024 * 25,  # 25MB
            'created_by': admin_user
        },
        {
            'name': '对话系统数据集',
            'description': '多轮对话数据，适用于聊天机器人和问答系统训练',
            'file_format': 'JSONL',
            'file_size': 1024 * 1024 * 80,  # 80MB
            'created_by': admin_user
        },
        {
            'name': '命名实体识别数据',
            'description': '中文命名实体识别标注数据，包含人名、地名、机构名等实体类型',
            'file_format': 'TXT',
            'file_size': 1024 * 1024 * 15,  # 15MB
            'created_by': admin_user
        },
        {
            'name': '机器翻译平行语料',
            'description': '中英文平行语料库，适用于机器翻译模型训练',
            'file_format': 'TSV',
            'file_size': 1024 * 1024 * 120,  # 120MB
            'created_by': admin_user
        }
    ]
    
    for dataset_data in datasets_data:
        dataset, created = Dataset.objects.get_or_create(
            name=dataset_data['name'],
            defaults=dataset_data
        )
        if created:
            print(f"✅ 创建数据集: {dataset.name}")
    
    # 创建示例知识库
    knowledge_bases_data = [
        {
            'name': '人工智能基础知识库',
            'description': '包含机器学习、深度学习、自然语言处理等AI基础知识',
            'content': '''
人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。

机器学习是人工智能的一个子领域，它使计算机能够在没有明确编程的情况下学习和改进。

深度学习是机器学习的一个子集，使用具有多个层的神经网络来建模和理解复杂的模式。

自然语言处理（NLP）是人工智能的一个分支，专注于计算机与人类语言之间的交互。

常见的机器学习算法包括：
- 线性回归
- 逻辑回归
- 决策树
- 随机森林
- 支持向量机
- 神经网络
            ''',
            'created_by': admin_user
        },
        {
            'name': '产品技术文档',
            'description': '产品相关的技术文档和API说明',
            'content': '''
产品API文档

1. 用户认证API
   - POST /api/auth/login - 用户登录
   - POST /api/auth/logout - 用户退出
   - GET /api/auth/profile - 获取用户信息

2. 数据管理API
   - GET /api/datasets/ - 获取数据集列表
   - POST /api/datasets/ - 创建数据集
   - GET /api/datasets/{id}/ - 获取数据集详情
   - PUT /api/datasets/{id}/ - 更新数据集
   - DELETE /api/datasets/{id}/ - 删除数据集

3. 模型训练API
   - GET /api/models/ - 获取模型列表
   - POST /api/models/ - 创建模型
   - POST /api/models/{id}/train/ - 开始训练
   - GET /api/models/{id}/status/ - 获取训练状态
            ''',
            'created_by': admin_user
        },
        {
            'name': '常见问题解答',
            'description': '用户常见问题及解答',
            'content': '''
常见问题解答（FAQ）

Q: 如何创建新的数据集？
A: 在数据中心页面点击"创建数据集"按钮，填写数据集名称、描述等信息，然后上传数据文件即可。

Q: 支持哪些数据格式？
A: 目前支持CSV、JSON、JSONL、TXT、TSV等格式的数据文件。

Q: 如何开始模型训练？
A: 在训练中心选择或创建模型，配置训练参数，选择数据集后即可开始训练。

Q: 训练需要多长时间？
A: 训练时间取决于数据集大小、模型复杂度和硬件配置，通常从几分钟到几小时不等。

Q: 如何部署训练好的模型？
A: 在应用中心创建新应用，选择训练好的模型，配置部署参数后即可部署。
            ''',
            'created_by': admin_user
        },
        {
            'name': '业务规则手册',
            'description': '业务流程和规则说明',
            'content': '''
业务规则手册

1. 数据管理规则
   - 每个用户最多可创建100个数据集
   - 单个数据集文件大小不超过1GB
   - 数据集名称必须唯一
   - 删除数据集前需确认没有关联的训练任务

2. 模型训练规则
   - 同时最多运行3个训练任务
   - 训练任务超时时间为24小时
   - 训练失败的任务可以重新启动
   - 模型版本号自动递增

3. 应用部署规则
   - 每个用户最多部署10个应用
   - 应用名称在用户范围内必须唯一
   - 应用停止后数据保留7天
   - 应用访问需要有效的API密钥
            ''',
            'created_by': admin_user
        },
        {
            'name': '技术架构说明',
            'description': '系统技术架构和组件说明',
            'content': '''
技术架构说明

系统采用微服务架构，主要包含以下组件：

1. 前端服务
   - 技术栈：Vue.js + Element UI
   - 功能：用户界面、数据展示、交互操作

2. 后端服务
   - 技术栈：Django + Django REST Framework
   - 功能：API服务、业务逻辑、数据处理

3. 数据库
   - 主数据库：PostgreSQL
   - 缓存：Redis
   - 文件存储：MinIO/AWS S3

4. 训练服务
   - 容器化：Docker + Kubernetes
   - GPU支持：NVIDIA CUDA
   - 分布式训练：Horovod

5. 监控服务
   - 日志：ELK Stack
   - 监控：Prometheus + Grafana
   - 告警：AlertManager
            ''',
            'created_by': admin_user
        }
    ]
    
    for kb_data in knowledge_bases_data:
        kb, created = KnowledgeBase.objects.get_or_create(
            name=kb_data['name'],
            defaults=kb_data
        )
        if created:
            print(f"✅ 创建知识库: {kb.name}")
    
    # 获取第一个数据集用于关联
    first_dataset = Dataset.objects.first()
    
    # 创建示例模型
    models_data = [
        {
            'name': 'BERT中文分类模型',
            'description': '基于BERT的中文文本分类模型',
            'version': '1.0',
            'status': 'completed',
            'dataset': first_dataset,
            'created_by': admin_user
        },
        {
            'name': 'GPT-2对话模型',
            'description': '基于GPT-2的中文对话生成模型',
            'version': '1.0',
            'status': 'training',
            'dataset': first_dataset,
            'created_by': admin_user
        },
        {
            'name': '情感分析模型',
            'description': '电商评论情感分析模型',
            'version': '1.0',
            'status': 'completed',
            'dataset': first_dataset,
            'created_by': admin_user
        }
    ]
    
    for model_data in models_data:
        model, created = Model.objects.get_or_create(
            name=model_data['name'],
            version=model_data['version'],
            created_by=admin_user,
            defaults=model_data
        )
        if created:
            print(f"✅ 创建模型: {model.name}")
    
    # 创建示例Docker镜像
    docker_images_data = [
        {
            'name': 'Python基础镜像',
            'tag': 'python:3.9',
            'description': 'Python基础环境，包含常用机器学习库',
            'size': 4857600,  # 约4.6GB
            'registry': 'docker.io',
            'created_by': admin_user
        },
        {
            'name': 'BERT微调镜像',
            'tag': 'bert:base',
            'description': 'BERT预训练模型微调环境',
            'size': 19430400,  # 约18.5GB
            'registry': 'harbor.example.com',
            'created_by': admin_user
        },
        {
            'name': 'GPT训练镜像',
            'tag': 'gpt:neo',
            'description': 'GPT模型训练环境，适用于大规模语言模型',
            'size': 24288000,  # 约23.2GB
            'registry': 'harbor.example.com',
            'created_by': admin_user
        },
        {
            'name': 'TensorFlow训练镜像',
            'tag': 'tensorflow:2.8',
            'description': 'TensorFlow深度学习环境',
            'size': 14572800,  # 约13.9GB
            'registry': 'docker.io',
            'created_by': admin_user
        },
        {
            'name': 'PyTorch训练镜像',
            'tag': 'pytorch:1.10',
            'description': 'PyTorch深度学习环境，适合研究和开发',
            'size': 9715200,   # 约9.3GB
            'registry': 'docker.io',
            'created_by': admin_user
        },
        {
            'name': '测试镜像',
            'tag': '1.0.0',
            'description': '用于测试的轻量级镜像',
            'size': 1000,
            'registry': 'docker.io',
            'created_by': admin_user
        },
        {
            'name': '测试镜像',
            'tag': '新功能',
            'description': '包含新功能的测试镜像',
            'size': 1000,
            'registry': 'docker.io',
            'created_by': admin_user
        }
    ]
    
    for image_data in docker_images_data:
        image, created = DockerImage.objects.get_or_create(
            name=image_data['name'],
            tag=image_data['tag'],
            registry=image_data['registry'],
            defaults=image_data
        )
        if created:
            print(f"✅ 创建Docker镜像: {image.name}:{image.tag}")
    
    # 获取第一个模型用于关联应用
    first_model = Model.objects.first()
    
    # 创建示例应用
    applications_data = [
        {
            'name': '智能客服助手',
            'description': '基于AI的智能客服问答系统',
            'model': first_model,
            'status': 'running',
            'created_by': admin_user
        },
        {
            'name': '文档智能分析',
            'description': '自动分析和分类文档内容',
            'model': first_model,
            'status': 'stopped',
            'created_by': admin_user
        },
        {
            'name': '情感监控系统',
            'description': '实时监控用户评论情感变化',
            'model': first_model,
            'status': 'running',
            'created_by': admin_user
        }
    ]
    
    for app_data in applications_data:
        app, created = Application.objects.get_or_create(
            name=app_data['name'],
            created_by=admin_user,
            defaults=app_data
        )
        if created:
            print(f"✅ 创建应用: {app.name}")
    
    print("✅ 示例数据创建完成！")
    print("\n数据统计:")
    print(f"- 数据集: {Dataset.objects.count()} 个")
    print(f"- 知识库: {KnowledgeBase.objects.count()} 个")
    print(f"- 模型: {Model.objects.count()} 个")
    print(f"- Docker镜像: {DockerImage.objects.count()} 个")
    print(f"- 应用: {Application.objects.count()} 个")

if __name__ == '__main__':
    create_sample_data() 