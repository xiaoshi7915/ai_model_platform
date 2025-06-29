import request from '@/utils/request'

// API基础路径
const baseURL = `/api/training-center`

// 模型API
export default {
  // 获取模型列表
  getModels() {
    return request({
      url: `${baseURL}/models/`,
      method: 'get'
    })
  },
  
  // 获取模型详情
  getModelDetail(id) {
    return request({
      url: `${baseURL}/models/${id}/`,
      method: 'get'
    })
  },
  
  // 创建模型
  createModel(data) {
    return request({
      url: `${baseURL}/models/`,
      method: 'post',
      data
    })
  },
  
  // 更新模型
  updateModel(id, data) {
    return request({
      url: `${baseURL}/models/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除模型
  deleteModel(id) {
    return request({
      url: `${baseURL}/models/${id}/`,
      method: 'delete'
    })
  },
  
  // 开始训练模型
  trainModel(id, data) {
    return request({
      url: `${baseURL}/models/${id}/train/`,
      method: 'post',
      data
    })
  },
  
  // 取消训练模型
  cancelTraining(id) {
    return request({
      url: `${baseURL}/models/${id}/cancel/`,
      method: 'post'
    })
  }
} 