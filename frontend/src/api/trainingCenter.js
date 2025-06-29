// 训练中心相关的API服务
// 包括模型、Docker镜像和训练任务的操作

import request from '@/utils/request'
// 删除未使用的导入，避免ESLint警告
// import { API_BASE_URL } from '@/config'

// 基础路径配置 - 移除多余的前缀
const baseURL = `training-center`

export default {
  /**
   * 获取模型列表
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回模型列表
   */
  getModels(params = {}) {
    return request({
      url: `/training-center/models/`,
      method: 'get',
      params
    })
  },

  /**
   * 获取模型详情
   * @param {number} id - 模型ID
   * @returns {Promise} - 返回模型详情
   */
  getModelDetail(id) {
    return request({
      url: `/training-center/models/${id}/`,
      method: 'get'
    })
  },

  /**
   * 创建模型
   * @param {Object} data - 模型数据
   * @returns {Promise} - 返回创建结果
   */
  createModel(data) {
    return request({
      url: `/training-center/models/`,
      method: 'post',
      data
    })
  },

  /**
   * 更新模型
   * @param {number} id - 模型ID
   * @param {Object} data - 模型数据
   * @returns {Promise} - 返回更新结果
   */
  updateModel(id, data) {
    return request({
      url: `/training-center/models/${id}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除模型
   * @param {number} id - 模型ID
   * @returns {Promise} - 返回删除结果
   */
  deleteModel(id) {
    return request({
      url: `/training-center/models/${id}/`,
      method: 'delete'
    })
  },

  /**
   * 训练模型
   * @param {number} id - 模型ID
   * @param {Object} data - 训练参数
   * @returns {Promise} - 返回训练结果
   */
  trainModel(id, data = {}) {
    return request({
      url: `/training-center/models/${id}/train/`,
      method: 'post',
      data
    })
  },

  /**
   * 获取模型版本列表
   * @param {number} id - 模型ID
   * @returns {Promise} - 返回模型版本列表
   */
  getModelVersions(id) {
    return request({
      url: `/training-center/models/${id}/versions/`,
      method: 'get'
    })
  },

  /**
   * 获取Docker镜像列表
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回Docker镜像列表
   */
  getDockerImages(params = {}) {
    return request({
      url: `/training-center/docker-images/`,
      method: 'get',
      params
    })
  },

  /**
   * 获取Docker镜像详情
   * @param {number} id - Docker镜像ID
   * @returns {Promise} - 返回Docker镜像详情
   */
  getDockerImageDetail(id) {
    return request({
      url: `/training-center/docker-images/${id}/`,
      method: 'get'
    })
  },

  /**
   * 创建Docker镜像
   * @param {Object} data - Docker镜像数据
   * @returns {Promise} - 返回创建结果
   */
  createDockerImage(data) {
    return request({
      url: `/training-center/docker-images/`,
      method: 'post',
      data
    })
  },

  /**
   * 更新Docker镜像
   * @param {number} id - Docker镜像ID
   * @param {Object} data - Docker镜像数据
   * @returns {Promise} - 返回更新结果
   */
  updateDockerImage(id, data) {
    return request({
      url: `/training-center/docker-images/${id}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除Docker镜像
   * @param {number} id - Docker镜像ID
   * @returns {Promise} - 返回删除结果
   */
  deleteDockerImage(id) {
    return request({
      url: `/training-center/docker-images/${id}/`,
      method: 'delete'
    })
  },

  /**
   * 获取训练任务列表
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回训练任务列表
   */
  getTrainingTasks(params = {}) {
    return request({
      url: `/training-center/training-jobs/`,
      method: 'get',
      params
    })
  },

  /**
   * 获取训练任务详情
   * @param {number} id - 训练任务ID
   * @returns {Promise} - 返回训练任务详情
   */
  getTrainingTaskDetail(id) {
    return request({
      url: `/training-center/training-jobs/${id}/`,
      method: 'get'
    })
  },

  /**
   * 创建训练任务
   * @param {Object} data - 训练任务数据
   * @returns {Promise} - 返回创建结果
   */
  createTrainingTask(data) {
    return request({
      url: `/training-center/training-jobs/`,
      method: 'post',
      data
    })
  },

  /**
   * 更新训练任务
   * @param {number} id - 训练任务ID
   * @param {Object} data - 训练任务数据
   * @returns {Promise} - 返回更新结果
   */
  updateTrainingTask(id, data) {
    return request({
      url: `/training-center/training-jobs/${id}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除训练任务
   * @param {number} id - 训练任务ID
   * @returns {Promise} - 返回删除结果
   */
  deleteTrainingTask(id) {
    return request({
      url: `/training-center/training-jobs/${id}/`,
      method: 'delete'
    })
  },

  /**
   * 开始训练任务
   * @param {number} id - 训练任务ID
   * @returns {Promise} - 返回开始训练结果
   */
  startTrainingTask(id) {
    return request({
      url: `/training-center/training-jobs/${id}/start/`,
      method: 'post'
    })
  },

  /**
   * 停止训练任务
   * @param {number} id - 训练任务ID
   * @returns {Promise} - 返回停止训练结果
   */
  stopTrainingTask(id) {
    return request({
      url: `/training-center/training-jobs/${id}/stop/`,
      method: 'post'
    })
  },

  /**
   * 获取训练任务日志
   * @param {number} id - 训练任务ID
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回训练任务日志
   */
  getTrainingTaskLogs(id, params = {}) {
    return request({
      url: `/training-center/training-jobs/${id}/logs/`,
      method: 'get',
      params
    })
  },

  /**
   * 获取训练任务进度
   * @param {number} id - 训练任务ID
   * @returns {Promise} - 返回训练任务进度
   */
  getTrainingTaskProgress(id) {
    return request({
      url: `/training-center/training-jobs/${id}/progress/`,
      method: 'get'
    })
  },

  /**
   * 获取训练任务指标
   * @param {number} id - 训练任务ID
   * @returns {Promise} - 返回训练任务指标
   */
  getTrainingTaskMetrics(id) {
    return request({
      url: `/training-center/training-jobs/${id}/metrics/`,
      method: 'get'
    })
  },

  /**
   * 导出模型
   * @param {number} id - 模型ID
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回模型导出结果
   */
  exportModel(id, params = {}) {
    return request({
      url: `/training-center/models/${id}/export/`,
      method: 'get',
      params
    })
  },

  /**
   * 导入模型
   * @param {Object} data - 模型数据
   * @returns {Promise} - 返回模型导入结果
   */
  importModel(data) {
    return request({
      url: `/training-center/models/import/`,
      method: 'post',
      data
    })
  },

  /**
   * 创建模型版本
   * @param {number} modelId - 模型ID
   * @param {Object} data - 模型版本数据
   * @returns {Promise} - 返回模型版本创建结果
   */
  createModelVersion(modelId, data) {
    return request({
      url: `/training-center/models/${modelId}/versions/`,
      method: 'post',
      data
    })
  }
} 