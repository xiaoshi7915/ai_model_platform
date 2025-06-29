from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APIProviderViewSet, APIConnectionViewSet, APIUsageLogViewSet, APIModelViewSet

# 创建路由器
router = DefaultRouter()
router.register(r'providers', APIProviderViewSet)
router.register(r'connections', APIConnectionViewSet)
router.register(r'logs', APIUsageLogViewSet)
router.register(r'models', APIModelViewSet)

# URL配置
urlpatterns = [
    path('', include(router.urls)),
] 