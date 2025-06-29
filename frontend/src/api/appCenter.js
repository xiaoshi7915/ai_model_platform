// 应用中心相关的API服务
// 包括应用和插件的操作

import request from '@/utils/request'

export default {
  /**
   * 获取应用列表
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回应用列表
   */
  getApplications(params = {}) {
    return request({
      url: '/app-center/applications/',
      method: 'get',
      params
    })
  },

  /**
   * 获取应用详情
   * @param {number} id - 应用ID
   * @returns {Promise} - 返回应用详情
   */
  getApplicationDetail(id) {
    return request({
      url: `/app-center/applications/${id}/`,
      method: 'get'
    })
  },

  /**
   * 创建应用
   * @param {Object} data - 应用数据
   * @returns {Promise} - 返回创建结果
   */
  createApplication(data) {
    return request({
      url: '/app-center/applications/',
      method: 'post',
      data
    })
  },

  /**
   * 更新应用
   * @param {number} id - 应用ID
   * @param {Object} data - 应用数据
   * @returns {Promise} - 返回更新结果
   */
  updateApplication(id, data) {
    return request({
      url: `/app-center/applications/${id}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除应用
   * @param {number} id - 应用ID
   * @returns {Promise} - 返回删除结果
   */
  deleteApplication(id) {
    return request({
      url: `/app-center/applications/${id}/`,
      method: 'delete'
    })
  },

  /**
   * 部署应用
   * @param {number} id - 应用ID
   * @returns {Promise} - 返回部署结果
   */
  deployApplication(id) {
    return request({
      url: `/app-center/applications/${id}/deploy/`,
      method: 'post'
    })
  },

  /**
   * 停止应用
   * @param {number} id - 应用ID
   * @returns {Promise} - 返回停止结果
   */
  stopApplication(id) {
    return request({
      url: `/app-center/applications/${id}/stop/`,
      method: 'post'
    })
  },

  /**
   * 获取应用监控数据
   * @param {number} id - 应用ID
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回监控数据
   */
  getApplicationMonitoring(id, params = {}) {
    return request({
      url: `/app-center/applications/${id}/monitoring/`,
      method: 'get',
      params
    })
  },

  /**
   * 获取应用日志
   * @param {number} id - 应用ID
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回应用日志
   */
  getApplicationLogs(id, params = {}) {
    return request({
      url: `/app-center/applications/${id}/logs/`,
      method: 'get',
      params
    })
  },

  /**
   * 获取插件列表
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回插件列表
   */
  getPlugins(params = {}) {
    return request({
      url: '/app-center/plugins/',
      method: 'get',
      params
    })
  },

  /**
   * 获取插件详情
   * @param {number} id - 插件ID
   * @returns {Promise} - 返回插件详情
   */
  getPluginDetail(id) {
    return request({
      url: `/app-center/plugins/${id}/`,
      method: 'get'
    })
  },

  /**
   * 创建插件
   * @param {Object} data - 插件数据
   * @returns {Promise} - 返回创建结果
   */
  createPlugin(data) {
    return request({
      url: '/app-center/plugins/',
      method: 'post',
      data
    })
  },

  /**
   * 更新插件
   * @param {number} id - 插件ID
   * @param {Object} data - 插件数据
   * @returns {Promise} - 返回更新结果
   */
  updatePlugin(id, data) {
    return request({
      url: `/app-center/plugins/${id}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除插件
   * @param {number} id - 插件ID
   * @returns {Promise} - 返回删除结果
   */
  deletePlugin(id) {
    return request({
      url: `/app-center/plugins/${id}/`,
      method: 'delete'
    })
  },

  /**
   * 为应用添加插件
   * @param {number} applicationId - 应用ID
   * @param {number} pluginId - 插件ID
   * @param {Object} data - 配置数据
   * @returns {Promise} - 返回添加结果
   */
  addPluginToApplication(applicationId, pluginId, data = {}) {
    return request({
      url: `/app-center/applications/${applicationId}/add_plugin/`,
      method: 'post',
      data: { plugin_id: pluginId, ...data }
    })
  },

  /**
   * 从应用移除插件
   * @param {number} applicationId - 应用ID
   * @param {number} pluginId - 插件ID
   * @returns {Promise} - 返回移除结果
   */
  removePluginFromApplication(applicationId, pluginId) {
    return request({
      url: `/app-center/applications/${applicationId}/remove_plugin/`,
      method: 'post',
      data: { plugin_id: pluginId }
    })
  }
} 