"""
评测中心应用的URL配置
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvaluationTaskViewSet, EvaluationReportViewSet, ModelComparisonViewSet

# 创建路由器
router = DefaultRouter()
router.register(r'tasks', EvaluationTaskViewSet)
router.register(r'reports', EvaluationReportViewSet)
router.register(r'comparisons', ModelComparisonViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 