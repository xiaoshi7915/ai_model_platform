// 请求工具
import axios from 'axios'
import { Message, MessageBox } from 'element-ui'
import store from '@/store'
import router from '@/router'
import { REQUEST_TIMEOUT } from '@/config'

// 禁用模拟数据，始终使用真实API
const useMockData = false

// 创建axios实例
const service = axios.create({
  baseURL: 'http://localhost:5688/api/v1',  // 指向后端5688端口
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前做处理
    const token = store.getters.token
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    console.log('原始请求URL:', config.url);
    console.log('baseURL:', config.baseURL);
    
    // 不需要复杂的URL处理，因为baseURL已经是/api/v1
    // 只需要确保URL以/开头即可
    if (!config.url.startsWith('/')) {
      config.url = '/' + config.url;
    }

    console.log('最终请求URL:', config.url);
    console.log('完整URL:', config.baseURL + config.url);
    
    return config
  },
  error => {
    // 处理请求错误
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 标记是否正在刷新token
let isRefreshing = false;
// 等待刷新token的请求队列
let waitingQueue = [];

// 响应拦截器
service.interceptors.response.use(
  response => {
    // 正常响应
    return response
  },
  error => {
    // 响应错误处理
    console.error('Response error in request.js:', error)
    
    // 获取原始请求配置
    const originalRequest = error.config;
    
    if (error.response) {
      // 服务器响应了，但状态码不是2xx
      const status = error.response.status
      const data = error.response.data
      
      // 处理不同的错误状态
      switch (status) {
        case 400:
          Message.error(data.message || data.detail || '请求参数错误')
          break
          
        case 401:
          // 如果没有在刷新token，则尝试刷新
          if (!isRefreshing) {
            isRefreshing = true;
            
            // 尝试刷新token，若有refresh_token可使用
            store.dispatch('user/refreshToken')
              .then(() => {
                console.log('Token刷新成功，重新发送队列中的请求');
                // 刷新成功，重新发送队列中的请求
                waitingQueue.forEach(callback => callback());
                waitingQueue = [];
              })
              .catch((refreshError) => {
                console.error('刷新token失败:', refreshError);
                // 刷新失败，需要重新登录，但不立即跳转
                Message.warning('身份验证已过期');
              })
              .finally(() => {
                isRefreshing = false;
              });
          }
          
          // 将请求加入队列
          return new Promise(resolve => {
            waitingQueue.push(() => {
              // 替换新的token
              originalRequest.headers['Authorization'] = `Bearer ${store.getters.token}`;
              resolve(service(originalRequest));
            });
          });
          
        case 403:
          Message.error('没有权限执行此操作')
          break
          
        case 404:
          Message.error('请求的资源不存在')
          break
          
        case 500:
          Message.error('服务器内部错误，请联系管理员')
          break
          
        default:
          Message.error(data.message || data.detail || `请求失败(${status})`)
      }
    } else if (error.request) {
      // 请求已发出，但未收到响应
      Message.error('服务器未响应，请检查网络连接')
    } else {
      // 发送请求时出错
      Message.error(`请求错误: ${error.message}`)
    }
    
    return Promise.reject(error)
  }
)

export default service 