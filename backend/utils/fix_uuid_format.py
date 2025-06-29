#!/usr/bin/env python
"""
检查并修复数据库中的UUID格式问题
"""

import os
import sys
import django
import re
import uuid

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

# 导入模型
from app_center.models import Application, Plugin, ApplicationPlugin
from django.db import connection

def validate_and_convert_uuid(value):
    """
    验证并转换UUID
    如果值是有效的UUID，则返回字符串格式
    如果不是，则尝试转换或返回None
    """
    if not value:
        return None
        
    try:
        # 尝试直接转换
        uuid_obj = uuid.UUID(str(value))
        return str(uuid_obj)
    except (ValueError, AttributeError, TypeError):
        # 检查是否是格式不正确的UUID
        if isinstance(value, str):
            # 移除所有非字母数字字符
            clean_value = re.sub(r'[^a-zA-Z0-9]', '', value)
            if len(clean_value) == 32:
                # 尝试添加连字符
                formatted_uuid = f"{clean_value[:8]}-{clean_value[8:12]}-{clean_value[12:16]}-{clean_value[16:20]}-{clean_value[20:]}"
                try:
                    uuid_obj = uuid.UUID(formatted_uuid)
                    return str(uuid_obj)
                except ValueError:
                    pass
        return None

def fix_plugin_uuids():
    """修复插件表中的UUID问题"""
    print("检查并修复插件UUID...")
    
    # 获取插件数据库表名
    plugin_table = Plugin._meta.db_table
    
    # 直接使用SQL检查UUID格式
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id FROM {plugin_table}")
        rows = cursor.fetchall()
        
        fixed_count = 0
        for row in rows:
            plugin_id = row[0]
            try:
                # 检查是否是有效的UUID
                uuid.UUID(str(plugin_id))
            except (ValueError, TypeError):
                # 尝试修复UUID
                fixed_uuid = validate_and_convert_uuid(plugin_id)
                if fixed_uuid:
                    # 更新记录
                    try:
                        cursor.execute(f"UPDATE {plugin_table} SET id = %s WHERE id = %s", [fixed_uuid, plugin_id])
                        fixed_count += 1
                        print(f"  已修复插件UUID: {plugin_id} -> {fixed_uuid}")
                    except Exception as e:
                        print(f"  修复插件UUID失败: {plugin_id}, 错误: {str(e)}")
    
    print(f"插件UUID检查完成，已修复: {fixed_count}")

def fix_application_uuids():
    """修复应用表中的UUID问题"""
    print("检查并修复应用UUID...")
    
    # 获取应用数据库表名
    app_table = Application._meta.db_table
    
    # 直接使用SQL检查UUID格式
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id FROM {app_table}")
        rows = cursor.fetchall()
        
        fixed_count = 0
        for row in rows:
            app_id = row[0]
            try:
                # 检查是否是有效的UUID
                uuid.UUID(str(app_id))
            except (ValueError, TypeError):
                # 尝试修复UUID
                fixed_uuid = validate_and_convert_uuid(app_id)
                if fixed_uuid:
                    # 更新记录
                    try:
                        cursor.execute(f"UPDATE {app_table} SET id = %s WHERE id = %s", [fixed_uuid, app_id])
                        fixed_count += 1
                        print(f"  已修复应用UUID: {app_id} -> {fixed_uuid}")
                    except Exception as e:
                        print(f"  修复应用UUID失败: {app_id}, 错误: {str(e)}")
    
    print(f"应用UUID检查完成，已修复: {fixed_count}")

def fix_application_plugin_uuids():
    """修复应用插件关联表中的UUID问题"""
    print("检查并修复应用插件关联UUID...")
    
    # 获取应用插件关联数据库表名
    app_plugin_table = ApplicationPlugin._meta.db_table
    
    # 直接使用SQL检查UUID格式
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT application_id, plugin_id FROM {app_plugin_table}")
        rows = cursor.fetchall()
        
        fixed_count = 0
        for row in rows:
            app_id, plugin_id = row
            
            # 检查应用ID
            try:
                uuid.UUID(str(app_id))
                app_id_valid = True
            except (ValueError, TypeError):
                app_id_valid = False
                
            # 检查插件ID
            try:
                uuid.UUID(str(plugin_id))
                plugin_id_valid = True
            except (ValueError, TypeError):
                plugin_id_valid = False
            
            # 如果有无效ID，尝试修复
            if not app_id_valid or not plugin_id_valid:
                fixed_app_id = validate_and_convert_uuid(app_id) if not app_id_valid else app_id
                fixed_plugin_id = validate_and_convert_uuid(plugin_id) if not plugin_id_valid else plugin_id
                
                if fixed_app_id and fixed_plugin_id:
                    # 更新记录
                    try:
                        cursor.execute(
                            f"UPDATE {app_plugin_table} SET application_id = %s, plugin_id = %s WHERE application_id = %s AND plugin_id = %s", 
                            [fixed_app_id, fixed_plugin_id, app_id, plugin_id]
                        )
                        fixed_count += 1
                        print(f"  已修复应用插件关联: {app_id},{plugin_id} -> {fixed_app_id},{fixed_plugin_id}")
                    except Exception as e:
                        print(f"  修复应用插件关联失败: {app_id},{plugin_id}, 错误: {str(e)}")
    
    print(f"应用插件关联UUID检查完成，已修复: {fixed_count}")

def check_db_tables():
    """检查是否存在所有必要的数据库表"""
    print("检查数据库表结构...")
    
    required_tables = [
        'data_center_dataset',
        'data_center_knowledgebase',
        'training_center_model',
        'training_center_dockerimage',
        'training_center_trainingjob',
        'app_center_application',
        'app_center_plugin',
        'app_center_applicationplugin',
        'evaluation_center_evaluationtask',
        'evaluation_center_evaluationreport',
        'evaluation_center_modelcomparison'
    ]
    
    with connection.cursor() as cursor:
        # 获取所有表名
        if connection.vendor == 'postgresql':
            cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        elif connection.vendor == 'sqlite':
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        else:
            cursor.execute("SHOW TABLES;")
        
        existing_tables = [row[0] for row in cursor.fetchall()]
    
    # 检查缺失的表
    missing_tables = [table for table in required_tables if table not in existing_tables]
    
    if missing_tables:
        print("发现缺失的数据库表:")
        for table in missing_tables:
            print(f"  - {table}")
        
        print("\n请先运行数据库迁移命令:")
        print("python manage.py makemigrations")
        print("python manage.py migrate")
        return False
    
    print("数据库表结构检查通过")
    return True

def main():
    """主函数"""
    print("===== 开始修复UUID格式问题 =====")
    
    if not check_db_tables():
        print("数据库表结构检查失败，请先修复表结构")
        return
    
    fix_plugin_uuids()
    fix_application_uuids()
    fix_application_plugin_uuids()
    
    print("\n===== UUID格式问题修复完成 =====")

if __name__ == "__main__":
    main() 