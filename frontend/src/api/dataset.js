import request from '@/utils/request'

// API基础路径
const baseURL = `/api/data-center`

// 数据集API
export default {
  // 获取数据集列表
  getDatasets() {
    return request({
      url: `${baseURL}/datasets/`,
      method: 'get'
    })
  },
  
  // 获取数据集详情
  getDatasetDetail(id) {
    return request({
      url: `${baseURL}/datasets/${id}/`,
      method: 'get'
    })
  },
  
  // 创建数据集
  createDataset(data) {
    return request({
      url: `${baseURL}/datasets/`,
      method: 'post',
      data
    })
  },
  
  // 更新数据集
  updateDataset(id, data) {
    return request({
      url: `${baseURL}/datasets/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除数据集
  deleteDataset(id) {
    return request({
      url: `${baseURL}/datasets/${id}/`,
      method: 'delete'
    })
  }
} 