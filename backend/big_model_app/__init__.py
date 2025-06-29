"""
大型模型构建管理平台
"""

# 设置默认应用配置
default_app_config = 'big_model_app.apps.BigModelAppConfig'

# 设置Celery应用
from .celery import app as celery_app

__all__ = ['celery_app'] 