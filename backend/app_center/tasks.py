"""
应用中心应用的Celery任务
"""

import time
import random
from celery import shared_task
from django.utils import timezone
from .models import Application

@shared_task
def deploy_application(application_id):
    """
    部署应用的异步处理
    
    参数:
        application_id: 应用ID
    """
    try:
        # 获取应用
        application = Application.objects.get(id=application_id)
        
        # 模拟部署过程（实际应用中应该调用真实的部署代码）
        time.sleep(5)  # 模拟部署时间
        
        # 生成随机端点（实际应用中应该使用真实的端点）
        application.endpoint = f"https://api.example.com/models/{application.model.id}/predict"
        
        # 生成随机资源占用（实际应用中应该使用真实的资源占用）
        application.resource_usage = {
            'cpu': f"{random.uniform(5, 30):.1f}%",
            'memory': f"{random.uniform(100, 1000):.1f}MB",
            'gpu': f"{random.uniform(0, 80):.1f}%"
        }
        
        application.save()
        
    except Application.DoesNotExist:
        # 应用不存在，记录错误
        print(f"应用 {application_id} 不存在")
    except Exception as e:
        # 发生错误，更新应用状态
        try:
            application = Application.objects.get(id=application_id)
            application.status = 'error'
            application.save()
        except:
            pass
        
        # 重新抛出异常
        raise

@shared_task
def stop_application(application_id):
    """
    停止应用的异步处理
    
    参数:
        application_id: 应用ID
    """
    try:
        # 获取应用
        application = Application.objects.get(id=application_id)
        
        # 模拟停止过程（实际应用中应该调用真实的停止代码）
        time.sleep(2)  # 模拟停止时间
        
        # 清除端点和资源占用
        application.endpoint = None
        application.resource_usage = {}
        application.save()
        
    except Application.DoesNotExist:
        # 应用不存在，记录错误
        print(f"应用 {application_id} 不存在")
    except Exception as e:
        # 发生错误，更新应用状态
        try:
            application = Application.objects.get(id=application_id)
            application.status = 'error'
            application.save()
        except:
            pass
        
        # 重新抛出异常
        raise 