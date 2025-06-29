import request from '@/utils/request'
import { API_BASE_URL } from '@/config'

// API基础路径
const baseURL = `/api/v1/auth`

// 用户API
export default {
  // 登录
  login(data) {
    return request({
      url: `${baseURL}/login/`,
      method: 'post',
      data
    })
  },
  
  // 注册
  register(data) {
    return request({
      url: `${baseURL}/register/`,
      method: 'post',
      data
    })
  },
  
  // 获取用户信息
  getUserInfo() {
    return request({
      url: `${baseURL}/profile/`,
      method: 'get'
    })
  },
  
  // 登出
  logout() {
    return request({
      url: `${baseURL}/logout/`,
      method: 'post'
    })
  }
} 