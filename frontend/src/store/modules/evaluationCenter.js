/**
 * 评估中心模块的状态管理
 */
import evaluationCenter from '@/api/evaluationCenter'
import trainingCenter from '@/api/trainingCenter'
import dataCenter from '@/api/dataCenter'

const state = {
  evaluationTasks: [],
  reports: [],
  comparisons: [],
  models: [],
  datasets: [],
  currentTask: null,
  currentReport: null,
  loading: false,
  error: null,
  pagination: {
    currentPage: 1,
    pageSize: 10,
    total: 0
  }
}

const getters = {
  evaluationTaskList: state => state.evaluationTasks,
  reportList: state => state.reports,
  comparisonList: state => state.comparisons,
  modelList: state => state.models,
  datasetList: state => state.datasets,
  currentTask: state => state.currentTask,
  currentReport: state => state.currentReport,
  loading: state => state.loading,
  error: state => state.error,
  pagination: state => state.pagination,
  totalTasks: state => state.evaluationTasks.length,
  totalReports: state => state.reports.length,
  totalComparisons: state => state.comparisons.length
}

const mutations = {
  SET_EVALUATION_TASKS(state, tasks) {
    state.evaluationTasks = Array.isArray(tasks) ? tasks : []
  },
  SET_REPORTS(state, reports) {
    state.reports = Array.isArray(reports) ? reports : []
  },
  SET_COMPARISONS(state, comparisons) {
    state.comparisons = Array.isArray(comparisons) ? comparisons : []
  },
  SET_MODELS(state, models) {
    state.models = Array.isArray(models) ? models : []
  },
  SET_DATASETS(state, datasets) {
    state.datasets = Array.isArray(datasets) ? datasets : []
  },
  SET_CURRENT_TASK(state, task) {
    state.currentTask = task
  },
  SET_CURRENT_REPORT(state, report) {
    state.currentReport = report
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  },
  ADD_EVALUATION_TASK(state, task) {
    state.evaluationTasks.unshift(task)
  },
  UPDATE_EVALUATION_TASK(state, updatedTask) {
    const index = state.evaluationTasks.findIndex(task => task.id === updatedTask.id)
    if (index !== -1) {
      state.evaluationTasks.splice(index, 1, updatedTask)
      if (state.currentTask && state.currentTask.id === updatedTask.id) {
        state.currentTask = updatedTask
      }
    }
  },
  DELETE_EVALUATION_TASK(state, taskId) {
    state.evaluationTasks = state.evaluationTasks.filter(task => task.id !== taskId)
    if (state.currentTask && state.currentTask.id === taskId) {
      state.currentTask = null
    }
  },
  SET_PAGINATION(state, { currentPage, pageSize, total }) {
    state.pagination = { currentPage, pageSize, total }
  }
}

const actions = {
  // 获取评估任务列表
  async fetchEvaluationTasks({ commit }, params = {}) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.getEvaluationTasks(params)
      console.log('评估任务API响应:', response)
      
      // 处理API响应数据
      let tasks = []
      if (response && response.results) {
        tasks = response.results
      } else if (Array.isArray(response)) {
        tasks = response
      } else if (response && response.data) {
        tasks = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      commit('SET_EVALUATION_TASKS', tasks)
      return tasks
    } catch (error) {
      console.error('获取评估任务失败:', error)
      commit('SET_ERROR', error.message || '获取评估任务失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取评估任务详情
  async fetchEvaluationTaskDetail({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.getEvaluationTaskDetail(id)
      const task = response.data || response
      commit('SET_CURRENT_TASK', task)
      return task
    } catch (error) {
      console.error('获取评估任务详情失败:', error)
      commit('SET_ERROR', error.message || '获取评估任务详情失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 创建评估任务
  async createEvaluationTask({ commit }, data) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.createEvaluationTask(data)
      const task = response.data || response
      commit('ADD_EVALUATION_TASK', task)
      return task
    } catch (error) {
      console.error('创建评估任务失败:', error)
      commit('SET_ERROR', error.message || '创建评估任务失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 更新评估任务
  async updateEvaluationTask({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.updateEvaluationTask(id, data)
      const task = response.data || response
      commit('UPDATE_EVALUATION_TASK', task)
      return task
    } catch (error) {
      console.error('更新评估任务失败:', error)
      commit('SET_ERROR', error.message || '更新评估任务失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 删除评估任务
  async deleteEvaluationTask({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      await evaluationCenter.deleteEvaluationTask(id)
      commit('DELETE_EVALUATION_TASK', id)
      return true
    } catch (error) {
      console.error('删除评估任务失败:', error)
      commit('SET_ERROR', error.message || '删除评估任务失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 开始评估任务
  async startEvaluationTask({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.startEvaluationTask(id)
      const task = response.data || response
      commit('UPDATE_EVALUATION_TASK', task)
      return task
    } catch (error) {
      console.error('开始评估任务失败:', error)
      commit('SET_ERROR', error.message || '开始评估任务失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 停止评估任务
  async stopEvaluationTask({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.stopEvaluationTask(id)
      const task = response.data || response
      commit('UPDATE_EVALUATION_TASK', task)
      return task
    } catch (error) {
      console.error('停止评估任务失败:', error)
      commit('SET_ERROR', error.message || '停止评估任务失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取评估报告列表
  async fetchEvaluationReports({ commit }, params = {}) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.getEvaluationReports(params)
      console.log('评估报告API响应:', response)
      
      // 处理API响应数据
      let reports = []
      if (response && response.results) {
        reports = response.results
      } else if (Array.isArray(response)) {
        reports = response
      } else if (response && response.data) {
        reports = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      commit('SET_REPORTS', reports)
      return reports
    } catch (error) {
      console.error('获取评估报告失败:', error)
      commit('SET_ERROR', error.message || '获取评估报告失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取评估报告详情
  async fetchEvaluationReportDetail({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.getEvaluationReportDetail(id)
      const report = response.data || response
      commit('SET_CURRENT_REPORT', report)
      return report
    } catch (error) {
      console.error('获取评估报告详情失败:', error)
      commit('SET_ERROR', error.message || '获取评估报告详情失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取模型对比列表
  async fetchComparisons({ commit }, params = {}) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.getModelComparisons(params)
      console.log('模型对比API响应:', response)
      
      // 处理API响应数据
      let comparisons = []
      if (response && response.results) {
        comparisons = response.results
      } else if (Array.isArray(response)) {
        comparisons = response
      } else if (response && response.data) {
        comparisons = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      commit('SET_COMPARISONS', comparisons)
      return comparisons
    } catch (error) {
      console.error('获取模型对比失败:', error)
      commit('SET_ERROR', error.message || '获取模型对比失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 创建模型对比
  async createModelComparison({ commit }, data) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.createModelComparison(data)
      const comparison = response.data || response
      commit('SET_COMPARISONS', [...state.comparisons, comparison])
      return comparison
    } catch (error) {
      console.error('创建模型对比失败:', error)
      commit('SET_ERROR', error.message || '创建模型对比失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取所有模型（从训练中心）
  async fetchAllModels({ commit }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await trainingCenter.getModels()
      console.log('模型API响应:', response)
      
      // 处理API响应数据
      let models = []
      if (response && response.results) {
        models = response.results
      } else if (Array.isArray(response)) {
        models = response
      } else if (response && response.data) {
        models = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      commit('SET_MODELS', models)
      return models
    } catch (error) {
      console.error('获取模型失败:', error)
      commit('SET_ERROR', error.message || '获取模型失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取所有数据集（从数据中心）
  async fetchAllDatasets({ commit }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.getDatasets()
      console.log('数据集API响应:', response)
      
      // 处理API响应数据
      let datasets = []
      if (response && response.results) {
        datasets = response.results
      } else if (Array.isArray(response)) {
        datasets = response
      } else if (response && response.data) {
        datasets = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      commit('SET_DATASETS', datasets)
      return datasets
    } catch (error) {
      console.error('获取数据集失败:', error)
      commit('SET_ERROR', error.message || '获取数据集失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取评估指标
  async fetchEvaluationMetrics({ commit }, taskId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.getEvaluationMetrics(taskId)
      return response.data || response
    } catch (error) {
      console.error('获取评估指标失败:', error)
      commit('SET_ERROR', error.message || '获取评估指标失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 导出评估报告
  async exportEvaluationReport({ commit }, { id, params = {} }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await evaluationCenter.exportEvaluationReport(id, params)
      return response.data || response
    } catch (error) {
      console.error('导出评估报告失败:', error)
      commit('SET_ERROR', error.message || '导出评估报告失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 设置分页
  setPagination({ commit }, pagination) {
    commit('SET_PAGINATION', pagination)
  },

  // 删除评测报告
  async deleteEvaluationReport({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await evaluationCenter.deleteEvaluationReport(id)
      commit('DELETE_EVALUATION_REPORT', id)
      commit('SET_ERROR', null)
    } catch (error) {
      console.error('删除评测报告失败:', error)
      commit('SET_ERROR', '删除评测报告失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取知识库在评测中心的使用情况
  async fetchKnowledgeBaseUsage({ commit }, knowledgeBaseId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      // 模拟获取知识库在评测任务中的使用情况
      const response = await new Promise(resolve => {
        setTimeout(() => {
          resolve({
            data: [
              {
                id: 1,
                name: '知识库检索准确性评测',
                created_at: new Date().toISOString(),
                status: 'completed',
                test_type: 'accuracy'
              },
              {
                id: 2,
                name: '知识库响应速度评测',
                created_at: new Date().toISOString(),
                status: 'running',
                test_type: 'performance'
              }
            ]
          })
        }, 300)
      })
      return response
    } catch (error) {
      console.error('获取知识库评测使用情况失败:', error)
      commit('SET_ERROR', error.message || '获取知识库评测使用情况失败')
      return { data: [] }
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
} 