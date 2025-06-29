"""
训练中心应用的URL配置
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModelViewSet, DockerImageViewSet, TrainingJobViewSet

# 创建路由器
router = DefaultRouter()
router.register(r'models', ModelViewSet)
router.register(r'docker-images', DockerImageViewSet)
router.register(r'training-jobs', TrainingJobViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 