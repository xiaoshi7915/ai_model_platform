import time
import json
import logging
import requests
from django.conf import settings
from django.core.cache import cache
from .models import APIConnection, APIUsageLog

logger = logging.getLogger(__name__)

class APIConnector:
    """API连接器工具类，用于处理与外部API的交互"""
    
    def __init__(self, connection_id=None, provider_type=None):
        """
        初始化API连接器
        
        Args:
            connection_id: API连接的ID，如果提供则使用指定的连接
            provider_type: API提供商类型，如果提供但未指定connection_id，则使用该类型的默认连接
        """
        self.connection = None
        
        if connection_id:
            # 获取指定的连接
            try:
                self.connection = APIConnection.objects.get(id=connection_id, is_active=True)
            except APIConnection.DoesNotExist:
                raise ValueError(f"无法找到ID为{connection_id}的API连接")
        elif provider_type:
            # 获取指定提供商类型的默认连接
            try:
                self.connection = APIConnection.objects.filter(
                    provider__provider_type=provider_type,
                    is_active=True,
                    is_default=True
                ).first()
                
                if not self.connection:
                    # 如果没有默认连接，使用第一个活跃连接
                    self.connection = APIConnection.objects.filter(
                        provider__provider_type=provider_type,
                        is_active=True
                    ).first()
                    
                if not self.connection:
                    raise ValueError(f"无法找到类型为{provider_type}的活跃API连接")
            except Exception as e:
                raise ValueError(f"获取API连接失败: {str(e)}")
        else:
            raise ValueError("必须提供connection_id或provider_type参数")
    
    def _prepare_headers(self, additional_headers=None):
        """准备请求头"""
        headers = {
            'Content-Type': 'application/json',
        }
        
        # 添加认证信息
        if self.connection.provider.provider_type == 'openai':
            headers['Authorization'] = f"Bearer {self.connection.api_key}"
            if self.connection.org_id:
                headers['OpenAI-Organization'] = self.connection.org_id
        elif self.connection.provider.provider_type == 'google':
            headers['Authorization'] = f"Bearer {self.connection.api_key}"
        elif self.connection.provider.provider_type == 'baidu':
            # 百度API使用不同的认证方式，在请求参数中处理
            pass
        elif self.connection.provider.provider_type == 'azure':
            headers['api-key'] = self.connection.api_key
        elif self.connection.provider.provider_type == 'anthropic':
            headers['x-api-key'] = self.connection.api_key
        elif self.connection.provider.provider_type == 'huggingface':
            headers['Authorization'] = f"Bearer {self.connection.api_key}"
        else:
            # 自定义API，使用存储的自定义头
            if self.connection.custom_headers:
                try:
                    for key, value in self.connection.custom_headers.items():
                        headers[key] = value
                except Exception as e:
                    logger.error(f"解析自定义请求头时出错: {str(e)}")
        
        # 添加额外请求头
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def _handle_response(self, response, endpoint):
        """处理API响应"""
        try:
            if response.status_code >= 200 and response.status_code < 300:
                return response.json()
            else:
                error_msg = f"API请求失败，状态码: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f"，错误信息: {json.dumps(error_detail)}"
                except:
                    error_msg += f"，错误响应: {response.text}"
                
                logger.error(error_msg)
                return {
                    'error': True,
                    'status_code': response.status_code,
                    'message': error_msg
                }
        except Exception as e:
            logger.exception(f"处理API响应时出错: {str(e)}")
            return {
                'error': True,
                'message': f"处理API响应时出错: {str(e)}"
            }
    
    def _log_usage(self, endpoint, request_data, response_data, status, 
                   error_message=None, tokens_used=0, response_time=0, user_ip=None):
        """记录API使用日志"""
        try:
            APIUsageLog.objects.create(
                connection=self.connection,
                endpoint=endpoint,
                request_data=request_data,
                response_data=response_data,
                status=status,
                error_message=error_message,
                tokens_used=tokens_used,
                response_time=response_time,
                user_ip=user_ip
            )
        except Exception as e:
            logger.exception(f"记录API使用日志时出错: {str(e)}")
    
    def call_api(self, endpoint, method='POST', data=None, params=None, 
                additional_headers=None, user_ip=None, log_usage=True):
        """
        调用API接口
        
        Args:
            endpoint: API端点路径，相对于base_url
            method: 请求方法，默认为POST
            data: 请求体数据
            params: URL参数
            additional_headers: 额外的请求头
            user_ip: 用户IP，用于日志记录
            log_usage: 是否记录使用日志
            
        Returns:
            API响应数据
        """
        # 构建完整URL
        url = f"{self.connection.provider.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # 准备请求头
        headers = self._prepare_headers(additional_headers)
        
        # 准备请求参数
        request_params = {}
        if params:
            request_params.update(params)
        
        # 添加自定义参数
        if self.connection.custom_params:
            try:
                request_params.update(self.connection.custom_params)
            except Exception as e:
                logger.error(f"解析自定义参数时出错: {str(e)}")
        
        # 百度API特殊处理：需要获取access_token
        if self.connection.provider.provider_type == 'baidu':
            token = cache.get(f'baidu_access_token_{self.connection.id}')
            if not token:
                token = self._get_baidu_access_token()
                cache.set(f'baidu_access_token_{self.connection.id}', token, 60 * 60 * 23)  # 23小时过期
            
            request_params['access_token'] = token
        
        # 记录开始时间
        start_time = time.time()
        status = 'failed'
        error_message = None
        tokens_used = 0
        response_data = None
        
        try:
            # 发送请求
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=request_params, timeout=60)
            elif method.upper() == 'POST':
                json_data = json.dumps(data) if data else None
                response = requests.post(url, headers=headers, params=request_params, 
                                        data=json_data, timeout=60)
            else:
                response = requests.request(method, url, headers=headers, params=request_params, 
                                          json=data, timeout=60)
            
            # 处理响应
            response_data = self._handle_response(response, endpoint)
            
            # 计算令牌使用量（仅用于OpenAI等提供这些信息的API）
            if isinstance(response_data, dict):
                if 'error' in response_data and response_data['error']:
                    status = 'error'
                    error_message = response_data.get('message', '未知错误')
                else:
                    status = 'success'
                    # 尝试获取令牌使用量
                    usage = response_data.get('usage', {})
                    tokens_used = usage.get('total_tokens', 0) or 0
        except requests.exceptions.Timeout:
            status = 'failed'
            error_message = "API请求超时"
            response_data = {'error': True, 'message': error_message}
        except requests.exceptions.RequestException as e:
            status = 'failed'
            error_message = f"API请求异常: {str(e)}"
            response_data = {'error': True, 'message': error_message}
        except Exception as e:
            status = 'error'
            error_message = f"API调用过程中发生错误: {str(e)}"
            response_data = {'error': True, 'message': error_message}
        finally:
            # 计算响应时间
            response_time = (time.time() - start_time) * 1000  # 转换为毫秒
            
            # 记录使用日志
            if log_usage:
                self._log_usage(
                    endpoint=endpoint,
                    request_data=data,
                    response_data=response_data,
                    status=status,
                    error_message=error_message,
                    tokens_used=tokens_used,
                    response_time=response_time,
                    user_ip=user_ip
                )
            
            return response_data
    
    def _get_baidu_access_token(self):
        """获取百度API的access_token"""
        api_key = self.connection.api_key
        secret_key = self.connection.api_secret
        
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            'grant_type': 'client_credentials',
            'client_id': api_key,
            'client_secret': secret_key
        }
        
        try:
            response = requests.post(url, params=params)
            result = response.json()
            return result.get('access_token')
        except Exception as e:
            logger.exception(f"获取百度API access_token时出错: {str(e)}")
            return None


# 使用示例函数
def call_openai_api(prompt, model="gpt-3.5-turbo", connection_id=None, user_ip=None):
    """调用OpenAI API的示例函数"""
    try:
        connector = APIConnector(connection_id=connection_id, provider_type='openai' if not connection_id else None)
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        response = connector.call_api(
            endpoint="chat/completions",
            data=data,
            user_ip=user_ip
        )
        
        if response and not response.get('error', False):
            if 'choices' in response and len(response['choices']) > 0:
                return {
                    'success': True,
                    'content': response['choices'][0]['message']['content'],
                    'usage': response.get('usage', {})
                }
        
        return {
            'success': False,
            'error': response.get('message', '未知错误'),
            'details': response
        }
        
    except Exception as e:
        logger.exception(f"调用OpenAI API时出错: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def call_baidu_api(prompt, connection_id=None, user_ip=None):
    """调用百度文心API的示例函数"""
    try:
        connector = APIConnector(connection_id=connection_id, provider_type='baidu' if not connection_id else None)
        
        data = {
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = connector.call_api(
            endpoint="rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions",
            data=data,
            user_ip=user_ip
        )
        
        if response and not response.get('error', False):
            return {
                'success': True,
                'content': response.get('result', ''),
                'usage': response.get('usage', {})
            }
        
        return {
            'success': False,
            'error': response.get('message', '未知错误'),
            'details': response
        }
        
    except Exception as e:
        logger.exception(f"调用百度API时出错: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        } 