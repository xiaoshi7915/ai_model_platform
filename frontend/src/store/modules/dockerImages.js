import axios from 'axios'
import { getDockerImages, createDockerImage, updateDockerImage, deleteDockerImage } from '@/api/dockerImages'
// 移除未使用的导入
// import { API_BASE_URL } from '@/config'

// 修改Docker镜像API路径 - 移除重复的api/v1前缀
const api = {
  getDockerImages: '/training-center/docker-images/',
  createDockerImage: '/training-center/docker-images/',
  updateDockerImage: (id) => `/training-center/docker-images/${id}/`,
  deleteDockerImage: (id) => `/training-center/docker-images/${id}/`
}

// 初始状态
const state = {
  dockerImages: [], // 存储Docker镜像列表
  count: 0, // 总镜像数量
  next: null, // 下一页API链接
  previous: null, // 上一页API链接
  loading: false,   // 加载状态
  error: null       // 错误信息
}

// getter
const getters = {
  // 获取Docker镜像列表
  dockerImages: state => state.dockerImages,
  
  // 通过ID获取Docker镜像
  getDockerImageById: state => id => {
    return state.dockerImages.find(image => image.id === id)
  },
  
  // 获取加载状态
  loading: state => state.loading,
  
  // 获取错误信息
  error: state => state.error,
  
  // 获取总数
  totalCount: state => state.count
}

// actions
const actions = {
  // 获取Docker镜像列表
  fetchDockerImages({ commit }, params = {}) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    
    return getDockerImages(params)
      .then(response => {
        // 处理API返回的分页数据格式
        commit('SET_DOCKER_IMAGES', response)
        return response
      })
      .catch(error => {
        commit('SET_ERROR', error.message || '获取Docker镜像列表失败')
        throw error
      })
      .finally(() => {
        commit('SET_LOADING', false)
      })
  },
  
  // 获取单个Docker镜像详情
  async fetchDockerImage({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.get(api.getDockerImageById(id))
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message || '获取Docker镜像详情失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建Docker镜像
  createDockerImage({ commit, dispatch }, imageData) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    
    return createDockerImage(imageData)
      .then(response => {
        // 创建成功后重新获取镜像列表
        dispatch('fetchDockerImages')
        return response
      })
      .catch(error => {
        commit('SET_ERROR', error.message || '创建Docker镜像失败')
        throw error
      })
      .finally(() => {
        commit('SET_LOADING', false)
      })
  },
  
  // 更新Docker镜像
  updateDockerImage({ commit, dispatch }, { id, imageData }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    
    return updateDockerImage(id, imageData)
      .then(response => {
        // 更新成功后重新获取镜像列表
        dispatch('fetchDockerImages')
        return response
      })
      .catch(error => {
        commit('SET_ERROR', error.message || '更新Docker镜像失败')
        throw error
      })
      .finally(() => {
        commit('SET_LOADING', false)
      })
  },
  
  // 删除Docker镜像
  deleteDockerImage({ commit, dispatch }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    
    return deleteDockerImage(id)
      .then(response => {
        // 删除成功后重新获取镜像列表
        dispatch('fetchDockerImages')
        return response
      })
      .catch(error => {
        commit('SET_ERROR', error.message || '删除Docker镜像失败')
        throw error
      })
      .finally(() => {
        commit('SET_LOADING', false)
      })
  }
}

// mutations
const mutations = {
  // 设置Docker镜像列表
  SET_DOCKER_IMAGES(state, data) {
    // 处理API返回的分页数据结构
    state.dockerImages = data.results || []
    state.count = data.count || 0
    state.next = data.next || null
    state.previous = data.previous || null
  },
  
  // 设置加载状态
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  
  // 设置错误信息
  SET_ERROR(state, error) {
    state.error = error
  },
  
  // 清除错误信息
  CLEAR_ERROR(state) {
    state.error = null
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
} 