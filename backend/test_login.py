#!/usr/bin/env python
"""
测试登录API的脚本
"""
import requests
import json

def test_login():
    """测试登录API"""
    # API端点
    url = 'http://localhost:5688/api/auth/login/'
    
    # 登录数据
    data = {
        'username': 'admin',
        'password': '123456'
    }
    
    try:
        print(f"发送登录请求到: {url}")
        print(f"请求数据: {data}")
        
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"登录成功!")
            print(f"Access Token: {result.get('access', 'N/A')}")
            print(f"Refresh Token: {result.get('refresh', 'N/A')}")
            return result
        else:
            print(f"登录失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"请求错误: {e}")
        return None

def test_protected_api(token):
    """测试需要认证的API"""
    if not token:
        print("没有token，跳过认证API测试")
        return
    
    # 测试数据中心API
    url = 'http://localhost:5688/api/data-center/datasets/'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"\n测试数据集API: {url}")
        response = requests.get(url, headers=headers)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"数据集数量: {len(result.get('results', result))}")
            print("API认证成功!")
        else:
            print(f"API请求失败: {response.text}")
            
    except Exception as e:
        print(f"API请求错误: {e}")

if __name__ == '__main__':
    # 测试登录
    login_result = test_login()
    
    if login_result:
        # 测试认证API
        access_token = login_result.get('access')
        test_protected_api(access_token) 