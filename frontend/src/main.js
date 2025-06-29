import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import { API_BASE_URL } from './config'
import { setStore } from './api'

// 全局样式
import './assets/styles/main.css'

// 配置 Element UI
Vue.use(Element, {
  size: 'medium',
  zIndex: 3000
})

// 将store实例设置到API模块
setStore(store)

// 配置axios全局默认值
axios.defaults.baseURL = '/api/v1'  // 统一API前缀
axios.defaults.timeout = 30000
axios.defaults.headers.common['Content-Type'] = 'application/json'

// 请求拦截器
axios.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    // 添加CSRF Token
    const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)?.[1]
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }
    
    // 修复URL重复前缀问题
    // 1. 移除任何 /api/v1/api/v1/ 形式的重复前缀
    if (config.url.includes('/api/v1/api/v1/')) {
      config.url = config.url.replace('/api/v1/api/v1/', '/');
    }
    
    // 2. 移除 /api/v1/ 前缀，因为baseURL已经包含这个前缀
    if (config.url.startsWith('/api/v1/')) {
      config.url = config.url.replace('/api/v1/', '/');
    }
    
    // 3. 移除 /api/ 前缀
    if (config.url.startsWith('/api/')) {
      config.url = config.url.replace('/api/', '/');
    }
    
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
axios.interceptors.response.use(
  response => {
    // 如果响应包含data字段，则直接返回data
    if (response.data !== undefined) {
      return response.data
    }
    return response
  },
  error => {
    // 请求发生错误时的全局错误处理
    if (error.response) {
      const status = error.response.status
      
      // 处理401未授权错误
      if (status === 401) {
        // 尝试刷新token，而不是立即登出
        store.dispatch('user/refreshToken')
          .then(() => {
            console.log("Token刷新成功，重试原始请求");
            // 成功刷新token后，可以重试原始请求
            const originalRequest = error.config;
            return axios(originalRequest);
          })
          .catch(refreshError => {
            console.error("刷新token失败，需要重新登录:", refreshError);
            // 只有刷新失败时才清除token并跳转登录页
            if (router.currentRoute.path !== '/login') {
              Element.Message.warning('登录已过期，请重新登录')
              // 清除token
              localStorage.removeItem('token')
              router.push('/login')
            }
          });
        
        // 返回一个新的Promise，避免后续错误处理
        return new Promise((resolve, reject) => {
          // 这里不做任何操作，让上面的重试逻辑处理
        });
      } else if (status === 403) {
        Element.Message.error('没有权限执行此操作')
      } else if (status === 500) {
        Element.Message.error('服务器错误，请联系管理员')
      } else {
        const errorMessage = error.response.data.message || error.response.data.detail || `请求失败(${status})`
        Element.Message.error(errorMessage)
      }
    } else if (error.request) {
      Element.Message.error('服务器未响应，请检查网络连接')
    } else {
      Element.Message.error(`请求错误: ${error.message}`)
    }
    
    return Promise.reject(error)
  }
)

// 全局注册axios
Vue.prototype.$axios = axios

Vue.config.productionTip = false

// 自动登录功能
const autoLogin = async () => {
  // 检查是否已经有token
  const token = localStorage.getItem('token')
  if (token) {
    console.log('已有token，跳过自动登录')
    return
  }
  
  try {
    console.log('开始自动登录...')
    await store.dispatch('user/login', {
      username: 'admin',
      password: '123456'
    })
    console.log('自动登录成功')
  } catch (error) {
    console.error('自动登录失败:', error)
  }
}

// 在Vue实例创建前执行自动登录
autoLogin().then(() => {
  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount('#app')
}) 