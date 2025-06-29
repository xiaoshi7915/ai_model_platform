"""
API应用的视图
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    """用户登录视图"""
    permission_classes = [AllowAny]

    def post(self, request):
        """处理用户登录请求"""
        username = request.data.get('username')
        password = request.data.get('password')
        
        # 验证用户凭据
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_exempt, name='dispatch')
class TokenRefreshView(APIView):
    """Token刷新视图"""
    permission_classes = [AllowAny]

    def post(self, request):
        """处理token刷新请求"""
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),  # 也可以返回新的refresh token
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    """用户登出视图"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """处理用户登出请求"""
        logout(request)
        return Response({'message': '成功登出'})

@method_decorator(csrf_exempt, name='dispatch')
class UserRegisterView(APIView):
    """用户注册视图"""
    permission_classes = [AllowAny]

    def post(self, request):
        """处理用户注册请求"""
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            # 创建用户
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email', ''),
                password=serializer.validated_data['password']
            )
            
            # 登录新用户
            login(request, user)
            
            # 生成令牌
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """用户资料视图"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取用户资料"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """更新用户资料"""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 