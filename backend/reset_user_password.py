#!/usr/bin/env python
"""
重置用户密码的脚本
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

from django.contrib.auth.models import User

def reset_password():
    """重置用户密码"""
    username = 'admin'
    new_password = '123456'
    
    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        print(f"用户 {username} 的密码已重置为: {new_password}")
        
        # 验证密码
        if user.check_password(new_password):
            print("密码验证成功!")
        else:
            print("密码验证失败!")
            
    except User.DoesNotExist:
        print(f"用户 {username} 不存在")

if __name__ == '__main__':
    reset_password() 