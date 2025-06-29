/**
 * 数据中心模块的状态管理
 */
import dataCenter from '@/api/dataCenter'

const state = {
  datasets: [],         // 数据集列表
  knowledgeBases: [],   // 知识库列表
  currentDataset: null, // 当前选中的数据集
  currentKnowledgeBase: null, // 当前选中的知识库
  datasetFormats: [],   // 数据集格式列表
  datasetStats: {},     // 数据集统计信息
  knowledgeBaseStats: {}, // 知识库统计信息
  loading: false,       // 加载状态
  error: null           // 错误信息
}

const getters = {
  datasetById: state => id => {
    return state.datasets.find(dataset => dataset.id === id) || null
  },
  knowledgeBaseById: state => id => {
    return state.knowledgeBases.find(kb => kb.id === id) || null
  },
  datasetList: state => state.datasets,
  knowledgeBaseList: state => state.knowledgeBases,
  totalDatasets: state => state.datasets.length,
  totalKnowledgeBases: state => state.knowledgeBases.length,
  datasetCount: state => state.datasets.length,
  knowledgeBaseCount: state => state.knowledgeBases.length,
  hasDatasets: state => state.datasets.length > 0,
  hasKnowledgeBases: state => state.knowledgeBases.length > 0,
  datasetFormats: state => state.datasetFormats
}

const mutations = {
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  },
  SET_DATASETS(state, datasets) {
    state.datasets = datasets
  },
  SET_KNOWLEDGE_BASES(state, knowledgeBases) {
    state.knowledgeBases = knowledgeBases
  },
  SET_CURRENT_DATASET(state, dataset) {
    state.currentDataset = dataset
  },
  SET_CURRENT_KNOWLEDGE_BASE(state, knowledgeBase) {
    state.currentKnowledgeBase = knowledgeBase
  },
  SET_DATASET_FORMATS(state, formats) {
    // 使用Set去重
    let uniqueFormats = new Set()
    
    if (Array.isArray(formats)) {
      formats.forEach(format => {
        if (typeof format === 'string') {
          uniqueFormats.add(format)
        } else if (format && format.value) {
          uniqueFormats.add(format.value)
        }
      })
    } else if (formats && typeof formats === 'object') {
      if (formats.results && Array.isArray(formats.results)) {
        formats.results.forEach(format => uniqueFormats.add(format))
      } else if (formats.data && Array.isArray(formats.data)) {
        formats.data.forEach(format => uniqueFormats.add(format))
      } else {
        Object.values(formats).forEach(format => uniqueFormats.add(format))
      }
    }
    
    // 转换为数组并排序
    state.datasetFormats = Array.from(uniqueFormats).sort()
  },
  SET_DATASET_STATS(state, stats) {
    state.datasetStats = stats
  },
  SET_KNOWLEDGE_BASE_STATS(state, stats) {
    state.knowledgeBaseStats = stats
  },
  ADD_DATASET(state, dataset) {
    state.datasets.unshift(dataset)
  },
  UPDATE_DATASET(state, dataset) {
    const index = state.datasets.findIndex(d => d.id === dataset.id)
    if (index !== -1) {
      state.datasets.splice(index, 1, dataset)
      // 如果当前选中的是这个数据集，也更新当前选中的数据集
      if (state.currentDataset && state.currentDataset.id === dataset.id) {
        state.currentDataset = dataset
      }
    }
  },
  REMOVE_DATASET(state, datasetId) {
    state.datasets = state.datasets.filter(d => d.id !== datasetId)
    // 如果当前选中的是这个数据集，清除选中状态
    if (state.currentDataset && state.currentDataset.id === datasetId) {
      state.currentDataset = null
    }
  },
  ADD_KNOWLEDGE_BASE(state, knowledgeBase) {
    state.knowledgeBases.unshift(knowledgeBase)
  },
  UPDATE_KNOWLEDGE_BASE(state, knowledgeBase) {
    const index = state.knowledgeBases.findIndex(kb => kb.id === knowledgeBase.id)
    if (index !== -1) {
      state.knowledgeBases.splice(index, 1, knowledgeBase)
      // 如果当前选中的是这个知识库，也更新当前选中的知识库
      if (state.currentKnowledgeBase && state.currentKnowledgeBase.id === knowledgeBase.id) {
        state.currentKnowledgeBase = knowledgeBase
      }
    }
  },
  REMOVE_KNOWLEDGE_BASE(state, knowledgeBaseId) {
    state.knowledgeBases = state.knowledgeBases.filter(kb => kb.id !== knowledgeBaseId)
    // 如果当前选中的是这个知识库，清除选中状态
    if (state.currentKnowledgeBase && state.currentKnowledgeBase.id === knowledgeBaseId) {
      state.currentKnowledgeBase = null
    }
  }
}

const actions = {
  // 获取数据集列表
  async fetchDatasets({ commit }, params = {}) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.getDatasets(params)
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
      console.error('获取数据集错误:', error)
      commit('SET_ERROR', error.message || '获取数据集失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取数据集详情
  async fetchDatasetDetail({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.getDatasetDetail(id)
      console.log('数据集详情API响应:', response)
      
      const dataset = response.data || response
      commit('SET_CURRENT_DATASET', dataset)
      return dataset
    } catch (error) {
      console.error('获取数据集详情失败:', error)
      commit('SET_ERROR', error.message || '获取数据集详情失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建数据集
  async createDataset({ commit }, { data, file, onProgress }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.createDataset(data, file, onProgress)
      const dataset = response.data || response
      commit('ADD_DATASET', dataset)
      return dataset
    } catch (error) {
      console.error('创建数据集失败:', error)
      commit('SET_ERROR', error.message || '创建数据集失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新数据集
  async updateDataset({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.updateDataset(id, data)
      const dataset = response.data || response
      commit('UPDATE_DATASET', dataset)
      return dataset
    } catch (error) {
      console.error('更新数据集失败:', error)
      commit('SET_ERROR', error.message || '更新数据集失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除数据集
  async deleteDataset({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      await dataCenter.deleteDataset(id)
      commit('REMOVE_DATASET', id)
      return true
    } catch (error) {
      console.error('删除数据集失败:', error)
      commit('SET_ERROR', error.message || '删除数据集失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取数据集格式列表
  async fetchDatasetFormats({ commit }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.getDatasetFormats()
      console.log('数据集格式API原始响应:', response)
      
      // 处理API响应数据
      let formats = []
      if (response && response.results) {
        formats = response.results
      } else if (Array.isArray(response)) {
        formats = response
      } else if (response && response.data) {
        formats = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      console.log('处理后的格式数据:', formats)
      commit('SET_DATASET_FORMATS', formats)
      return formats
    } catch (error) {
      console.error('获取数据集格式失败:', error)
      commit('SET_ERROR', error.message || '获取数据集格式失败')
      // 设置默认格式作为备选
      const defaultFormats = ['csv', 'json', 'txt']
      commit('SET_DATASET_FORMATS', defaultFormats)
      return defaultFormats
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取数据集统计信息
  async fetchDatasetStats({ commit }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.getDatasetStats()
      commit('SET_DATASET_STATS', response)
      return response
    } catch (error) {
      commit('SET_ERROR', error.message || '获取数据集统计信息失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 切换数据集公开状态
  async toggleDatasetPublic({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.toggleDatasetPublic(id)
      commit('UPDATE_DATASET', response)
      return response
    } catch (error) {
      commit('SET_ERROR', error.message || '切换数据集公开状态失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取知识库列表
  async fetchKnowledgeBases({ commit }, params = {}) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.getKnowledgeBases(params)
      console.log('知识库API响应:', response)
      
      // 处理API响应数据
      let knowledgeBases = []
      if (response && response.results) {
        knowledgeBases = response.results
      } else if (Array.isArray(response)) {
        knowledgeBases = response
      } else if (response && response.data) {
        knowledgeBases = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      commit('SET_KNOWLEDGE_BASES', knowledgeBases)
      return knowledgeBases
    } catch (error) {
      console.error('获取知识库错误:', error)
      commit('SET_ERROR', error.message || '获取知识库失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取知识库详情
  async fetchKnowledgeBaseDetail({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.getKnowledgeBaseDetail(id)
      console.log('知识库详情API响应:', response)
      
      const knowledgeBase = response.data || response
      commit('SET_CURRENT_KNOWLEDGE_BASE', knowledgeBase)
      return knowledgeBase
    } catch (error) {
      console.error('获取知识库详情失败:', error)
      commit('SET_ERROR', error.message || '获取知识库详情失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建知识库
  async createKnowledgeBase({ commit }, data) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.createKnowledgeBase(data)
      const knowledgeBase = response.data || response
      commit('ADD_KNOWLEDGE_BASE', knowledgeBase)
      return knowledgeBase
    } catch (error) {
      console.error('创建知识库失败:', error)
      commit('SET_ERROR', error.message || '创建知识库失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新知识库
  async updateKnowledgeBase({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.updateKnowledgeBase(id, data)
      const knowledgeBase = response.data || response
      commit('UPDATE_KNOWLEDGE_BASE', knowledgeBase)
      return knowledgeBase
    } catch (error) {
      console.error('更新知识库失败:', error)
      commit('SET_ERROR', error.message || '更新知识库失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除知识库
  async deleteKnowledgeBase({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      await dataCenter.deleteKnowledgeBase(id)
      commit('REMOVE_KNOWLEDGE_BASE', id)
      return true
    } catch (error) {
      console.error('删除知识库失败:', error)
      commit('SET_ERROR', error.message || '删除知识库失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取知识库统计信息
  async fetchKnowledgeBaseStats({ commit }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.getKnowledgeBaseStats()
      commit('SET_KNOWLEDGE_BASE_STATS', response)
      return response
    } catch (error) {
      commit('SET_ERROR', error.message || '获取知识库统计信息失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 切换知识库公开状态
  async toggleKnowledgeBasePublic({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.toggleKnowledgeBasePublic(id)
      commit('UPDATE_KNOWLEDGE_BASE', response)
      return response
    } catch (error) {
      commit('SET_ERROR', error.message || '切换知识库公开状态失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 为知识库创建向量索引
  async createVectorIndex({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await dataCenter.createVectorIndex(id)
      commit('UPDATE_KNOWLEDGE_BASE', response)
      return response
    } catch (error) {
      commit('SET_ERROR', error.message || '创建向量索引失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取数据集预览数据
  async fetchDatasetPreview({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      // 模拟数据集预览API调用
      const response = await new Promise(resolve => {
        setTimeout(() => {
          resolve({
            data: [
              { id: 1, name: '示例数据1', value: 100, category: 'A' },
              { id: 2, name: '示例数据2', value: 200, category: 'B' },
              { id: 3, name: '示例数据3', value: 150, category: 'A' }
            ]
          })
        }, 500)
      })
      return response
    } catch (error) {
      console.error('获取数据集预览失败:', error)
      commit('SET_ERROR', error.message || '获取数据集预览失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取数据集使用情况
  async fetchDatasetUsage({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      // 模拟数据集使用情况API调用
      const response = await new Promise(resolve => {
        setTimeout(() => {
          resolve({
            data: [
              {
                id: 1,
                type: '训练',
                name: '文本分类训练任务',
                created_at: new Date().toISOString(),
                status: 'completed'
              },
              {
                id: 2,
                type: '评测',
                name: '模型性能评测',
                created_at: new Date().toISOString(),
                status: 'running'
              }
            ]
          })
        }, 500)
      })
      return response
    } catch (error) {
      console.error('获取数据集使用情况失败:', error)
      commit('SET_ERROR', error.message || '获取数据集使用情况失败')
      throw error
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