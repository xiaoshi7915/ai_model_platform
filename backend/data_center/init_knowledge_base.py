#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
知识库测试数据初始化脚本
用于创建示例知识库数据
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
from data_center.models import KnowledgeBase, Dataset
from django.contrib.auth.models import User

# 示例文本内容
SAMPLE_TEXT_CONTENT = """
# 人工智能基础知识

## 什么是人工智能

人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，致力于创造能够模拟人类智能的机器。
人工智能系统通常具有感知环境、学习、推理和自主行动的能力。

## 人工智能的主要分支

1. **机器学习**：使计算机能够从数据中学习，而无需明确编程。
2. **深度学习**：基于人工神经网络的机器学习子集，可以处理非结构化数据。
3. **自然语言处理**：使计算机能够理解和生成人类语言。
4. **计算机视觉**：使计算机能够从图像或视频中获取高级信息。
5. **强化学习**：通过与环境的交互来学习最佳行为。

## 人工智能的应用

- 医疗诊断
- 自动驾驶汽车
- 推荐系统
- 智能助手
- 金融分析
- 游戏
- 安全监控

## 人工智能的未来发展

随着技术的进步，人工智能将继续发展并融入我们的日常生活。研究人员正在努力创造更通用、更具创造性的AI系统，
但同时也需要考虑伦理问题和负责任的AI发展。
"""

SAMPLE_QA_CONTENT = """
Q: 什么是大型语言模型？
A: 大型语言模型（Large Language Models，简称LLMs）是一种基于深度学习的自然语言处理模型，它们通过在海量文本数据上训练，学习了语言的规律和知识。这些模型通常包含数十亿甚至数千亿个参数，具有理解和生成人类语言的能力。代表模型包括GPT系列、Claude、LLaMA等。

Q: 机器学习和深度学习有什么区别？
A: 机器学习是人工智能的一个子领域，使计算机能够从数据中学习而无需明确编程。深度学习则是机器学习的一个子集，它使用多层神经网络来模拟人脑的工作方式，特别擅长处理非结构化数据如图像、音频和文本。深度学习需要大量数据和计算资源，但可以自动提取特征，而传统机器学习通常需要人工特征工程。

Q: 什么是迁移学习？
A: 迁移学习是机器学习的一种方法，它利用在一个任务上获得的知识来帮助学习另一个相关任务。这种方法特别适用于目标任务数据有限的情况。例如，可以使用在大规模图像数据集上预训练的模型，然后通过微调来适应特定领域的图像分类任务。

Q: 模型微调是什么意思？
A: 模型微调是指在预训练模型的基础上，使用特定领域的数据进行额外训练，使模型适应特定任务的过程。微调通常可以保留预训练模型学到的通用知识，同时使模型在特定领域表现更好。微调常用于自然语言处理和计算机视觉任务。

Q: 强化学习和监督学习有什么不同？
A: 监督学习使用带标签的数据来训练模型，模型学习输入和标签之间的映射关系。而强化学习则是通过与环境的交互和反馈来学习，模型（称为智能体）学习选择能够最大化未来奖励的动作。强化学习没有明确的正确答案，而是通过试错来优化策略。
"""

SAMPLE_STRUCTURED_CONTENT = """
{
  "concepts": [
    {
      "name": "人工智能",
      "definition": "人工智能是计算机科学的一个分支，研究如何创造模拟人类智能的机器。",
      "related": ["机器学习", "深度学习", "自然语言处理"]
    },
    {
      "name": "机器学习",
      "definition": "机器学习是人工智能的一个子领域，研究如何使计算机系统从数据中学习和改进。",
      "types": ["监督学习", "无监督学习", "半监督学习", "强化学习"],
      "related": ["深度学习", "神经网络", "决策树"]
    },
    {
      "name": "深度学习",
      "definition": "深度学习是机器学习的一个子集，使用多层神经网络进行特征提取和转换。",
      "applications": ["图像识别", "语音识别", "自然语言处理", "推荐系统"],
      "models": ["CNN", "RNN", "Transformer", "GAN"]
    },
    {
      "name": "自然语言处理",
      "definition": "自然语言处理是人工智能的一个分支，研究如何使计算机理解和生成人类语言。",
      "tasks": ["文本分类", "文本生成", "机器翻译", "情感分析", "命名实体识别"],
      "models": ["BERT", "GPT", "T5", "RoBERTa"]
    },
    {
      "name": "强化学习",
      "definition": "强化学习是一种机器学习方法，智能体通过与环境交互并获得反馈来学习最佳行为策略。",
      "algorithms": ["Q-Learning", "DQN", "PPO", "A3C"],
      "applications": ["游戏AI", "机器人控制", "自动驾驶", "推荐系统"]
    }
  ]
}
"""

def create_knowledge_bases():
    """创建测试知识库"""
    print("正在创建测试知识库...")
    
    # 知识库类型
    types = [
        ('text', '文本知识库', SAMPLE_TEXT_CONTENT),
        ('qa', '问答知识库', SAMPLE_QA_CONTENT),
        ('structured', '结构化知识库', SAMPLE_STRUCTURED_CONTENT)
    ]
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    # 获取数据集
    datasets = Dataset.objects.all()
    
    kb_list = []
    
    for i, (kb_type, type_name, content) in enumerate(types):
        name = f"{type_name}示例"
        kb, created = KnowledgeBase.objects.get_or_create(
            name=name,
            defaults={
                'description': f"这是一个{type_name}的示例，用于演示知识库功能。",
                'content': content,
                'type': kb_type,
                'is_public': True,
                'tags': '示例,AI,知识库',
                'has_vector_index': random.choice([True, False]),
                'created_by': admin_user,
            }
        )
        
        if created:
            print(f"  - 创建知识库: {name}")
            
            # 添加随机数据集关联
            if datasets.exists():
                related_datasets = random.sample(list(datasets), min(random.randint(1, 2), datasets.count()))
                for dataset in related_datasets:
                    kb.related_datasets.add(dataset)
                print(f"    - 关联数据集: {', '.join([ds.name for ds in related_datasets])}")
        
        kb_list.append(kb)
    
    return kb_list

def main():
    """主函数"""
    print("开始初始化知识库测试数据...")
    
    # 创建知识库
    kb_list = create_knowledge_bases()
    
    print("\n测试数据初始化完成！")
    print(f"创建了 {len(kb_list)} 个知识库")

if __name__ == "__main__":
    main() 