import os
import django

# 首先设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api_connector.models import APIProvider, APIConnection, APIUsageLog

def test_api():
    # 创建一个测试客户端
    client = APIClient()
    
    # 检查是否已有超级用户
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123456@')
    
    # 使用超级用户登录
    client.login(username='admin', password='admin123456@')
    
    # 测试API提供商列表
    response = client.get('/api/v1/api-connector/providers/')
    print("\n=== API提供商列表 ===")
    print("状态码:", response.status_code)
    print("数据:", response.data if hasattr(response, 'data') else response.content)
    
    # 测试API连接列表
    response = client.get('/api/v1/api-connector/connections/')
    print("\n=== API连接列表 ===")
    print("状态码:", response.status_code)
    print("数据:", response.data if hasattr(response, 'data') else response.content)
    
    # 测试API使用日志统计
    response = client.get('/api/v1/api-connector/logs/statistics/?period=week')
    print("\n=== API使用日志统计 ===")
    print("状态码:", response.status_code)
    print("数据:", response.data if hasattr(response, 'data') else response.content)
    
    # 打印总结信息
    print("\n=== 数据统计 ===")
    print(f"API提供商数量: {APIProvider.objects.count()}")
    print(f"API连接数量: {APIConnection.objects.count()}")
    print(f"API使用日志数量: {APIUsageLog.objects.count()}")

if __name__ == '__main__':
    test_api() 