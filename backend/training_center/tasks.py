"""
训练中心应用的Celery任务
"""

import time
import random
from celery import shared_task
from django.utils import timezone
from .models import TrainingJob

@shared_task
def start_training_job(training_job_id):
    """
    启动训练任务的异步处理
    
    参数:
        training_job_id: 训练任务ID
    """
    try:
        # 获取训练任务
        training_job = TrainingJob.objects.get(id=training_job_id)
        
        # 更新任务状态为运行中
        training_job.status = 'running'
        training_job.started_at = timezone.now()
        training_job.save()
        
        # 记录日志
        training_job.log = f"{training_job.log or ''}[{timezone.now()}] 任务开始运行\n"
        training_job.save()
        
        # 模拟训练过程（实际应用中应该调用真实的训练代码）
        simulate_training(training_job)
        
        # 更新任务状态为已完成
        training_job.status = 'completed'
        training_job.completed_at = timezone.now()
        training_job.save()
        
        # 更新模型状态
        model = training_job.model
        model.status = 'completed'
        model.training_completed_at = timezone.now()
        
        # 生成随机性能指标（实际应用中应该使用真实的评估结果）
        model.metrics = {
            'accuracy': round(random.uniform(0.7, 0.99), 4),
            'loss': round(random.uniform(0.01, 0.3), 4),
            'f1_score': round(random.uniform(0.7, 0.99), 4),
            'training_time': (timezone.now() - training_job.started_at).total_seconds()
        }
        model.save()
        
        # 记录日志
        training_job.log = f"{training_job.log or ''}[{timezone.now()}] 任务完成\n"
        training_job.save()
        
    except TrainingJob.DoesNotExist:
        # 任务不存在，记录错误
        print(f"训练任务 {training_job_id} 不存在")
    except Exception as e:
        # 发生错误，更新任务状态
        try:
            training_job = TrainingJob.objects.get(id=training_job_id)
            training_job.status = 'failed'
            training_job.completed_at = timezone.now()
            training_job.log = f"{training_job.log or ''}[{timezone.now()}] 任务失败: {str(e)}\n"
            training_job.save()
            
            # 更新模型状态
            model = training_job.model
            model.status = 'failed'
            model.save()
        except:
            pass
        
        # 重新抛出异常
        raise

def simulate_training(training_job):
    """
    模拟训练过程
    
    参数:
        training_job: 训练任务对象
    """
    # 获取模型和参数
    model = training_job.model
    parameters = model.parameters
    
    # 记录参数
    log_message = f"[{timezone.now()}] 使用参数: {parameters}\n"
    training_job.log = f"{training_job.log or ''}{log_message}"
    training_job.save()
    
    # 模拟训练过程中的日志输出
    total_epochs = parameters.get('epochs', 10)
    for epoch in range(1, total_epochs + 1):
        # 模拟每个epoch的训练
        time.sleep(1)  # 模拟训练时间
        
        # 生成随机指标
        accuracy = round(0.5 + (epoch / total_epochs) * 0.4 + random.uniform(-0.05, 0.05), 4)
        loss = round(0.5 - (epoch / total_epochs) * 0.4 + random.uniform(-0.05, 0.05), 4)
        
        # 记录日志
        log_message = f"[{timezone.now()}] Epoch {epoch}/{total_epochs} - accuracy: {accuracy}, loss: {loss}\n"
        training_job.log = f"{training_job.log or ''}{log_message}"
        training_job.save()
        
        # 检查任务是否被取消
        training_job.refresh_from_db()
        if training_job.status == 'cancelled':
            log_message = f"[{timezone.now()}] 任务被取消\n"
            training_job.log = f"{training_job.log or ''}{log_message}"
            training_job.save()
            return 