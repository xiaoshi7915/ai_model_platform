// API服务入口文件
// 导出所有API服务

import axios from 'axios'
import user from './user'
import model from './model'
import dataset from './dataset'
import auth from './auth'
import trainingCenter from './trainingCenter'
import appCenter from './appCenter'
import evaluationCenter from './evaluationCenter'
import dataCenter from './dataCenter'
import apiConnector from './apiConnector'
import request from '@/utils/request'
import Cookies from 'js-cookie'

// 配置axios默认值
axios.defaults.timeout = 30000
axios.defaults.headers.common['Content-Type'] = 'application/json'
// 确保API路径前缀统一
axios.defaults.baseURL = '/api/v1'

// 设置CSRF令牌
const csrftoken = Cookies.get('csrftoken')
if (csrftoken) {
  request.defaults.headers.common['X-CSRFToken'] = csrftoken
}

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
    
    // 彻底解决重复前缀问题
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
    
    // 4. 确保所有非绝对URL都以/开头
    if (!config.url.startsWith('http') && !config.url.startsWith('/')) {
      config.url = '/' + config.url;
    }
    
    console.log('处理后的请求URL:', config.url);
    
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
axios.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // 如果是401错误，尝试刷新Token而不是直接登出
    if (error.response && error.response.status === 401) {
      console.warn('认证失败，尝试刷新Token');
      
      // 获取store实例
      const store = window._vueStore;
      if (store) {
        // 尝试刷新token
        store.dispatch('user/refreshToken')
          .then(() => {
            console.log('Token刷新成功，重试请求');
            // 刷新成功后，可以重试原始请求
            const originalRequest = error.config;
            return axios(originalRequest);
          })
          .catch(refreshError => {
            console.error('Token刷新失败:', refreshError);
            // 如果刷新失败，才考虑重定向到登录页
          });
      }
    }
    return Promise.reject(error)
  }
)

// 合并所有 API
const api = {
  user,
  model,
  dataset,
  evaluationCenter,
  dataCenter,
  trainingCenter,
  appCenter,
  auth,
  apiConnector,
  training: {
    // 获取模型列表
    getModels() {
      return axios.get('/training-center/models/')
    },
    // 获取模型详情
    getModelDetail(id) {
      return axios.get(`/training-center/models/${id}/`)
    },
    // 创建模型
    createModel(data) {
      return axios.post('/training-center/models/', data)
    },
    // 更新模型
    updateModel(id, data) {
      return axios.put(`/training-center/models/${id}/`, data)
    },
    // 删除模型
    deleteModel(id) {
      return axios.delete(`/training-center/models/${id}/`)
    },
    // 获取Docker镜像列表
    getDockerImages(params) {
      return axios.get('/training-center/docker-images/', { params })
    },
    // 获取Docker镜像详情
    getDockerImageDetail(id) {
      return axios.get(`/training-center/docker-images/${id}/`)
    },
    // 创建Docker镜像
    createDockerImage(data) {
      return axios.post('/training-center/docker-images/', data)
    },
    // 更新Docker镜像
    updateDockerImage(id, data) {
      return axios.put(`/training-center/docker-images/${id}/`, data)
    },
    // 删除Docker镜像
    deleteDockerImage(id) {
      return axios.delete(`/training-center/docker-images/${id}/`)
    },
    // 获取训练任务列表
    getTrainingJobs(params) {
      return axios.get('/training-center/training-jobs/', { params })
    },
    // 获取训练任务详情
    getTrainingJobDetail(id) {
      return axios.get(`/training-center/training-jobs/${id}/`)
    },
    // 取消训练任务
    cancelTrainingJob(id) {
      return axios.post(`/training-center/training-jobs/${id}/cancel/`)
    },
    // 训练模型
    trainModel(id, data) {
      return axios.post(`/training-center/models/${id}/train/`, data)
    },
    // 获取模型版本列表
    getModelVersions(id) {
      return axios.get(`/training-center/models/${id}/versions/`)
    }
  }
}

// 将store实例保存到全局，以便在拦截器中访问
export function setStore(store) {
  window._vueStore = store;
}

export default api 