import axios from 'axios'

// API基础路径
const API_BASE = '/api/v1'

const state = {
  models: [],
  currentModel: null,
  jobs: [],
  loading: false,
  error: null
}

const mutations = {
  SET_MODELS(state, models) {
    state.models = models
  },
  SET_CURRENT_MODEL(state, model) {
    state.currentModel = model
  },
  SET_JOBS(state, jobs) {
    state.jobs = jobs
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  }
}

const actions = {
  // 获取所有模型列表
  async fetchModels({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.get(`${API_BASE}/training-center/models/`, { params })
      let models = []
      
      if (response) {
        if (Array.isArray(response)) {
          models = response
        } else if (response.results && Array.isArray(response.results)) {
          models = response.results
        } else if (typeof response === 'object') {
          models = [response]
        }
      }
      
      commit('SET_MODELS', models)
      commit('SET_ERROR', null)
      return models
    } catch (error) {
      console.error('获取模型列表失败:', error)
      commit('SET_ERROR', error.message || '获取模型列表失败')
      commit('SET_MODELS', [])
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取单个模型详情
  async fetchModel({ commit }, modelId) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.get(`${API_BASE}/training-center/models/${modelId}/`)
      commit('SET_CURRENT_MODEL', response.data)
      return response.data
    } catch (error) {
      console.error('获取模型详情失败:', error)
      commit('SET_ERROR', error.message || '获取模型详情失败')
      // 直接抛出错误，不使用模拟数据
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取训练任务列表
  async fetchJobs({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.get(`${API_BASE}/training-center/jobs/`)
      commit('SET_JOBS', response.data.results || response.data)
      return response.data
    } catch (error) {
      console.error('获取训练任务列表失败:', error)
      commit('SET_ERROR', error.message || '获取训练任务列表失败')
      // 返回空数组，避免UI错误
      commit('SET_JOBS', [])
      return { results: [] }
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const getters = {
  modelById: state => id => {
    return state.models.find(model => model.id === id) || null
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 