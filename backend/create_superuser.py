#!/usr/bin/env python
"""
创建默认的超级用户
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
sys.path.append('/opt/big_model_app/backend')

django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """创建默认的超级用户"""
    username = 'admin'
    password = 'admin123456@'
    email = 'admin@example.com'
    
    # 检查用户是否已存在
    if User.objects.filter(username=username).exists():
        print(f"✅ 超级用户 '{username}' 已存在")
        # 更新密码
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✅ 更新超级用户 '{username}' 的密码")
    else:
        # 创建新的超级用户
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ 创建超级用户 '{username}' 成功")
    
    print(f"用户名: {username}")
    print(f"密码: {password}")
    print(f"邮箱: {email}")

if __name__ == '__main__':
    create_superuser() 