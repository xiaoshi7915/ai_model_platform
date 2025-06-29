#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据中心测试数据初始化脚本
用于创建数据集的测试数据
"""

import os
import sys
import django
import random
import uuid
from datetime import datetime, timedelta
from django.utils import timezone

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

# 导入模型
from data_center.models import Dataset
from django.contrib.auth.models import User

def create_datasets():
    """创建数据集测试数据"""
    print("正在创建数据集测试数据...")
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    # 数据集模板
    dataset_templates = [
        # 文本类数据集
        ('通用对话语料库', '包含多领域的人机对话数据，适用于训练通用对话模型。类型: text, 领域: dialogue', 'text', 'dialogue'),
        ('电商评论数据集', '包含商品评论及情感标注，适用于情感分析模型训练。类型: text, 领域: sentiment', 'text', 'sentiment'),
        ('医疗文献摘要集', '医学文献的摘要和关键词，适用于医疗文本理解。类型: text, 领域: medical', 'text', 'medical'),
        ('法律文书数据集', '包含各类法律文书和判决书，适用于法律领域模型训练。类型: text, 领域: legal', 'text', 'legal'),
        ('金融新闻语料库', '金融领域新闻文章及分类，适用于金融文本分析。类型: text, 领域: finance', 'text', 'finance'),
        
        # 图像类数据集
        ('通用物体识别数据集', '包含日常物体的图像及标注，适用于物体识别模型训练。类型: image, 领域: object_detection', 'image', 'object_detection'),
        ('医疗影像数据集', '各类医疗影像及诊断标注，适用于医疗图像分析。类型: image, 领域: medical', 'image', 'medical'),
        ('人脸识别基准集', '不同角度和光照条件下的人脸图像，适用于人脸识别。类型: image, 领域: facial_recognition', 'image', 'facial_recognition'),
        
        # 多模态数据集
        ('图文匹配数据集', '图像及对应的文本描述，适用于图文匹配模型。类型: multimodal, 领域: image_text', 'multimodal', 'image_text'),
        ('视频字幕数据集', '视频片段及对应的字幕文本，适用于视频理解。类型: multimodal, 领域: video_text', 'multimodal', 'video_text'),
        
        # 结构化数据集
        ('用户行为分析数据', '用户行为日志及标签，适用于推荐系统。类型: structured, 领域: user_behavior', 'structured', 'user_behavior'),
        ('金融交易记录集', '金融交易数据及风险标记，适用于金融风控。类型: structured, 领域: finance', 'structured', 'finance')
    ]
    
    datasets_created = []
    
    for name, desc, data_type, domain in dataset_templates:
        # 随机生成文件大小和行数
        file_size = random.randint(50, 1000) * 1024 * 1024  # MB转字节
        rows_count = random.randint(1000, 100000)
        columns_count = random.randint(5, 50)
        
        # 随机创建和更新时间
        created_at = timezone.now() - timedelta(days=random.randint(30, 365))
        updated_at = created_at + timedelta(days=random.randint(1, 30))
        
        # 随机格式
        formats = {
            'text': ['csv', 'json', 'txt', 'jsonl'],
            'image': ['jpg', 'png', 'zip', 'tar.gz'],
            'multimodal': ['zip', 'tar.gz', 'jsonl'],
            'structured': ['csv', 'json', 'parquet', 'sql']
        }
        file_format = random.choice(formats.get(data_type, ['csv', 'json']))
        
        # 构建特征描述
        features_description = ""
        
        if data_type == 'text':
            avg_length = random.randint(50, 5000)
            languages = random.sample(['中文', '英文', '日文', '法文', '德文'], k=random.randint(1, 3))
            preprocessing = random.sample(['tokenization', 'stemming', 'lemmatization', 'stop_words_removal'], k=random.randint(1, 3))
            features_description = f"\n平均长度: {avg_length} 字符\n语言: {', '.join(languages)}\n预处理: {', '.join(preprocessing)}"
        elif data_type == 'image':
            resolution = f"{random.choice([640, 800, 1024, 1280])}x{random.choice([480, 600, 768, 1024])}"
            color = random.choice(['RGB', 'grayscale', 'RGBA'])
            annotation = random.choice(['bounding_box', 'segmentation', 'keypoints', 'classification'])
            features_description = f"\n分辨率: {resolution}\n颜色模式: {color}\n标注类型: {annotation}"
        elif data_type == 'multimodal':
            modalities = random.sample(['text', 'image', 'audio', 'video'], k=random.randint(2, 3))
            alignment = random.choice(['paired', 'weakly_paired', 'unpaired'])
            languages = random.sample(['中文', '英文', '日文'], k=random.randint(1, 2))
            features_description = f"\n模态: {', '.join(modalities)}\n对齐类型: {alignment}\n语言: {', '.join(languages)}"
        elif data_type == 'structured':
            fields = random.randint(5, 50)
            types = random.sample(['integer', 'float', 'string', 'boolean', 'timestamp'], k=random.randint(3, 5))
            missing = random.choice([True, False])
            time_series = random.choice([True, False])
            features_description = f"\n字段数: {fields}\n数据类型: {', '.join(types)}\n包含缺失值: {'是' if missing else '否'}\n时间序列: {'是' if time_series else '否'}"
        
        # 合并描述和特征
        full_description = desc + features_description
        
        # 构建标签
        tags = f"{data_type},{domain},{file_format}"
        
        # 随机状态
        status = random.choice(['pending', 'processing', 'ready', 'error'])
        status_message = ""
        if status == 'error':
            status_message = random.choice([
                "文件格式错误",
                "处理超时",
                "数据不完整",
                "解析失败"
            ])
        
        # 创建数据集
        dataset, created = Dataset.objects.get_or_create(
            name=name,
            defaults={
                'description': full_description,
                'file_format': file_format,
                'file_size': file_size,
                'rows_count': rows_count,
                'columns_count': columns_count,
                'status': status,
                'status_message': status_message,
                'is_public': random.choice([True, False]),
                'tags': tags,
                'created_by': admin_user,
                'created_at': created_at,
                'updated_at': updated_at
            }
        )
        
        if created:
            print(f"  - 创建数据集: {name} ({data_type}/{domain})")
            print(f"    大小: {file_size/(1024*1024):.2f} MB, 行数: {rows_count}")
            datasets_created.append(dataset)
    
    return datasets_created

def main():
    """主函数"""
    print("开始初始化数据中心测试数据...")
    
    # 创建数据集
    datasets = create_datasets()
    
    print("\n测试数据初始化完成！")
    print(f"创建了 {len(datasets)} 个数据集")

if __name__ == "__main__":
    main() 