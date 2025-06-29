#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试数据生成脚本
用于生成大型模型构建管理平台的测试数据
"""

import os
import django
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
import random
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

from django.contrib.auth.models import User
try:
    from data_center.models import Dataset, DatasetFormat, Chunk, KnowledgeBase
except ImportError:
    print("数据中心模块未找到")
    Dataset, DatasetFormat, Chunk, KnowledgeBase = None, None, None, None

try:
    from training_center.models import Model, DockerImage, TrainingJob
except ImportError:
    print("训练中心模块未找到")
    Model, DockerImage, TrainingJob = None, None, None

try:
    from app_center.models import Application, Plugin, ApplicationLog, ApplicationMetric
except ImportError:
    print("应用中心模块未找到")
    Application, Plugin, ApplicationLog, ApplicationMetric = None, None, None, None

try:
    from evaluation_center.models import EvaluationTask, EvaluationMetric, EvaluationReport
except ImportError:
    print("评测中心模块未找到")
    EvaluationTask, EvaluationMetric, EvaluationReport = None, None, None

try:
    from api_connector.models import APIProvider, APIConnection, APIModel, APIUsageLog
except ImportError:
    print("API连接器模块未找到")
    APIProvider, APIConnection, APIModel, APIUsageLog = None, None, None, None


def create_test_users():
    """创建测试用户"""
    try:
        # 创建超级用户
        admin, admin_created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if admin_created:
            admin.set_password('admin123456')
            admin.save()
            print('创建管理员用户成功')
        else:
            print('管理员用户已存在')

        # 创建普通测试用户
        user1, created = User.objects.get_or_create(
            username='test_user1',
            defaults={
                'email': 'test1@example.com',
                'is_staff': False
            }
        )
        if created:
            user1.set_password('password123')
            user1.save()
            print('创建测试用户1成功')
        else:
            print('测试用户1已存在')

        user2, created = User.objects.get_or_create(
            username='test_user2',
            defaults={
                'email': 'test2@example.com',
                'is_staff': False
            }
        )
        if created:
            user2.set_password('password123')
            user2.save()
            print('创建测试用户2成功')
        else:
            print('测试用户2已存在')
            
        return admin, user1, user2
    except Exception as e:
        print(f'创建测试用户失败: {e}')
        return None, None, None


def create_api_connector_data(users):
    """创建API连接器测试数据"""
    if APIProvider is None or APIConnection is None or APIModel is None or APIUsageLog is None:
        print("API连接器模块未找到，跳过创建")
        return [], [], [], []
    
    admin, user1, user2 = users
    
    # 创建API提供商
    providers_data = [
        {
            'name': 'OpenAI',
            'provider_type': 'openai',
            'description': 'OpenAI GPT系列模型提供商',
            'base_url': 'https://api.openai.com/v1/',
            'docs_url': 'https://platform.openai.com/docs/api-reference',
            'is_active': True
        },
        {
            'name': '百度智能云',
            'provider_type': 'baidu',
            'description': '百度文心一言API服务',
            'base_url': 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/',
            'docs_url': 'https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html',
            'is_active': True
        },
        {
            'name': 'Google AI',
            'provider_type': 'google',
            'description': 'Google Gemini模型服务',
            'base_url': 'https://generativelanguage.googleapis.com/v1/',
            'docs_url': 'https://developers.google.com/ai/docs',
            'is_active': True
        },
        {
            'name': 'Azure OpenAI',
            'provider_type': 'azure',
            'description': 'Microsoft Azure OpenAI服务',
            'base_url': 'https://your-resource.openai.azure.com/',
            'docs_url': 'https://docs.microsoft.com/en-us/azure/cognitive-services/openai/',
            'is_active': False
        }
    ]
    
    providers = []
    for provider_data in providers_data:
        try:
            provider, created = APIProvider.objects.get_or_create(
                name=provider_data['name'],
                defaults=provider_data
            )
            if created:
                print(f'创建API提供商 {provider.name} 成功')
            providers.append(provider)
        except Exception as e:
            print(f'创建API提供商 {provider_data["name"]} 失败: {e}')
    
    # 创建API连接
    connections = []
    for i, provider in enumerate(providers[:2]):  # 只为前两个提供商创建连接
        try:
            connection, created = APIConnection.objects.get_or_create(
                name=f'{provider.name}默认连接',
                provider=provider,
                defaults={
                    'api_key': f'sk-{uuid.uuid4().hex[:32]}',  # 模拟API密钥
                    'org_id': f'org-{uuid.uuid4().hex[:16]}' if provider.provider_type == 'openai' else None,
                    'custom_headers': {'User-Agent': 'BigModelApp/1.0'},
                    'custom_params': {'temperature': 0.7, 'max_tokens': 2000},
                    'rate_limit': 60,
                    'is_default': True,
                    'is_active': True
                }
            )
            if created:
                print(f'创建API连接 {connection.name} 成功')
            connections.append(connection)
        except Exception as e:
            print(f'创建API连接失败: {e}')
    
    # 创建API模型
    models_data = [
        # OpenAI模型
        {'provider_type': 'openai', 'name': 'GPT-4 Turbo', 'model_identifier': 'gpt-4-turbo-preview', 'model_type': 'chat', 'max_tokens': 128000},
        {'provider_type': 'openai', 'name': 'GPT-3.5 Turbo', 'model_identifier': 'gpt-3.5-turbo', 'model_type': 'chat', 'max_tokens': 16384},
        {'provider_type': 'openai', 'name': 'Text Embedding Ada 002', 'model_identifier': 'text-embedding-ada-002', 'model_type': 'embedding', 'max_tokens': 8192},
        # 百度模型
        {'provider_type': 'baidu', 'name': '文心一言', 'model_identifier': 'completions_pro', 'model_type': 'chat', 'max_tokens': 2000},
        {'provider_type': 'baidu', 'name': 'Embedding V1', 'model_identifier': 'embedding-v1', 'model_type': 'embedding', 'max_tokens': 512},
    ]
    
    api_models = []
    for model_data in models_data:
        provider = next((p for p in providers if p.provider_type == model_data['provider_type']), None)
        if provider:
            try:
                model, created = APIModel.objects.get_or_create(
                    name=model_data['name'],
                    provider=provider,
                    defaults={
                        'model_type': model_data['model_type'],
                        'model_identifier': model_data['model_identifier'],
                        'description': f'{model_data["name"]} - {provider.name}提供的{model_data["model_type"]}模型',
                        'max_tokens': model_data['max_tokens'],
                        'params_schema': {
                            'temperature': {'type': 'float', 'min': 0, 'max': 1, 'default': 0.7},
                            'max_tokens': {'type': 'int', 'min': 1, 'max': model_data['max_tokens'], 'default': 1000}
                        },
                        'is_default': model_data['model_type'] == 'chat' and 'GPT-4' in model_data['name'],
                        'is_active': True
                    }
                )
                if created:
                    print(f'创建API模型 {model.name} 成功')
                api_models.append(model)
            except Exception as e:
                print(f'创建API模型 {model_data["name"]} 失败: {e}')
    
    # 创建API使用日志
    usage_logs = []
    endpoints = ['/chat/completions', '/embeddings', '/completions', '/models']
    statuses = ['success', 'failed', 'rate_limited', 'error']
    
    for connection in connections:
        for i in range(20):  # 每个连接创建20条日志
            try:
                endpoint = random.choice(endpoints)
                status = random.choice(statuses)
                
                request_data = {
                    'model': random.choice([m.model_identifier for m in api_models if m.provider == connection.provider]),
                    'messages': [{'role': 'user', 'content': f'测试请求 {i+1}'}] if 'chat' in endpoint else None,
                    'prompt': f'测试提示 {i+1}' if 'completions' in endpoint and 'chat' not in endpoint else None,
                    'max_tokens': random.randint(100, 1000),
                    'temperature': round(random.uniform(0.1, 0.9), 2)
                }
                
                response_data = None
                error_message = None
                tokens_used = 0
                
                if status == 'success':
                    response_data = {
                        'id': f'chatcmpl-{uuid.uuid4().hex[:8]}',
                        'object': 'chat.completion' if 'chat' in endpoint else 'text_completion',
                        'created': int(timezone.now().timestamp()),
                        'choices': [{'text': f'这是测试响应 {i+1}', 'index': 0}],
                        'usage': {'prompt_tokens': random.randint(10, 100), 'completion_tokens': random.randint(20, 200)}
                    }
                    tokens_used = response_data['usage']['prompt_tokens'] + response_data['usage']['completion_tokens']
                elif status == 'failed':
                    error_message = '模型调用失败'
                elif status == 'rate_limited':
                    error_message = '超出API调用频率限制'
                elif status == 'error':
                    error_message = '网络连接错误'
                
                log = APIUsageLog.objects.create(
                    connection=connection,
                    endpoint=endpoint,
                    request_data=request_data,
                    response_data=response_data,
                    status=status,
                    error_message=error_message,
                    tokens_used=tokens_used,
                    response_time=round(random.uniform(100, 3000), 2),  # 100ms - 3s
                    user_ip=f'192.168.1.{random.randint(1, 255)}',
                    created_at=timezone.now() - timedelta(hours=random.randint(1, 24*7))  # 过去一周内
                )
                usage_logs.append(log)
            except Exception as e:
                print(f'创建API使用日志失败: {e}')
    
    print(f'创建API连接器测试数据完成: {len(providers)}个提供商, {len(connections)}个连接, {len(api_models)}个模型, {len(usage_logs)}条日志')
    return providers, connections, api_models, usage_logs


def create_dataset_formats():
    """创建数据集格式"""
    if DatasetFormat is None:
        return None, None, None
    
    try:
        csv_format, created = DatasetFormat.objects.get_or_create(
            name='CSV',
            defaults={'description': '逗号分隔值文件格式'}
        )
        if created:
            print('创建CSV数据集格式成功')
            
        json_format, created = DatasetFormat.objects.get_or_create(
            name='JSON',
            defaults={'description': 'JSON文件格式'}
        )
        if created:
            print('创建JSON数据集格式成功')
            
        txt_format, created = DatasetFormat.objects.get_or_create(
            name='TXT',
            defaults={'description': '纯文本文件格式'}
        )
        if created:
            print('创建TXT数据集格式成功')
            
        return csv_format, json_format, txt_format
    except Exception as e:
        print(f'创建数据集格式失败: {e}')
        return None, None, None


def create_datasets(users, formats):
    """创建测试数据集"""
    if Dataset is None:
        return []
    
    admin, user1, user2 = users
    csv_format, json_format, txt_format = formats
    
    dataset_names = ['金融数据集', '医疗数据集', '教育数据集', '客服对话集', '网络文章集']
    dataset_descriptions = [
        '包含股票、基金、债券等金融领域的结构化数据',
        '包含患者病历、诊断结果等医疗领域的数据',
        '包含学生成绩、课程评价等教育领域的数据',
        '包含客户服务对话、问题解决方案等数据',
        '包含网络文章、博客内容等非结构化数据'
    ]
    
    datasets = []
    for i in range(5):
        try:
            ds, created = Dataset.objects.get_or_create(
                name=dataset_names[i],
                defaults={
                    'description': dataset_descriptions[i],
                    'format': csv_format if i % 3 == 0 else (json_format if i % 3 == 1 else txt_format),
                    'size': 1024 * 1024 * (i + 1),  # 1MB到5MB不等
                    'created_by': admin if i % 3 == 0 else (user1 if i % 3 == 1 else user2),
                    'status': 'processed',
                    'file': f'datasets/dataset_{i+1}.zip',
                    'metadata': {'rows': 1000 * (i + 1), 'columns': 10 + i}
                }
            )
            if created:
                print(f'创建数据集 {dataset_names[i]} 成功')
            datasets.append(ds)
        except Exception as e:
            print(f'创建数据集 {dataset_names[i]} 失败: {e}')
    
    return datasets


def create_knowledge_bases(users):
    """创建测试知识库"""
    if KnowledgeBase is None or Chunk is None:
        return []
    
    admin, user1, user2 = users
    
    kb_names = ['金融知识库', '医疗知识库', '法律知识库', '技术文档库', '产品手册库']
    kb_descriptions = [
        '包含金融领域的专业知识、术语解释和案例分析',
        '包含医疗健康领域的专业知识、诊断指南和治疗方案',
        '包含法律法规、案例判例和法律解释',
        '包含各种技术文档、API说明和实施指南',
        '包含产品说明书、用户手册和常见问题解答'
    ]
    
    knowledge_bases = []
    for i in range(5):
        try:
            kb, created = KnowledgeBase.objects.get_or_create(
                name=kb_names[i],
                defaults={
                    'description': kb_descriptions[i],
                    'created_by': admin if i % 3 == 0 else (user1 if i % 3 == 1 else user2),
                    'config': {'embedding_model': 'text2vec', 'chunk_size': 1000, 'chunk_overlap': 200},
                    'status': 'active'
                }
            )
            
            if created:
                # 为每个知识库创建一些块
                for j in range(3):
                    Chunk.objects.create(
                        knowledge_base=kb,
                        content=f'这是{kb_names[i]}的第{j+1}个知识块，包含该领域的重要信息。',
                        metadata={'source': f'document_{i}_{j}.pdf', 'page': j+1}
                    )
                print(f'创建知识库 {kb_names[i]} 成功')
            knowledge_bases.append(kb)
        except Exception as e:
            print(f'创建知识库 {kb_names[i]} 失败: {e}')
    
    return knowledge_bases


def create_docker_images(users):
    """创建Docker镜像"""
    if DockerImage is None:
        return []
    
    admin, user1, user2 = users
    
    docker_names = ['Python基础镜像', 'PyTorch训练镜像', 'TensorFlow训练镜像', 'BERT微调镜像', 'GPT训练镜像']
    docker_tags = ['python:3.9', 'pytorch:1.10', 'tensorflow:2.8', 'bert:base', 'gpt:neo']
    docker_registries = ['docker.io', 'docker.io', 'docker.io', 'harbor.example.com', 'harbor.example.com']
    docker_descriptions = [
        'Python基础环境，包含常用的数据处理库',
        'PyTorch深度学习环境，适用于各类模型训练',
        'TensorFlow深度学习环境，适用于各类模型训练',
        'BERT预训练模型微调环境，适用于NLP任务',
        'GPT模型训练环境，适用于文本生成任务'
    ]
    
    # 如果DockerImage表中数据少于5条，则创建测试数据
    docker_images = []
    if DockerImage.objects.count() < 5:
        for i in range(5):
            try:
                docker_image, created = DockerImage.objects.get_or_create(
                    name=docker_names[i],
                    tag=docker_tags[i],
                    defaults={
                        'description': docker_descriptions[i],
                        'registry': docker_registries[i],
                        'created_by': admin if i % 3 == 0 else (user1 if i % 3 == 1 else user2),
                        'size': 1024 * 1024 * 100 * (i + 1)  # 100MB到500MB不等
                    }
                )
                if created:
                    print(f'创建Docker镜像 {docker_names[i]} 成功')
                docker_images.append(docker_image)
            except Exception as e:
                print(f'创建Docker镜像 {docker_names[i]} 失败: {e}')
    else:
        docker_images = list(DockerImage.objects.all()[:5])
    
    return docker_images


def create_models(users, datasets, docker_images):
    """创建模型"""
    if Model is None or TrainingJob is None:
        return []
    
    admin, user1, user2 = users
    
    model_names = ['金融文本分类模型', '医疗NER模型', '通用问答模型', '情感分析模型', '文本摘要模型']
    model_descriptions = [
        '基于BERT的金融文本分类模型，可识别文本所属的金融类别',
        '基于BiLSTM-CRF的医疗命名实体识别模型，提取医疗文本中的实体',
        '基于T5的通用问答模型，回答各类常见问题',
        '基于RoBERTa的情感分析模型，分析文本情感倾向',
        '基于BART的文本摘要模型，自动生成文章摘要'
    ]
    
    model_params = [
        {'learning_rate': 2e-5, 'batch_size': 16, 'epochs': 5},
        {'learning_rate': 1e-4, 'batch_size': 32, 'epochs': 10},
        {'learning_rate': 5e-5, 'batch_size': 8, 'epochs': 3},
        {'learning_rate': 3e-5, 'batch_size': 16, 'epochs': 4},
        {'learning_rate': 2e-5, 'batch_size': 4, 'epochs': 6}
    ]
    
    model_metrics = [
        {'accuracy': 0.92, 'f1': 0.91, 'precision': 0.90, 'recall': 0.92},
        {'f1': 0.85, 'precision': 0.83, 'recall': 0.87},
        {'bleu': 0.78, 'rouge-1': 0.72},
        {'accuracy': 0.94, 'f1': 0.93},
        {'rouge-1': 0.45, 'rouge-2': 0.22, 'rouge-l': 0.39}
    ]
    
    # 如果Model表中数据少于5条，则创建测试数据
    models = []
    if Model.objects.count() < 5:
        for i in range(5):
            try:
                model, created = Model.objects.get_or_create(
                    name=model_names[i],
                    defaults={
                        'description': model_descriptions[i],
                        'version': '1.0.0',
                        'status': 'trained' if i < 3 else 'training',
                        'parameters': model_params[i],
                        'metrics': model_metrics[i] if i < 3 else {},
                        'dataset': datasets[i] if i < len(datasets) else None,
                        'created_by': admin if i % 3 == 0 else (user1 if i % 3 == 1 else user2)
                    }
                )
                
                if created:
                    print(f'创建模型 {model_names[i]} 成功')
                    
                    # 为前3个已训练完成的模型创建训练任务
                    if i < 3 and docker_images:
                        TrainingJob.objects.create(
                            model=model,
                            docker_image=docker_images[i % len(docker_images)],
                            status='completed',
                            started_at=timezone.now() - timedelta(days=i+1, hours=i),
                            completed_at=timezone.now() - timedelta(days=i+1),
                            log='训练已完成，模型保存成功。\n最终loss: 0.0342\n准确率: 92.7%'
                        )
                        print(f'为模型 {model_names[i]} 创建训练任务成功')
                    
                    # 为后2个正在训练的模型创建训练任务
                    if i >= 3 and docker_images:
                        TrainingJob.objects.create(
                            model=model,
                            docker_image=docker_images[i % len(docker_images)],
                            status='running',
                            started_at=timezone.now() - timedelta(hours=i),
                            log='正在训练中...\n当前epoch: 3/6\n当前loss: 0.1245\n当前批次: 240/500'
                        )
                        print(f'为模型 {model_names[i]} 创建训练任务成功')
                
                models.append(model)
            except Exception as e:
                print(f'创建模型 {model_names[i]} 失败: {e}')
    else:
        models = list(Model.objects.all()[:5])
    
    return models


def create_plugins(users):
    """创建插件"""
    if Plugin is None:
        return []
    
    admin, user1, user2 = users
    
    plugin_names = ['数据预处理插件', '模型可视化插件', '数据增强插件', '模型监控插件', '结果导出插件']
    plugin_versions = ['1.2.0', '0.9.5', '1.0.0', '2.1.0', '0.8.3']
    plugin_descriptions = [
        '提供数据清洗、归一化、特征提取等预处理功能',
        '可视化模型结构、训练过程和预测结果',
        '通过同义词替换、回译等方式增强训练数据',
        '监控模型的性能、资源占用和预测质量',
        '将模型预测结果导出为多种格式'
    ]
    
    plugins = []
    if Plugin.objects.count() < 5:
        for i in range(5):
            try:
                plugin, created = Plugin.objects.get_or_create(
                    name=plugin_names[i],
                    version=plugin_versions[i],
                    defaults={
                        'description': plugin_descriptions[i],
                        'status': 'active' if i != 2 else 'inactive',
                        'entry_point': f'plugins.{plugin_names[i].lower().replace(" ", "_")}.main',
                        'file': f'plugins/{plugin_names[i].lower().replace(" ", "_")}_v{plugin_versions[i]}.zip',
                        'compatibility': {'models': ['all'], 'min_version': '0.5.0'},
                        'created_by': admin if i % 3 == 0 else (user1 if i % 3 == 1 else user2)
                    }
                )
                
                if created:
                    print(f'创建插件 {plugin_names[i]} 成功')
                plugins.append(plugin)
            except Exception as e:
                print(f'创建插件 {plugin_names[i]} 失败: {e}')
    else:
        plugins = list(Plugin.objects.all()[:5])
    
    return plugins


def create_applications(users, models, plugins):
    """创建应用"""
    if Application is None or ApplicationLog is None or ApplicationMetric is None:
        return []
    
    admin, user1, user2 = users
    
    app_names = ['金融文本分析服务', '医疗实体识别服务', '智能客服问答系统', '舆情监测分析系统', '文档摘要服务']
    app_descriptions = [
        '提供金融文本分类、关键信息提取等服务',
        '识别医疗文本中的疾病、症状、药物等实体',
        '基于大型语言模型的智能客服问答系统',
        '监测和分析社交媒体、新闻等渠道的舆情',
        '自动生成长文档的摘要，提取关键信息'
    ]
    
    applications = []
    if Application.objects.count() < 5 and models:
        for i in range(min(5, len(models))):
            try:
                status = 'running' if i < 3 else ('stopped' if i == 3 else 'created')
                app, created = Application.objects.get_or_create(
                    name=app_names[i],
                    defaults={
                        'description': app_descriptions[i],
                        'model': models[i],
                        'api_endpoint': f'/api/v1/apps/{uuid.uuid4()}' if status == 'running' else None,
                        'status': status,
                        'config': {
                            'max_concurrency': 10,
                            'timeout': 30,
                            'log_level': 'info',
                            'cache_size': 1024,
                            'batch_size': 16,
                            'environment': {'DEBUG': 'false', 'TIMEOUT': '30'}
                        },
                        'created_by': admin if i % 3 == 0 else (user1 if i % 3 == 1 else user2),
                        'deployed_at': timezone.now() - timedelta(days=5-i) if status == 'running' else None
                    }
                )
                
                if created:
                    # 添加插件
                    if plugins:
                        for j in range(min(3, len(plugins))):
                            if j % 2 == i % 2:  # 按一定规则选择插件，确保每个应用的插件不同
                                app.plugins.add(plugins[j])
                    
                    print(f'创建应用 {app_names[i]} 成功')
                    
                    # 为运行中的应用添加日志和指标
                    if status == 'running':
                        # 添加日志
                        log_levels = ['info', 'warning', 'error', 'debug']
                        log_messages = [
                            '应用启动成功',
                            '收到API请求，参数校验通过',
                            '处理请求完成，耗时125ms',
                            '返回响应，状态码200',
                            '检测到高负载，自动扩展资源',
                            '警告：请求队列积压超过阈值',
                            '错误：模型加载失败，重试中',
                            '调试：当前内存使用率75%'
                        ]
                        
                        for j in range(10):  # 每个应用添加10条日志
                            level = log_levels[j % 4]
                            message = log_messages[j % len(log_messages)]
                            if level == 'error':
                                message = '错误：' + message
                            elif level == 'warning':
                                message = '警告：' + message
                            
                            ApplicationLog.objects.create(
                                application=app,
                                level=level,
                                message=message,
                                timestamp=timezone.now() - timedelta(minutes=j*10)
                            )
                        
                        # 添加性能指标
                        for j in range(12):  # 12小时的监控数据
                            ApplicationMetric.objects.create(
                                application=app,
                                cpu_usage=20 + j % 30 + (i*5),  # 20%-80%不等
                                memory_usage=30 + j % 40 + (i*3),  # 30%-90%不等
                                total_requests=100 * (j+1) * (i+1),
                                avg_response_time=50 + j % 100,  # 50ms-150ms不等
                                error_rate=0.5 + (j % 10) / 100,  # 0.5%-1.5%不等
                                timestamp=timezone.now() - timedelta(hours=j)
                            )
                        
                        print(f'为应用 {app_names[i]} 添加日志和指标成功')
                
                applications.append(app)
            except Exception as e:
                print(f'创建应用 {app_names[i]} 失败: {e}')
    else:
        applications = list(Application.objects.all()[:5])
    
    return applications


def create_evaluation_tasks(users, models):
    """创建评测任务和报告"""
    if EvaluationTask is None or EvaluationReport is None:
        return
    
    admin, user1, user2 = users
    
    # 如果评测任务少于5个，则创建测试数据
    if EvaluationTask.objects.count() < 5 and models:
        for i in range(min(5, len(models))):
            try:
                status = 'completed' if i < 3 else ('running' if i == 3 else 'pending')
                task, created = EvaluationTask.objects.get_or_create(
                    name=f'{models[i].name}评测任务',
                    defaults={
                        'description': f'评测{models[i].name}在测试集上的性能',
                        'model': models[i],
                        'status': status,
                        'config': {
                            'test_data': f'test_data_{i+1}.jsonl',
                            'batch_size': 32,
                            'metrics': ['accuracy', 'f1_score', 'precision', 'recall']
                        },
                        'created_by': admin if i % 3 == 0 else (user1 if i % 3 == 1 else user2),
                        'start_time': timezone.now() - timedelta(days=i+1),
                        'end_time': timezone.now() - timedelta(days=i) if status == 'completed' else None
                    }
                )
                
                if created:
                    print(f'创建评测任务 {task.name} 成功')
                    
                    # 为已完成的评测任务创建报告
                    if status == 'completed':
                        report_results = {
                            'accuracy': round(0.8 + (i * 0.03), 2),
                            'f1_score': round(0.75 + (i * 0.04), 2), 
                            'precision': round(0.78 + (i * 0.03), 2),
                            'recall': round(0.77 + (i * 0.035), 2)
                        }
                        
                        EvaluationReport.objects.create(
                            task=task,
                            results=report_results,
                            summary=f'{models[i].name}在测试集上表现良好，各项指标均达到预期水平。',
                            created_at=timezone.now() - timedelta(days=i)
                        )
                        
                        print(f'为评测任务 {task.name} 创建报告成功')
            
            except Exception as e:
                print(f'创建评测任务 {models[i].name if i < len(models) else "未知"} 失败: {e}')


def create_training_jobs(models, docker_images):
    """创建训练任务"""
    if TrainingJob is None:
        return []
    
    job_statuses = ['pending', 'running', 'completed', 'failed', 'cancelled']
    
    # 检查是否已有训练任务
    try:
        existing_count = TrainingJob.objects.count()
    except Exception as e:
        print(f"训练任务数据库查询失败: {e}")
        existing_count = 0
    
    jobs = []
    if existing_count < 10:
        for i in range(10):
            try:
                status = job_statuses[i % len(job_statuses)]
                started_at = timezone.now() - timedelta(days=10-i, hours=random.randint(1, 5))
                completed_at = None
                
                if status in ['completed', 'failed', 'cancelled']:
                    completed_at = started_at + timedelta(hours=random.randint(1, 8))
                
                job = TrainingJob.objects.create(
                    model=models[i % len(models)],
                    docker_image=docker_images[i % len(docker_images)],
                    status=status,
                    log="训练日志内容...\n" + "log line\n" * 50,
                    started_at=started_at,
                    completed_at=completed_at,
                    created_by=models[i % len(models)].created_by
                )
                jobs.append(job)
                print(f'创建训练任务 {job.id} 成功')
            except Exception as e:
                print(f'创建训练任务失败: {e}')
    else:
        try:
            jobs = list(TrainingJob.objects.all()[:10])
            print(f'已存在 {len(jobs)} 个训练任务，跳过创建')
        except Exception as e:
            print(f'获取已存在训练任务失败: {e}')
            jobs = []
    
    return jobs


def main():
    """主函数"""
    print('开始创建测试数据...')
    
    # 创建测试用户
    users = create_test_users()
    
    # 创建数据集格式
    formats = create_dataset_formats()
    
    # 创建数据集
    datasets = create_datasets(users, formats)
    
    # 创建知识库
    knowledge_bases = create_knowledge_bases(users)
    
    # 创建Docker镜像
    docker_images = create_docker_images(users)
    
    # 创建模型
    models = create_models(users, datasets, docker_images)
    
    # 创建插件
    plugins = create_plugins(users)
    
    # 创建应用
    applications = create_applications(users, models, plugins)
    
    # 创建评测任务和报告
    create_evaluation_tasks(users, models)
    
    # 创建训练任务
    training_jobs = create_training_jobs(models, docker_images)
    
    # 创建API连接器测试数据
    api_connector_data = create_api_connector_data(users)
    
    print('测试数据创建完成！')


if __name__ == '__main__':
    main() 