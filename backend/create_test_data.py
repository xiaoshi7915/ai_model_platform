import os
import django

# 首先设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

# 然后导入模型
from api_connector.models import APIProvider, APIConnection, APIUsageLog
import uuid
from datetime import datetime, timedelta
import random

def create_test_data():
    # 检查是否已有数据
    if APIProvider.objects.exists():
        print('已存在数据，清除旧数据...')
        APIProvider.objects.all().delete()
    
    # 创建API提供商
    openai_provider = APIProvider.objects.create(
        name='OpenAI',
        provider_type='openai',
        description='OpenAI API服务提供商',
        base_url='https://api.openai.com/v1/'
    )

    baidu_provider = APIProvider.objects.create(
        name='百度智能云',
        provider_type='baidu',
        description='百度智能云API服务提供商',
        base_url='https://aip.baidubce.com/'
    )

    # 创建API连接
    openai_conn = APIConnection.objects.create(
        name='OpenAI测试连接',
        provider=openai_provider,
        api_key='sk-test123456',
        is_default=True
    )

    baidu_conn = APIConnection.objects.create(
        name='百度智能云测试连接',
        provider=baidu_provider,
        api_key='testkey',
        api_secret='testsecret',
        is_default=True
    )

    # 创建一些使用日志
    for i in range(10):
        day_offset = random.randint(0, 6)
        date = datetime.now() - timedelta(days=day_offset)
        status = random.choice(['success', 'failed'])
        
        APIUsageLog.objects.create(
            connection=openai_conn if i % 2 == 0 else baidu_conn,
            endpoint='/completions' if i % 2 == 0 else '/chat/completions',
            status=status,
            tokens_used=random.randint(100, 3000),
            response_time=random.randint(200, 2000),
            created_at=date
        )

    print('创建完成! 共创建了2个API提供商, 2个API连接和10条使用日志')

if __name__ == '__main__':
    create_test_data() 