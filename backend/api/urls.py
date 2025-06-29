"""
API应用的URL配置
"""

from django.urls import path
from .views import UserLoginView, UserLogoutView, UserRegisterView, UserProfileView, TokenRefreshView

urlpatterns = [
    # 用户认证相关
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
] 