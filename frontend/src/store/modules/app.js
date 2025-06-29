// app.js - 应用全局状态管理

import Vue from 'vue'
import axios from 'axios'
import { mockApplications, mockPlugins, mockMetrics, mockLogs } from '@/utils/mockData'

// API基础路径
const API_BASE = '/api/v1'

const state = {
  applications: [],
  application: null,
  plugins: [],
  loading: false,
  error: null,
  metrics: {},
  logs: {}
}

const mutations = {
  SET_APPLICATIONS(state, applications) {
    state.applications = applications
  },
  SET_APPLICATION(state, application) {
    state.application = application
  },
  SET_PLUGINS(state, plugins) {
    state.plugins = plugins
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  },
  SET_APPLICATION_METRICS(state, { applicationId, metrics }) {
    Vue.set(state.metrics, applicationId, metrics)
  },
  SET_APPLICATION_LOGS(state, { applicationId, logs }) {
    Vue.set(state.logs, applicationId, logs)
  }
}

const actions = {
  // 获取所有应用列表
  async fetchApplications({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.get(`${API_BASE}/app-center/applications/`)
      // 处理API响应数据
      const applications = response.data?.results || response.data || []
      commit('SET_APPLICATIONS', Array.isArray(applications) ? applications : [])
      return response.data
    } catch (error) {
      console.error('获取应用列表失败:', error)
      commit('SET_ERROR', error.message || '获取应用列表失败')
      // 使用模拟数据作为备选
      commit('SET_APPLICATIONS', mockApplications)
      return { results: mockApplications }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取单个应用详情
  async fetchApplication({ commit }, applicationId) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.get(`${API_BASE}/app-center/applications/${applicationId}/`)
      commit('SET_APPLICATION', response.data)
      return response.data
    } catch (error) {
      console.error('获取应用详情失败:', error)
      commit('SET_ERROR', error.message || '获取应用详情失败')
      // 使用模拟数据作为备选
      const mockApp = mockApplications.find(app => app.id === applicationId) || mockApplications[0]
      commit('SET_APPLICATION', mockApp)
      return mockApp
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 创建应用
  async createApplication({ commit, dispatch }, applicationData) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.post(`${API_BASE}/app-center/applications/`, applicationData)
      // 创建成功后刷新应用列表
      await dispatch('fetchApplications')
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message || '创建应用失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 更新应用
  async updateApplication({ commit, dispatch }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.put(`${API_BASE}/app-center/applications/${id}/`, data)
      // 更新成功后刷新应用列表
      await dispatch('fetchApplications')
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message || '更新应用失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 删除应用
  async deleteApplication({ commit, dispatch }, applicationId) {
    commit('SET_LOADING', true)
    try {
      await axios.delete(`${API_BASE}/app-center/applications/${applicationId}/`)
      // 删除成功后刷新应用列表
      await dispatch('fetchApplications')
      return true
    } catch (error) {
      commit('SET_ERROR', error.message || '删除应用失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 部署应用
  async deployApplication({ commit, dispatch }, applicationId) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.post(`${API_BASE}/app-center/applications/${applicationId}/deploy/`)
      // 部署请求成功后刷新应用列表
      await dispatch('fetchApplications')
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message || '部署应用失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 停止应用
  async stopApplication({ commit, dispatch }, applicationId) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.post(`${API_BASE}/app-center/applications/${applicationId}/stop/`)
      // 停止请求成功后刷新应用列表
      await dispatch('fetchApplications')
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.message || '停止应用失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取插件列表
  async fetchPlugins({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await axios.get(`${API_BASE}/app-center/plugins/`)
      // 处理API响应数据
      const plugins = response.data?.results || response.data || []
      commit('SET_PLUGINS', Array.isArray(plugins) ? plugins : [])
      return response.data
    } catch (error) {
      console.error('获取插件列表失败:', error)
      commit('SET_ERROR', error.message || '获取插件列表失败')
      // 使用模拟数据作为备选
      commit('SET_PLUGINS', mockPlugins)
      return { results: mockPlugins }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取应用监控数据
  async fetchApplicationMetrics({ commit }, applicationId) {
    try {
      const response = await axios.get(`${API_BASE}/app-center/applications/${applicationId}/metrics/`)
      const metrics = response.data || {
        cpu_usage: 0,
        memory_usage: 0,
        total_requests: 0,
        avg_response_time: 0,
        error_rate: 0
      }
      commit('SET_APPLICATION_METRICS', { applicationId, metrics })
      return metrics
    } catch (error) {
      console.error('获取应用监控数据失败:', error)
      // 使用模拟数据作为备选
      commit('SET_APPLICATION_METRICS', { applicationId, metrics: mockMetrics })
      return mockMetrics
    }
  },

  // 获取应用日志
  async fetchApplicationLogs({ commit }, { applicationId, level, page, pageSize }) {
    try {
      const params = {
        level: level || '',
        page: page || 1,
        page_size: pageSize || 10
      }
      const response = await axios.get(`${API_BASE}/app-center/applications/${applicationId}/logs/`, { params })
      const logs = response.data || { results: [], count: 0 }
      commit('SET_APPLICATION_LOGS', { applicationId, logs })
      return logs
    } catch (error) {
      console.error('获取应用日志失败:', error)
      // 使用模拟数据作为备选
      commit('SET_APPLICATION_LOGS', { applicationId, logs: mockLogs })
      return mockLogs
    }
  }
}

const getters = {
  applicationById: state => id => {
    return state.applications.find(app => app.id === id) || null
  },
  applicationMetrics: state => id => {
    return state.metrics[id] || {
      cpu_usage: 0,
      memory_usage: 0,
      total_requests: 0,
      avg_response_time: 0,
      error_rate: 0
    }
  },
  applicationLogs: state => id => {
    return state.logs[id] || { results: [], count: 0 }
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 