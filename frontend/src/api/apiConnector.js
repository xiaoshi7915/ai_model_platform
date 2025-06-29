import axios from 'axios'

// API基础路径 - 修改去掉多余的前缀
const baseURL = `api-connector`

// API连接器相关接口
export default {
  // 获取API提供商列表
  getProviders(params = {}) {
    return axios.get(`/${baseURL}/providers/`, { params })
  },
  
  // 获取API提供商详情
  getProviderDetail(id) {
    return axios.get(`/${baseURL}/providers/${id}/`)
  },
  
  // 创建API提供商
  createProvider(data) {
    return axios.post(`/${baseURL}/providers/`, data)
  },
  
  // 更新API提供商
  updateProvider(id, data) {
    return axios.put(`/${baseURL}/providers/${id}/`, data)
  },
  
  // 删除API提供商
  deleteProvider(id) {
    return axios.delete(`/${baseURL}/providers/${id}/`)
  },
  
  // 获取API提供商类型
  getProviderTypes() {
    return axios.get(`/${baseURL}/providers/types/`)
  },
  
  // 获取API连接列表
  getConnections(params = {}) {
    return axios.get(`/${baseURL}/connections/`, { params })
  },
  
  // 获取API连接详情
  getConnectionDetail(id) {
    return axios.get(`/${baseURL}/connections/${id}/`)
  },
  
  // 创建API连接
  createConnection(data) {
    return axios.post(`/${baseURL}/connections/`, data)
  },
  
  // 更新API连接
  updateConnection(id, data) {
    return axios.put(`/${baseURL}/connections/${id}/`, data)
  },
  
  // 删除API连接
  deleteConnection(id) {
    return axios.delete(`/${baseURL}/connections/${id}/`)
  },
  
  // 设置API连接为默认
  setDefaultConnection(id) {
    return axios.post(`/${baseURL}/connections/${id}/set_default/`)
  },
  
  // 测试API连接
  testConnection(id) {
    return axios.post(`/${baseURL}/connections/${id}/test/`)
  },
  
  // 获取API使用日志列表
  getLogs(params = {}) {
    return axios.get(`/${baseURL}/logs/`, { params })
  },
  
  // 获取API使用统计
  getStatistics(params = {}) {
    return axios.get(`/${baseURL}/logs/statistics/`, { params })
  }
} 