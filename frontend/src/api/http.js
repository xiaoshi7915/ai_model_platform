// HTTP请求工具
// 封装axios，处理请求拦截和响应拦截

import axios from 'axios'
import store from '@/store'
import router from '@/router'
import { Message } from 'element-ui'

// 创建axios实例
const http = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || '/api/v1', // API基础URL
  timeout: 30000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json'
  }
})

// 调试信息
console.log('API基础URL:', http.defaults.baseURL);

// 请求拦截器
http.interceptors.request.use(
  config => {
    // 在请求发送前添加token
    const token = store.state.token
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    // 调试信息
    console.log('发送请求:', config.method.toUpperCase(), config.url);
    
    return config
  },
  error => {
    // 请求错误处理
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
http.interceptors.response.use(
  response => {
    // 响应数据处理
    console.log('请求成功:', response.config.url, response.status);
    return response.data
  },
  error => {
    // 响应错误处理
    const { response } = error
    
    if (response) {
      // 调试信息
      console.error('请求失败:', error.config?.url, response.status, response.data);
      
      // 根据状态码处理不同错误
      switch (response.status) {
        case 401: // 未授权
          Message.error('登录已过期，请重新登录')
          store.dispatch('logout')
          router.push('/login')
          break
        case 403: // 禁止访问
          Message.error('没有权限访问该资源')
          break
        case 404: // 资源不存在
          Message.error('请求的资源不存在')
          break
        case 500: // 服务器错误
          Message.error('服务器错误，请稍后再试')
          break
        default:
          // 其他错误
          Message.error(response.data.message || '请求失败')
      }
    } else {
      // 网络错误
      console.error('网络错误:', error.message);
      Message.error('网络错误，请检查网络连接或服务器状态')
    }
    
    return Promise.reject(error)
  }
)

// 封装GET请求
export const get = (url, params = {}) => {
  return http.get(url, { params })
}

// 封装POST请求
export const post = (url, data = {}) => {
  return http.post(url, data)
}

// 封装PUT请求
export const put = (url, data = {}) => {
  return http.put(url, data)
}

// 封装DELETE请求
export const del = (url) => {
  return http.delete(url)
}

// 封装上传文件请求
export const upload = (url, file, onProgress) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return http.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: progressEvent => {
      if (onProgress) {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(percentCompleted)
      }
    }
  })
}

// 封装下载文件请求
export const download = (url, params = {}, filename) => {
  return http.get(url, {
    params,
    responseType: 'blob'
  }).then(response => {
    // 创建Blob对象
    const blob = new Blob([response])
    
    // 创建下载链接
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = filename || getFilenameFromResponse(response)
    link.click()
    
    // 释放URL对象
    URL.revokeObjectURL(link.href)
  })
}

// 从响应头中获取文件名
const getFilenameFromResponse = (response) => {
  const contentDisposition = response.headers['content-disposition']
  if (contentDisposition) {
    const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/
    const matches = filenameRegex.exec(contentDisposition)
    if (matches != null && matches[1]) {
      return matches[1].replace(/['"]/g, '')
    }
  }
  return 'download'
}

export default http 