"""
ASGI配置文件
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')

application = get_asgi_application() 