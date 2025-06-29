"""
评测中心应用的Celery任务
"""

import time
import random
import json
from celery import shared_task
from django.utils import timezone
from .models import EvaluationTask, EvaluationReport, ModelComparison

@shared_task
def run_evaluation_task(task_id):
    """
    运行评测任务的异步处理
    
    参数:
        task_id: 评测任务ID
    """
    try:
        # 获取评测任务
        task = EvaluationTask.objects.get(id=task_id)
        
        # 模拟评测过程（实际应用中应该调用真实的评测代码）
        time.sleep(5)  # 模拟评测时间
        
        # 生成随机评测指标（实际应用中应该使用真实的评测结果）
        metrics = {
            'accuracy': round(random.uniform(0.7, 0.99), 4),
            'precision': round(random.uniform(0.7, 0.99), 4),
            'recall': round(random.uniform(0.7, 0.99), 4),
            'f1_score': round(random.uniform(0.7, 0.99), 4),
            'latency': round(random.uniform(10, 500), 2),
            'throughput': round(random.uniform(1, 100), 2)
        }
        
        # 更新任务状态和指标
        task.status = 'completed'
        task.metrics = metrics
        task.completed_at = timezone.now()
        task.save()
        
        # 生成评测报告
        generate_evaluation_report(task)
        
    except EvaluationTask.DoesNotExist:
        # 任务不存在，记录错误
        print(f"评测任务 {task_id} 不存在")
    except Exception as e:
        # 发生错误，更新任务状态
        try:
            task = EvaluationTask.objects.get(id=task_id)
            task.status = 'failed'
            task.completed_at = timezone.now()
            task.save()
        except:
            pass
        
        # 重新抛出异常
        raise

def generate_evaluation_report(task):
    """
    生成评测报告
    
    参数:
        task: 评测任务对象
    """
    # 生成报告摘要
    summary = f"模型 {task.model.name} v{task.model.version} 在数据集 {task.dataset.name} 上的评测结果"
    
    # 生成详细结果
    details = {
        'model_info': {
            'name': task.model.name,
            'version': task.model.version,
            'parameters': task.model.parameters
        },
        'dataset_info': {
            'name': task.dataset.name,
            'size': task.dataset.file_size
        },
        'metrics': task.metrics,
        'evaluation_parameters': task.parameters
    }
    
    # 生成图表数据
    charts = {
        'metrics_radar': {
            'categories': ['准确率', '精确率', '召回率', 'F1分数'],
            'values': [
                task.metrics.get('accuracy', 0),
                task.metrics.get('precision', 0),
                task.metrics.get('recall', 0),
                task.metrics.get('f1_score', 0)
            ]
        },
        'performance_bar': {
            'categories': ['延迟(ms)', '吞吐量(req/s)'],
            'values': [
                task.metrics.get('latency', 0),
                task.metrics.get('throughput', 0)
            ]
        }
    }
    
    # 生成改进建议
    suggestions = generate_suggestions(task.metrics)
    
    # 创建或更新评测报告
    try:
        report = task.report
        report.summary = summary
        report.details = details
        report.charts = charts
        report.suggestions = suggestions
        report.save()
    except EvaluationReport.DoesNotExist:
        EvaluationReport.objects.create(
            task=task,
            summary=summary,
            details=details,
            charts=charts,
            suggestions=suggestions
        )

def generate_suggestions(metrics):
    """
    根据评测指标生成改进建议
    
    参数:
        metrics: 评测指标字典
    
    返回:
        改进建议文本
    """
    suggestions = []
    
    # 根据准确率给出建议
    accuracy = metrics.get('accuracy', 0)
    if accuracy < 0.8:
        suggestions.append("模型准确率较低，建议增加训练数据量或优化模型结构。")
    elif accuracy < 0.9:
        suggestions.append("模型准确率一般，可以尝试调整超参数或使用更复杂的模型。")
    else:
        suggestions.append("模型准确率较高，可以考虑模型压缩或优化推理速度。")
    
    # 根据精确率和召回率给出建议
    precision = metrics.get('precision', 0)
    recall = metrics.get('recall', 0)
    if precision < recall and precision < 0.85:
        suggestions.append("模型精确率较低，建议调整决策阈值或增加负样本。")
    elif recall < precision and recall < 0.85:
        suggestions.append("模型召回率较低，建议调整决策阈值或增加正样本。")
    
    # 根据延迟给出建议
    latency = metrics.get('latency', 0)
    if latency > 200:
        suggestions.append("模型延迟较高，建议进行模型量化或蒸馏以提高推理速度。")
    
    return "\n".join(suggestions)

@shared_task
def generate_model_comparison(comparison_id):
    """
    生成模型比较的异步处理
    
    参数:
        comparison_id: 模型比较ID
    """
    try:
        # 获取模型比较
        comparison = ModelComparison.objects.get(id=comparison_id)
        
        # 获取所有模型
        models = comparison.models.all()
        
        # 模拟比较过程（实际应用中应该调用真实的比较代码）
        time.sleep(3)  # 模拟比较时间
        
        # 生成比较结果
        results = {
            'models': [],
            'metrics': ['accuracy', 'precision', 'recall', 'f1_score', 'latency', 'throughput'],
            'radar_chart': {
                'categories': ['准确率', '精确率', '召回率', 'F1分数'],
                'series': []
            },
            'bar_chart': {
                'categories': ['延迟(ms)', '吞吐量(req/s)'],
                'series': []
            }
        }
        
        # 为每个模型生成随机指标
        for model in models:
            # 生成随机指标
            metrics = {
                'accuracy': round(random.uniform(0.7, 0.99), 4),
                'precision': round(random.uniform(0.7, 0.99), 4),
                'recall': round(random.uniform(0.7, 0.99), 4),
                'f1_score': round(random.uniform(0.7, 0.99), 4),
                'latency': round(random.uniform(10, 500), 2),
                'throughput': round(random.uniform(1, 100), 2)
            }
            
            # 添加模型信息和指标
            results['models'].append({
                'id': model.id,
                'name': model.name,
                'version': model.version,
                'metrics': metrics
            })
            
            # 添加雷达图数据
            results['radar_chart']['series'].append({
                'name': f"{model.name} v{model.version}",
                'values': [
                    metrics['accuracy'],
                    metrics['precision'],
                    metrics['recall'],
                    metrics['f1_score']
                ]
            })
            
            # 添加柱状图数据
            results['bar_chart']['series'].append({
                'name': f"{model.name} v{model.version}",
                'values': [
                    metrics['latency'],
                    metrics['throughput']
                ]
            })
        
        # 更新比较结果
        comparison.results = results
        comparison.save()
        
    except ModelComparison.DoesNotExist:
        # 比较不存在，记录错误
        print(f"模型比较 {comparison_id} 不存在")
    except Exception as e:
        # 发生错误，记录错误
        print(f"生成模型比较时发生错误: {str(e)}")
        # 重新抛出异常
        raise 