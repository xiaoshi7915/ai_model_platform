// 数据中心相关的API服务
import request from '@/utils/request'

export default {
  // 获取数据集列表
  getDatasets(params = {}) {
    return request({
      url: '/data-center/datasets/',
      method: 'get',
      params
    })
  },
  
  // 获取数据集详情
  getDatasetDetail(id) {
    return request({
      url: `/data-center/datasets/${id}/`,
      method: 'get'
    })
  },
  
  // 创建数据集
  createDataset(data, file, onProgress) {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      formData.append(key, data[key])
    })
    if (file) {
      formData.append('file', file)
    }
    
    return request({
      url: '/data-center/datasets/',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: onProgress
    })
  },
  
  // 更新数据集
  updateDataset(id, data) {
    return request({
      url: `/data-center/datasets/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除数据集
  deleteDataset(id) {
    return request({
      url: `/data-center/datasets/${id}/`,
      method: 'delete'
    })
  },
  
  // 获取数据集格式列表
  getDatasetFormats() {
    return request({
      url: '/data-center/datasets/formats/',
      method: 'get'
    })
  },
  
  // 获取数据集统计信息
  getDatasetStats(id) {
    return request({
      url: `/data-center/datasets/${id}/stats/`,
      method: 'get'
    })
  },
  
  // 获取知识库列表
  getKnowledgeBases(params = {}) {
    return request({
      url: '/data-center/knowledge-bases/',
      method: 'get',
      params
    })
  },
  
  // 获取知识库详情
  getKnowledgeBaseDetail(id) {
    return request({
      url: `/data-center/knowledge-bases/${id}/`,
      method: 'get'
    })
  },
  
  // 创建知识库
  createKnowledgeBase(data) {
    return request({
      url: '/data-center/knowledge-bases/',
      method: 'post',
      data
    })
  },
  
  // 更新知识库
  updateKnowledgeBase(id, data) {
    return request({
      url: `/data-center/knowledge-bases/${id}/`,
      method: 'put',
      data
    })
  },
  
  // 删除知识库
  deleteKnowledgeBase(id) {
    return request({
      url: `/data-center/knowledge-bases/${id}/`,
      method: 'delete'
    })
  },
  
  // 导入数据到数据集
  importDataToDataset(id, data) {
    return request({
      url: `/data-center/datasets/${id}/import/`,
      method: 'post',
      data
    })
  },
  
  // 导出数据集
  exportDataset(id, params = {}) {
    return request({
      url: `/data-center/datasets/${id}/export/`,
      method: 'get',
      params
    })
  },
  
  // 向知识库添加文档
  addDocumentToKnowledgeBase(id, data) {
    return request({
      url: `/data-center/knowledge-bases/${id}/documents/`,
      method: 'post',
      data
    })
  },
  
  // 从知识库删除文档
  removeDocumentFromKnowledgeBase(knowledgeBaseId, documentId) {
    return request({
      url: `/data-center/knowledge-bases/${knowledgeBaseId}/documents/${documentId}/`,
      method: 'delete'
    })
  },
  
  // 搜索知识库
  searchKnowledgeBase(id, query) {
    return request({
      url: `/data-center/knowledge-bases/${id}/search/`,
      method: 'post',
      data: { query }
    })
  }
}
