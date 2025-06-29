"""
应用中心应用的URL配置
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, PluginViewSet

# 创建路由器
router = DefaultRouter()
router.register(r'applications', ApplicationViewSet)
router.register(r'plugins', PluginViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 