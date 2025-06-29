/**
 * Docker镜像相关的API服务
 */

import request from '@/utils/request'

// 基础路径配置
const baseURL = '/training-center/docker-images'

/**
 * 获取Docker镜像列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Docker镜像列表
 */
export const getDockerImages = (params = {}) => {
  return request({
    url: `${baseURL}/`,
    method: 'get',
    params
  })
}

/**
 * 获取Docker镜像详情
 * @param {number} id - Docker镜像ID
 * @returns {Promise} - 返回Docker镜像详情
 */
export const getDockerImageDetail = (id) => {
  return request({
    url: `${baseURL}/${id}/`,
    method: 'get'
  })
}

/**
 * 创建Docker镜像
 * @param {Object} data - Docker镜像数据
 * @returns {Promise} - 返回创建结果
 */
export const createDockerImage = (data) => {
  return request({
    url: `${baseURL}/`,
    method: 'post',
    data
  })
}

/**
 * 更新Docker镜像
 * @param {number} id - Docker镜像ID
 * @param {Object} data - Docker镜像数据
 * @returns {Promise} - 返回更新结果
 */
export const updateDockerImage = (id, data) => {
  return request({
    url: `${baseURL}/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除Docker镜像
 * @param {number} id - Docker镜像ID
 * @returns {Promise} - 返回删除结果
 */
export const deleteDockerImage = (id) => {
  return request({
    url: `${baseURL}/${id}/`,
    method: 'delete'
  })
}

export default {
  getDockerImages,
  getDockerImageDetail,
  createDockerImage,
  updateDockerImage,
  deleteDockerImage
} 