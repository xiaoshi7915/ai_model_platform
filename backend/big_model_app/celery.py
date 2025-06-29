"""
Celery配置文件
"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置Django设置模块的默认值
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')

app = Celery('big_model_app')

# 使用字符串表示，这样worker不必序列化配置对象
app.config_from_object('django.conf:settings', namespace='CELERY')

# 从所有已注册的Django应用中加载任务模块
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    """调试任务，打印请求信息"""
    print(f'Request: {self.request!r}') 