import django
import os
import sys
from datetime import datetime, timedelta
import random

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

from django.contrib.auth.models import User
from evaluation_center.models import EvaluationTask, EvaluationReport
from training_center.models import Model
from data_center.models import Dataset

def create_evaluation_data():
    try:
        # 获取管理员用户
        admin_user = User.objects.get(username='admin')
        print(f"找到管理员用户: {admin_user.username}")
        
        # 获取现有的模型和数据集
        models = list(Model.objects.all())
        datasets = list(Dataset.objects.all())
        
        if not models:
            print("❌ 没有找到模型，请先创建模型数据")
            return
            
        if not datasets:
            print("❌ 没有找到数据集，请先创建数据集数据")
            return
        
        print(f"找到 {len(models)} 个模型和 {len(datasets)} 个数据集")
        
        # 创建评测任务
        evaluation_tasks_data = [
            {
                'name': 'BERT模型文本分类评测',
                'description': '评测BERT模型在中文文本分类任务上的性能',
                'model': models[0] if models else None,
                'dataset': datasets[0] if datasets else None,
                'status': 'completed',
                'metrics': ['accuracy', 'precision', 'recall', 'f1'],
                'parameters': {
                    'temperature': 0.7,
                    'max_length': 512,
                    'batch_size': 16
                },
                'created_by': admin_user
            },
            {
                'name': 'GPT-2对话生成评测',
                'description': '评测GPT-2模型在对话生成任务上的表现',
                'model': models[1] if len(models) > 1 else models[0],
                'dataset': datasets[1] if len(datasets) > 1 else datasets[0],
                'status': 'running',
                'metrics': ['bleu', 'rouge'],
                'parameters': {
                    'temperature': 0.8,
                    'max_length': 1024,
                    'batch_size': 8
                },
                'created_by': admin_user
            },
            {
                'name': '情感分析模型评测',
                'description': '评测情感分析模型的准确性和稳定性',
                'model': models[2] if len(models) > 2 else models[0],
                'dataset': datasets[2] if len(datasets) > 2 else datasets[0],
                'status': 'completed',
                'metrics': ['accuracy', 'f1', 'auc'],
                'parameters': {
                    'temperature': 0.5,
                    'max_length': 256,
                    'batch_size': 32
                },
                'created_by': admin_user
            },
            {
                'name': '多模型性能对比评测',
                'description': '对比多个模型在同一数据集上的性能表现',
                'model': models[0],
                'dataset': datasets[0],
                'status': 'pending',
                'metrics': ['accuracy', 'precision', 'recall', 'f1', 'auc'],
                'parameters': {
                    'temperature': 0.7,
                    'max_length': 512,
                    'batch_size': 16
                },
                'created_by': admin_user
            }
        ]
        
        created_tasks = []
        for task_data in evaluation_tasks_data:
            task, created = EvaluationTask.objects.get_or_create(
                name=task_data['name'],
                created_by=admin_user,
                defaults=task_data
            )
            if created:
                created_tasks.append(task)
                print(f"✅ 创建评测任务: {task.name}")
        
        # 为已完成的任务创建评测报告
        completed_tasks = EvaluationTask.objects.filter(status='completed')
        
        for task in completed_tasks:
            # 检查是否已经有报告
            if hasattr(task, 'report'):
                continue
                
            # 生成模拟的评测结果
            report_data = generate_mock_report_data(task)
            
            report = EvaluationReport.objects.create(
                task=task,
                summary=report_data['summary'],
                details=report_data['details'],
                charts=report_data['charts'],
                suggestions=report_data['suggestions']
            )
            print(f"✅ 创建评测报告: {task.name} 的评测报告")
        
        print(f"\n✅ 评测中心数据创建完成！")
        print(f"- 评测任务: {EvaluationTask.objects.count()} 个")
        print(f"- 评测报告: {EvaluationReport.objects.count()} 个")
        
    except User.DoesNotExist:
        print("❌ 管理员用户不存在，请先创建admin用户")
    except Exception as e:
        print(f"❌ 创建评测数据失败: {e}")
        import traceback
        traceback.print_exc()

def generate_mock_report_data(task):
    """生成模拟的评测报告数据"""
    
    # 根据任务的指标生成模拟结果
    details = {}
    for metric in task.metrics:
        if metric == 'accuracy':
            details[metric] = {
                'value': round(random.uniform(0.85, 0.95), 4),
                'description': '模型预测正确的样本比例'
            }
        elif metric == 'precision':
            details[metric] = {
                'value': round(random.uniform(0.80, 0.92), 4),
                'description': '预测为正例中实际为正例的比例'
            }
        elif metric == 'recall':
            details[metric] = {
                'value': round(random.uniform(0.82, 0.94), 4),
                'description': '实际正例中被正确预测的比例'
            }
        elif metric == 'f1':
            details[metric] = {
                'value': round(random.uniform(0.83, 0.93), 4),
                'description': '精确率和召回率的调和平均值'
            }
        elif metric == 'bleu':
            details[metric] = {
                'value': round(random.uniform(0.25, 0.45), 4),
                'description': '生成文本与参考文本的相似度'
            }
        elif metric == 'rouge':
            details[metric] = {
                'value': round(random.uniform(0.30, 0.50), 4),
                'description': '生成摘要与参考摘要的相似度'
            }
        elif metric == 'auc':
            details[metric] = {
                'value': round(random.uniform(0.88, 0.96), 4),
                'description': 'ROC曲线下的面积'
            }
    
    # 生成图表数据
    charts = {
        'metrics_radar': {
            'categories': list(details.keys()),
            'values': [details[metric]['value'] for metric in details.keys()]
        },
        'performance_bar': {
            'categories': list(details.keys()),
            'values': [details[metric]['value'] for metric in details.keys()]
        }
    }
    
    # 生成摘要
    best_metric = max(details.keys(), key=lambda k: details[k]['value'])
    best_value = details[best_metric]['value']
    
    summary = f"模型在{task.dataset.name}上的评测已完成。最佳指标为{best_metric}，得分{best_value}。整体性能表现良好，达到了预期的评测标准。"
    
    # 生成建议
    suggestions = "建议继续优化模型参数，特别是在低分指标方面。可以考虑增加训练数据量或调整模型架构以进一步提升性能。"
    
    return {
        'summary': summary,
        'details': details,
        'charts': charts,
        'suggestions': suggestions
    }

if __name__ == '__main__':
    create_evaluation_data()

