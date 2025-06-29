"""
UUID格式处理辅助函数
"""

import uuid
import re
from django.db import connection

def is_valid_uuid(value):
    """
    检查输入是否是有效的UUID格式
    """
    try:
        uuid_obj = uuid.UUID(str(value))
        return True
    except (ValueError, AttributeError, TypeError):
        return False

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

def fix_database_uuids():
    """
    修复数据库中可能的UUID格式问题
    适用于SQLite数据库中的UUID存储格式错误
    """
    if connection.vendor != 'sqlite':
        # 只处理SQLite数据库
        return
        
    # 获取所有数据库表
    with connection.cursor() as cursor:
        # 获取所有使用UUID的表和字段
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            if table_name.startswith('sqlite_') or table_name.startswith('django_'):
                continue
                
            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            # 检查每一列
            for column in columns:
                column_name = column[1]
                # 如果字段名包含'id'或'uuid'，可能是UUID字段
                if ('id' in column_name.lower() or 'uuid' in column_name.lower()) and column_name != 'id':
                    try:
                        # 尝试修复该字段的UUID格式
                        cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE {column_name} IS NOT NULL")
                        rows = cursor.fetchall()
                        
                        for row in rows:
                            value = row[0]
                            if value and not is_valid_uuid(value):
                                fixed_uuid = validate_and_convert_uuid(value)
                                if fixed_uuid and fixed_uuid != value:
                                    cursor.execute(
                                        f"UPDATE {table_name} SET {column_name} = ? WHERE {column_name} = ?",
                                        [fixed_uuid, value]
                                    )
                    except Exception as e:
                        print(f"修复表 {table_name} 的 {column_name} 时出错: {str(e)}")

# 在Django启动时自动修复UUID
# 注意：这是一个临时解决方案，长期应该迁移到PostgreSQL
def auto_fix_uuids():
    try:
        fix_database_uuids()
    except Exception as e:
        print(f"自动修复UUID时出错: {str(e)}") 