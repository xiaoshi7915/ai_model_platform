"""
URL配置文件
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API文档配置
schema_view = get_schema_view(
    openapi.Info(
        title="大模型构建管理平台 API",
        default_version='v1',
        description="大模型构建管理平台的API文档",
        terms_of_service="http://chenxiaoshivivid.com.cn:6688/all",
        contact=openapi.Contact(email="chenxs@flamelephant.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # 管理后台
    path('admin/', admin.site.urls),
    
    # API文档
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # 主要API路由 - 无版本号（推荐使用）
    path('api/auth/', include('api.urls')),
    path('api/data-center/', include('data_center.urls')),
    path('api/training-center/', include('training_center.urls')),
    path('api/app-center/', include('app_center.urls')),
    path('api/evaluation-center/', include('evaluation_center.urls')),
    path('api/api-connector/', include('api_connector.urls')),
    
    # 兼容旧版API路由 - v1版本号（向后兼容）
    path('api/v1/auth/', include('api.urls')),
    path('api/v1/data-center/', include('data_center.urls')),
    path('api/v1/training-center/', include('training_center.urls')),
    path('api/v1/app-center/', include('app_center.urls')),
    path('api/v1/evaluation-center/', include('evaluation_center.urls')),
    path('api/v1/api-connector/', include('api_connector.urls')),
]

# 在开发环境中提供媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 