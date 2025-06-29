#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库连接检查工具
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def check_db_connection():
    """检查数据库连接"""
    print("开始检查数据库连接...")
    
    # 获取数据库配置
    db_engine = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')
    
    if db_engine == 'django.db.backends.postgresql':
        # PostgreSQL数据库
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'ai_model_app')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', '')
        
        try:
            print(f"尝试连接PostgreSQL数据库: {db_host}:{db_port}/{db_name}")
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_password
            )
            cursor = conn.cursor()
            # 执行一个简单的查询
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"数据库连接成功! PostgreSQL版本: {version[0]}")
            
            # 检查pgvector扩展
            try:
                cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
                if cursor.fetchone():
                    print("pgvector扩展已安装")
                else:
                    print("警告: pgvector扩展未安装，请安装该扩展以支持向量搜索功能")
            except Exception as e:
                print(f"检查pgvector扩展失败: {e}")
            
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"连接PostgreSQL数据库失败: {e}")
            return False
    else:
        # SQLite数据库
        db_path = os.getenv('DB_NAME', 'db.sqlite3')
        print(f"使用SQLite数据库: {db_path}")
        if os.path.exists(db_path):
            print("数据库文件存在")
            return True
        else:
            print(f"警告: 数据库文件不存在: {db_path}")
            return False

if __name__ == "__main__":
    if check_db_connection():
        print("数据库连接检查通过")
        sys.exit(0)
    else:
        print("数据库连接检查失败")
        sys.exit(1)
