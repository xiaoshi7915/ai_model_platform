"""
数据中心应用的URL配置
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, KnowledgeBaseViewSet

# 创建路由器
router = DefaultRouter()
router.register(r'datasets', DatasetViewSet)
router.register(r'knowledge-bases', KnowledgeBaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 