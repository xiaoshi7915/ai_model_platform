import Vue from 'vue'
import Vuex from 'vuex'
import Cookies from 'js-cookie'
import dockerImages from './modules/dockerImages'
import api from '@/api'
import user from './modules/user'
import model from './modules/model'
import dataset from './modules/dataset'
import appCenter from './modules/appCenter'
import dataCenter from './modules/dataCenter'
import trainingCenter from './modules/trainingCenter'
import evaluationCenter from './modules/evaluationCenter'
import app from './modules/app'
import axios from 'axios'
import training from './modules/training'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    dockerImages,
    user,
    model,
    dataset,
    appCenter,
    dataCenter,
    trainingCenter,
    evaluationCenter,
    training
  },
  state: {
    loading: false,
    error: null
  },
  getters: {
    isLoading: state => state.loading,
    error: state => state.error,
    // 用户相关getters
    token: state => state.user.token,
    refreshToken: state => state.user.refreshToken, 
    userInfo: state => state.user.userInfo,
    isLoggedIn: state => !!state.user.token
  },
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading)
    },
    setError({ commit }, error) {
      commit('SET_ERROR', error)
    },
    // 认证相关
    async login({ commit }, credentials) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.auth.login(credentials)
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '登录失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async register({ commit }, userData) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.auth.register(userData)
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '注册失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async logout({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        await api.auth.logout()
      } catch (error) {
        commit('SET_ERROR', error.message || '登出失败')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchUserProfile({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.auth.getProfile()
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '获取用户信息失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 数据中心相关
    async fetchDatasets({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.dataCenter.getDatasets()
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '获取数据集失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchKnowledgeBases({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.dataCenter.getKnowledgeBases()
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '获取知识库失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 训练中心相关
    async fetchModels({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.trainingCenter.getModels()
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '获取模型失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchTrainingJobs({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.trainingCenter.getTrainingJobs()
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '获取训练任务失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 应用中心相关
    async fetchApplications({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.appCenter.getApplications()
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '获取应用失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchPlugins({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.appCenter.getPlugins()
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '获取插件失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 评测中心相关
    async fetchEvaluationTasks({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.evaluationCenter.getEvaluationTasks()
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '获取评测任务失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchEvaluationReports({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.evaluationCenter.getEvaluationReports()
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '获取评测报告失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchModelComparisons({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.evaluationCenter.getModelComparisons()
        return response
      } catch (error) {
        commit('SET_ERROR', error.message || '获取模型比较失败')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  strict: process.env.NODE_ENV !== 'production'
})

export default store 