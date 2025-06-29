#!/usr/bin/env python
"""
创建测试用户的脚本
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    """创建测试用户"""
    username = 'admin'
    password = '123456'
    email = 'admin@example.com'
    
    # 检查用户是否已存在
    if User.objects.filter(username=username).exists():
        print(f"用户 {username} 已存在")
        user = User.objects.get(username=username)
    else:
        # 创建新用户
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_staff=True,
            is_superuser=True
        )
        print(f"创建用户成功: {username}")
    
    print(f"用户名: {user.username}")
    print(f"邮箱: {user.email}")
    print(f"是否为管理员: {user.is_staff}")
    print(f"是否为超级用户: {user.is_superuser}")
    
    return user

if __name__ == '__main__':
    create_test_user() 