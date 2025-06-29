#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
应用中心测试数据初始化脚本
用于创建应用程序和插件的测试数据
"""

import os
import sys
import django
import random
import json
import uuid
from datetime import datetime, timedelta
from django.utils import timezone

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

# 导入模型
from app_center.models import Application, Plugin, ApplicationPlugin, ApplicationLog, ApplicationMetric
from training_center.models import Model
from django.contrib.auth.models import User

def create_plugins():
    """创建插件测试数据"""
    print("正在创建插件测试数据...")
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    # 插件模板
    plugin_templates = [
        # 数据处理插件
        ('数据清洗', '1.0.0', '用于文本数据的预处理、清洗和规范化'),
        ('数据增强', '2.1.0', '通过各种方法丰富和扩展输入数据'),
        ('语言检测', '1.2.3', '自动检测输入文本的语言类型'),
        
        # 模型适配插件
        ('Token优化', '0.9.5', '优化Token使用，降低API调用成本'),
        ('模型路由', '1.5.2', '根据查询自动选择最合适的模型'),
        ('上下文管理', '2.0.1', '优化大模型上下文窗口的使用'),
        
        # 工具功能插件
        ('网页抓取', '1.0.0', '从指定URL提取网页内容'),
        ('搜索引擎', '2.3.1', '接入搜索引擎获取实时信息'),
        ('代码执行', '0.8.5', '安全地执行用户提供的代码'),
        ('文件处理', '1.4.2', '处理各种格式的文件内容'),
        
        # 安全相关插件
        ('敏感内容过滤', '3.1.0', '过滤有害、敏感或不当内容'),
        ('用户认证', '2.0.0', '提供多种用户认证和授权方式'),
        ('输入验证', '1.1.0', '验证和清理用户输入，防止注入攻击'),
        
        # 性能优化插件
        ('缓存管理', '2.2.1', '智能缓存常用查询结果'),
        ('批处理', '1.0.3', '合并多个请求进行批量处理'),
        ('响应压缩', '0.9.1', '压缩API响应数据减少传输量'),
        
        # 集成插件
        ('知识库连接', '1.3.0', '连接到外部知识库或文档系统'),
        ('数据库接口', '2.0.0', '连接各种关系型和非关系型数据库'),
        ('API网关', '1.5.0', '统一管理和路由外部API调用'),
        
        # 监控与分析插件
        ('用户反馈', '1.0.2', '收集和分析用户反馈信息'),
        ('性能监控', '2.1.0', '监控应用性能和资源使用情况'),
        ('用量统计', '1.4.1', '统计API调用次数和资源消耗')
    ]
    
    plugins_created = []
    
    for name, version, description in plugin_templates:
        # 随机状态
        status = random.choice(['active', 'inactive', 'deprecated'])
        
        # 随机创建和更新时间
        created_at = timezone.now() - timedelta(days=random.randint(1, 180))
        updated_at = created_at + timedelta(days=random.randint(1, 30))
        
        # 创建插件
        plugin, created = Plugin.objects.get_or_create(
            name=name,
            version=version,
            defaults={
                'description': description,
                'status': status,
                'created_by': admin_user,
                'created_at': created_at,
                'updated_at': updated_at
            }
        )
        
        if created:
            print(f"  - 创建插件: {name} {version} ")
            print(f"    状态: {status}")
            plugins_created.append(plugin)
    
    return plugins_created

def create_applications():
    """创建应用程序测试数据"""
    print("\n正在创建应用程序测试数据...")
    
    # 获取或创建管理员用户
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
    )
    
    # 获取已有模型，如果没有，则创建一个默认模型
    models = list(Model.objects.filter(status='deployed'))
    if not models:
        print("  未找到已部署的模型，创建默认模型...")
        default_model, _ = Model.objects.get_or_create(
            name="默认大语言模型",
            version="v1.0",
            defaults={
                'description': "用于演示的默认大语言模型",
                'created_by': admin_user,
                'created_at': timezone.now() - timedelta(days=30),
                'updated_at': timezone.now() - timedelta(days=15)
            }
        )
        models = [default_model]
    
    # 应用程序模板
    app_templates = [
        # 通用对话类应用
        ('智能助手', '通用型智能对话助手，可回答各种问题和执行简单任务', 'general-assistant', 'api'),
        ('客服机器人', '用于自动回答客户咨询的客服机器人', 'customer-service', 'api'),
        ('面试助手', '协助HR进行初步面试筛选的智能系统', 'hr-assistant', 'api'),
        
        # 内容生成类应用
        ('文章创作', '根据主题和提示生成高质量文章内容', 'content-creation', 'web'),
        ('代码助手', '辅助程序员编写、调试和优化代码', 'code-assistant', 'api'),
        ('广告文案', '生成针对特定产品和受众的广告文案', 'advertising', 'api'),
        ('邮件助手', '帮助起草和优化各类商务邮件', 'email-assistant', 'web'),
        
        # 内容分析类应用
        ('情感分析', '分析文本内容的情感倾向和强度', 'sentiment-analysis', 'api'),
        ('文档摘要', '自动总结长文档的要点和关键信息', 'summarization', 'web'),
        ('数据分析', '解读数据并生成见解和报告', 'data-analysis', 'api'),
        
        # 行业特定应用
        ('医疗问答', '回答医疗健康相关问题的专业系统', 'healthcare', 'web'),
        ('法律助手', '提供法律咨询和文档起草帮助', 'legal', 'api'),
        ('金融分析', '分析财经新闻和市场趋势', 'finance', 'web'),
        ('教育辅导', '针对学生问题提供解答和辅导', 'education', 'web'),
        
        # 多模态应用
        ('图像描述', '为上传的图像生成详细描述', 'image-description', 'api'),
        ('商品识别', '识别图片中的商品并提供相关信息', 'product-recognition', 'api'),
    ]
    
    applications_created = []
    plugins = list(Plugin.objects.filter(status='active'))
    
    for name, description, domain, app_type in app_templates:
        # 随机选择模型
        model = random.choice(models)
        
        # 随机状态
        status = random.choice(['draft', 'running', 'stopped', 'error'])
        
        # 随机创建和更新时间
        created_at = timezone.now() - timedelta(days=random.randint(1, 90))
        updated_at = created_at + timedelta(days=random.randint(1, 30))
        
        # 随机生成配置
        config = {
            'max_concurrency': random.choice([1, 2, 4, 8, 16, 32]),
            'timeout': random.choice([10, 30, 60, 120, 300]),
            'log_level': random.choice(['debug', 'info', 'warning', 'error']),
            'cache_size': random.choice([0, 100, 500, 1000, 5000]),
            'batch_size': random.choice([1, 2, 4, 8, 16]),
        }
        
        # 随机环境变量
        if random.choice([True, False]):
            config['env_vars'] = {
                'API_KEY': f'sk-{uuid.uuid4().hex[:24]}',
                'DEBUG': random.choice(['true', 'false']),
                'LOG_PATH': '/var/log/app/',
                'MAX_TOKENS': str(random.choice([1024, 2048, 4096, 8192])),
            }
        
        # 创建应用程序
        endpoint = f"/api/v1/{name.lower().replace(' ', '-')}"
        
        application, created = Application.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'api_endpoint': endpoint,
                'model': model,
                'status': status,
                'config': config,
                'created_by': admin_user,
                'created_at': created_at,
                'updated_at': updated_at
            }
        )
        
        if created:
            print(f"  - 创建应用: {name} ({domain})")
            print(f"    状态: {status}, 模型: {model.name} {model.version}")
            print(f"    端点: {endpoint}")
            applications_created.append(application)
            
            # 为应用添加随机插件
            if plugins:
                num_plugins = random.randint(0, min(5, len(plugins)))
                selected_plugins = random.sample(plugins, num_plugins)
                
                for plugin in selected_plugins:
                    app_plugin, plugin_created = ApplicationPlugin.objects.get_or_create(
                        application=application,
                        plugin=plugin,
                        defaults={
                            'enabled': random.choice([True, False])
                        }
                    )
                    
                    if plugin_created:
                        print(f"    - 添加插件: {plugin.name} v{plugin.version}")
            
            # 添加应用日志
            if status != 'draft':
                log_count = random.randint(5, 15)
                
                for i in range(log_count):
                    timestamp = created_at + timedelta(minutes=random.randint(1, int((timezone.now() - created_at).total_seconds() / 60)))
                    
                    log_level = random.choice(['INFO', 'WARNING', 'ERROR', 'DEBUG'])
                    log_message = ""
                    
                    if log_level == 'INFO':
                        templates = [
                            "应用启动成功",
                            "收到用户请求，ID: {}",
                            "请求处理完成，耗时: {}ms",
                            "模型响应成功，标记数: {}",
                            "缓存命中，返回缓存结果"
                        ]
                        log_message = random.choice(templates).format(
                            uuid.uuid4(),
                            random.randint(50, 2000),
                            random.randint(100, 5000)
                        )
                    elif log_level == 'WARNING':
                        templates = [
                            "请求处理时间超过阈值: {}ms",
                            "缓存接近容量上限: {}%",
                            "并发请求数接近限制: {}/{}",
                            "模型响应时间异常: {}ms"
                        ]
                        log_message = random.choice(templates).format(
                            random.randint(1000, 5000),
                            random.randint(80, 95),
                            random.randint(config['max_concurrency']-2, config['max_concurrency']),
                            config['max_concurrency'],
                            random.randint(2000, 8000)
                        )
                    elif log_level == 'ERROR':
                        templates = [
                            "模型调用失败: {}",
                            "请求超时: 超过{}秒",
                            "内存不足: 当前使用{}MB",
                            "插件加载失败: {}",
                            "无法连接到模型服务: {}"
                        ]
                        log_message = random.choice(templates).format(
                            "连接拒绝",
                            config['timeout'],
                            random.randint(800, 2000),
                            random.choice([p.name for p in plugins]) if plugins else "未知插件",
                            "连接超时"
                        )
                    elif log_level == 'DEBUG':
                        templates = [
                            "请求参数: {}",
                            "模型配置: {}",
                            "处理流程: {} -> {} -> {}",
                            "缓存状态: 已用{}/总容量{}"
                        ]
                        log_message = random.choice(templates).format(
                            json.dumps({"query": "示例查询", "max_tokens": random.randint(100, 1000)}),
                            json.dumps({"temperature": 0.7, "top_p": 0.95}),
                            "接收请求", "处理输入", "调用模型",
                            random.randint(1, max(config['cache_size'], 1)),
                            config['cache_size']
                        )
                    
                    # 创建日志条目
                    ApplicationLog.objects.create(
                        application=application,
                        timestamp=timestamp,
                        level=log_level,
                        message=log_message
                    )
            
            # 添加应用指标
            if status in ['running', 'stopped']:
                metrics_data = {
                    'total_requests': random.randint(100, 10000),
                    'avg_response_time': round(random.uniform(50, 2000), 2),
                    'error_rate': round(random.uniform(0, 0.05), 4),
                    'cache_hit_rate': round(random.uniform(0.3, 0.9), 2) if config['cache_size'] > 0 else 0,
                }
                
                # CPU使用率历史数据
                metrics_data['cpu_usage_history'] = [round(random.uniform(5, 80), 1) for _ in range(24)]
                
                # 内存使用率历史数据
                metrics_data['memory_usage_history'] = [round(random.uniform(10, 90), 1) for _ in range(24)]
                
                # 每日请求量历史数据
                metrics_data['daily_requests'] = [random.randint(10, 500) for _ in range(30)]
                
                # 创建或更新指标
                ApplicationMetric.objects.update_or_create(
                    application=application,
                    defaults={
                        'total_requests': metrics_data['total_requests'],
                        'avg_response_time': metrics_data['avg_response_time'],
                        'error_rate': metrics_data['error_rate'],
                        'cpu_usage': metrics_data['cpu_usage_history'][-1] if metrics_data['cpu_usage_history'] else 0,
                        'memory_usage': metrics_data['memory_usage_history'][-1] if metrics_data['memory_usage_history'] else 0
                    }
                )
    
    return applications_created

def main():
    """主函数"""
    print("开始初始化应用中心测试数据...")
    
    # 创建插件
    plugins = create_plugins()
    
    # 创建应用程序
    applications = create_applications()
    
    print("\n测试数据初始化完成！")
    print(f"创建了 {len(plugins)} 个插件")
    print(f"创建了 {len(applications)} 个应用程序")

if __name__ == "__main__":
    main() 