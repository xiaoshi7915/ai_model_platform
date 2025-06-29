// 应用中心Vuex模块
import api from '@/api'
import { generateMockApplications, generateMockPlugins } from '@/utils/mockData'

const state = {
  applications: [], // 应用列表
  currentApplication: null, // 当前应用
  plugins: [], // 插件列表
  loading: false, // 加载状态
  error: null // 错误信息
}

const mutations = {
  // 设置应用列表
  SET_APPLICATIONS(state, applications) {
    state.applications = applications
  },
  
  // 设置当前应用
  SET_CURRENT_APPLICATION(state, application) {
    state.currentApplication = application
  },
  
  // 设置插件列表
  SET_PLUGINS(state, plugins) {
    state.plugins = plugins
  },
  
  // 设置加载状态
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  
  // 设置错误信息
  SET_ERROR(state, error) {
    state.error = error
  },
  
  // 添加应用
  ADD_APPLICATION(state, application) {
    state.applications.push(application)
  },
  
  // 更新应用
  UPDATE_APPLICATION(state, application) {
    const index = state.applications.findIndex(app => app.id === application.id)
    if (index !== -1) {
      state.applications.splice(index, 1, application)
    }
  },
  
  // 删除应用
  DELETE_APPLICATION(state, id) {
    state.applications = state.applications.filter(app => app.id !== id)
  },
  
  // 添加插件
  ADD_PLUGIN(state, plugin) {
    state.plugins.push(plugin)
  }
}

const actions = {
  // 获取应用列表
  async fetchApplications({ commit }, params) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.getApplications(params)
      console.log('Applications API Response:', response)
      
      // 处理API响应数据
      let applications = []
      if (response && response.results) {
        applications = response.results
      } else if (Array.isArray(response)) {
        applications = response
      } else if (response && response.data) {
        applications = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      commit('SET_APPLICATIONS', applications)
      commit('SET_ERROR', null)
      return applications
    } catch (error) {
      console.error('获取应用列表失败:', error)
      commit('SET_ERROR', '获取应用列表失败')
      return []
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取应用详情
  async fetchApplicationDetail({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.getApplicationDetail(id)
      console.log('Application Detail API Response:', response)
      
      const application = response.data || response
      commit('SET_CURRENT_APPLICATION', application)
      commit('SET_ERROR', null)
      return application
    } catch (error) {
      console.error('获取应用详情失败:', error)
      commit('SET_ERROR', '获取应用详情失败')
      return null
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建应用
  async createApplication({ commit }, data) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.createApplication(data)
      const application = response.data || response
      commit('ADD_APPLICATION', application)
      commit('SET_ERROR', null)
      return application
    } catch (error) {
      console.error('创建应用失败:', error)
      commit('SET_ERROR', '创建应用失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新应用
  async updateApplication({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.updateApplication(id, data)
      const application = response.data || response
      commit('UPDATE_APPLICATION', application)
      commit('SET_ERROR', null)
      return application
    } catch (error) {
      console.error('更新应用失败:', error)
      commit('SET_ERROR', '更新应用失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除应用
  async deleteApplication({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await api.appCenter.deleteApplication(id)
      commit('DELETE_APPLICATION', id)
      commit('SET_ERROR', null)
      return true
    } catch (error) {
      console.error('删除应用失败:', error)
      commit('SET_ERROR', '删除应用失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 部署应用
  async deployApplication({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.deployApplication(id)
      const application = response.data || response
      commit('UPDATE_APPLICATION', application)
      commit('SET_ERROR', null)
      return application
    } catch (error) {
      console.error('部署应用失败:', error)
      commit('SET_ERROR', '部署应用失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 停止应用
  async stopApplication({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.stopApplication(id)
      const application = response.data || response
      commit('UPDATE_APPLICATION', application)
      commit('SET_ERROR', null)
      return application
    } catch (error) {
      console.error('停止应用失败:', error)
      commit('SET_ERROR', '停止应用失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取应用监控数据
  async fetchApplicationMonitoring({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.getApplicationMonitoring(id)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      console.error('获取应用监控数据失败:', error)
      commit('SET_ERROR', '获取应用监控数据失败')
      return null
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取应用日志
  async fetchApplicationLogs({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.getApplicationLogs(id)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      console.error('获取应用日志失败:', error)
      commit('SET_ERROR', '获取应用日志失败')
      return null
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取插件列表
  async fetchPlugins({ commit }, params) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.getPlugins(params)
      console.log('Plugins API Response:', response)
      
      // 处理API响应数据
      let plugins = []
      if (response && response.results) {
        plugins = response.results
      } else if (Array.isArray(response)) {
        plugins = response
      } else if (response && response.data) {
        plugins = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      commit('SET_PLUGINS', plugins)
      commit('SET_ERROR', null)
      return plugins
    } catch (error) {
      console.error('获取插件列表失败:', error)
      commit('SET_ERROR', '获取插件列表失败')
      return []
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取插件详情
  async fetchPluginDetail({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.getPluginDetail(id)
      const plugin = response.data || response
      commit('SET_CURRENT_PLUGIN', plugin)
      commit('SET_ERROR', null)
      return plugin
    } catch (error) {
      console.error('获取插件详情失败:', error)
      commit('SET_ERROR', '获取插件详情失败')
      return null
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建插件
  async createPlugin({ commit }, data) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.createPlugin(data)
      const plugin = response.data || response
      commit('ADD_PLUGIN', plugin)
      commit('SET_ERROR', null)
      return plugin
    } catch (error) {
      console.error('创建插件失败:', error)
      commit('SET_ERROR', '创建插件失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新插件
  async updatePlugin({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.updatePlugin(id, data)
      const plugin = response.data || response
      commit('UPDATE_PLUGIN', plugin)
      commit('SET_ERROR', null)
      return plugin
    } catch (error) {
      console.error('更新插件失败:', error)
      commit('SET_ERROR', '更新插件失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除插件
  async deletePlugin({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await api.appCenter.deletePlugin(id)
      commit('DELETE_PLUGIN', id)
      commit('SET_ERROR', null)
      return true
    } catch (error) {
      console.error('删除插件失败:', error)
      commit('SET_ERROR', '删除插件失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 添加插件到应用
  async addPluginToApplication({ commit, dispatch }, { applicationId, pluginId, config = {} }) {
    commit('SET_LOADING', true)
    try {
      await api.appCenter.addPluginToApplication(applicationId, { plugin_id: pluginId, config })
      await dispatch('fetchApplicationDetail', applicationId)
      commit('SET_ERROR', null)
      return true
    } catch (error) {
      console.error('添加插件失败:', error)
      commit('SET_ERROR', '添加插件失败')
      return false
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 从应用中移除插件
  async removePluginFromApplication({ commit, dispatch }, { applicationId, pluginId }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.appCenter.removePluginFromApplication(applicationId, pluginId)
      // 重新获取应用详情以更新插件列表
      await dispatch('fetchApplicationDetail', applicationId)
      commit('SET_ERROR', null)
      return response
    } catch (error) {
      console.error('移除插件失败:', error)
      commit('SET_ERROR', '移除插件失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取知识库在应用中心的使用情况
  async fetchKnowledgeBaseUsage({ commit }, knowledgeBaseId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      // 模拟获取知识库在应用中的使用情况
      const response = await new Promise(resolve => {
        setTimeout(() => {
          resolve({
            data: [
              {
                id: 1,
                name: '智能问答应用',
                created_at: new Date().toISOString(),
                status: 'running',
                app_type: 'QA'
              },
              {
                id: 2,
                name: '文档检索助手',
                created_at: new Date().toISOString(),
                status: 'deployed',
                app_type: 'Search'
              }
            ]
          })
        }, 300)
      })
      return response
    } catch (error) {
      console.error('获取知识库应用使用情况失败:', error)
      commit('SET_ERROR', error.message || '获取知识库应用使用情况失败')
      return { data: [] }
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const getters = {
  // 获取应用列表
  applications: state => state.applications,
  
  // 获取当前应用
  currentApplication: state => state.currentApplication,
  
  // 获取插件列表
  plugins: state => state.plugins,
  
  // 获取加载状态
  loading: state => state.loading,
  
  // 获取错误信息
  error: state => state.error,
  
  // 获取运行中的应用
  runningApplications: state => state.applications.filter(app => app.status === 'running'),
  
  // 获取已停止的应用
  stoppedApplications: state => state.applications.filter(app => app.status === 'stopped')
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 