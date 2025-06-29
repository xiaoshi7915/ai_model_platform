// 训练中心Vuex模块
import api from '@/api'

const state = {
  models: [], // 模型列表
  currentModel: null, // 当前模型
  dockerImages: [], // Docker镜像列表
  currentDockerImage: null, // 当前Docker镜像
  trainingJobs: [], // 训练任务列表
  currentTrainingJob: null, // 当前训练任务
  currentPage: 1,
  pageSize: 10,
  total: 0,
  loading: false, // 加载状态
  error: null // 错误信息
}

const mutations = {
  // 设置模型列表
  SET_MODELS(state, models) {
    state.models = models || []
  },
  
  // 设置当前模型
  SET_CURRENT_MODEL(state, model) {
    state.currentModel = model
  },
  
  // 设置Docker镜像列表
  SET_DOCKER_IMAGES(state, images) {
    state.dockerImages = images || []
  },
  
  // 设置当前Docker镜像
  SET_CURRENT_DOCKER_IMAGE(state, dockerImage) {
    state.currentDockerImage = dockerImage
  },
  
  // 设置训练任务列表
  SET_TRAINING_JOBS(state, jobs) {
    state.trainingJobs = jobs || []
  },
  
  // 设置当前训练任务
  SET_CURRENT_TRAINING_JOB(state, trainingJob) {
    state.currentTrainingJob = trainingJob
  },
  
  // 设置加载状态
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  
  // 设置错误信息
  SET_ERROR(state, error) {
    state.error = error
  },
  
  // 添加模型
  ADD_MODEL(state, model) {
    state.models.push(model)
  },
  
  // 更新模型
  UPDATE_MODEL(state, model) {
    const index = state.models.findIndex(m => m.id === model.id)
    if (index !== -1) {
      state.models.splice(index, 1, model)
    }
  },
  
  // 删除模型
  DELETE_MODEL(state, modelId) {
    state.models = state.models.filter(m => m.id !== modelId)
  },
  
  // 添加Docker镜像
  ADD_DOCKER_IMAGE(state, image) {
    state.dockerImages.push(image)
  },
  
  // 更新Docker镜像
  UPDATE_DOCKER_IMAGE(state, image) {
    const index = state.dockerImages.findIndex(i => i.id === image.id)
    if (index !== -1) {
      state.dockerImages.splice(index, 1, image)
    }
  },
  
  // 删除Docker镜像
  DELETE_DOCKER_IMAGE(state, imageId) {
    state.dockerImages = state.dockerImages.filter(i => i.id !== imageId)
  },
  
  // 添加训练任务
  ADD_TRAINING_JOB(state, job) {
    state.trainingJobs.push(job)
  },
  
  // 更新训练任务
  UPDATE_TRAINING_JOB(state, job) {
    const index = state.trainingJobs.findIndex(j => j.id === job.id)
    if (index !== -1) {
      state.trainingJobs.splice(index, 1, job)
    }
  },
  
  // 删除训练任务
  DELETE_TRAINING_JOB(state, jobId) {
    state.trainingJobs = state.trainingJobs.filter(j => j.id !== jobId)
  }
}

const actions = {
  // 获取模型列表
  async fetchModels({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.trainingCenter.getModels()
      console.log('Models API Response:', response)
      
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
      commit('SET_ERROR', null)
      return models
    } catch (error) {
      console.error('获取模型列表失败:', error)
      commit('SET_ERROR', error.message || '获取模型列表失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取模型详情
  async fetchModelDetail({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const model = await api.training.getModelDetail(id)
      commit('SET_CURRENT_MODEL', model)
      commit('SET_ERROR', null)
      return model
    } catch (error) {
      console.error('获取模型详情失败:', error)
      commit('SET_ERROR', '获取模型详情失败')
      return null
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建模型
  async createModel({ commit }, model) {
    commit('SET_LOADING', true)
    try {
      const response = await api.trainingCenter.createModel(model)
      commit('ADD_MODEL', response.data || response)
      return response.data || response
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新模型
  async updateModel({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.trainingCenter.updateModel(id, data)
      commit('UPDATE_MODEL', response.data || response)
      return response.data || response
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除模型
  async deleteModel({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await api.trainingCenter.deleteModel(id)
      commit('DELETE_MODEL', id)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 训练模型
  async trainModel({ commit, dispatch }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const result = await api.training.trainModel(id, data)
      // 重新获取模型详情
      await dispatch('fetchModelDetail', id)
      commit('SET_ERROR', null)
      return result
    } catch (error) {
      console.error('训练模型失败:', error)
      commit('SET_ERROR', '训练模型失败')
      return null
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取模型版本列表
  async fetchModelVersions({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const versions = await api.training.getModelVersions(id)
      commit('SET_ERROR', null)
      return versions
    } catch (error) {
      console.error('获取模型版本列表失败:', error)
      commit('SET_ERROR', '获取模型版本列表失败')
      return []
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取Docker镜像列表
  async fetchDockerImages({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.trainingCenter.getDockerImages()
      console.log('Docker Images API Response:', response)
      
      // 处理API响应数据
      let images = []
      if (response && response.results) {
        images = response.results
      } else if (Array.isArray(response)) {
        images = response
      } else if (response && response.data) {
        images = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      commit('SET_DOCKER_IMAGES', images)
      commit('SET_ERROR', null)
      return images
    } catch (error) {
      console.error('获取Docker镜像列表失败:', error)
      commit('SET_ERROR', error.message || '获取Docker镜像列表失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取Docker镜像详情
  async fetchDockerImageDetail({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const dockerImage = await api.training.getDockerImageDetail(id)
      commit('SET_CURRENT_DOCKER_IMAGE', dockerImage)
      commit('SET_ERROR', null)
      return dockerImage
    } catch (error) {
      console.error('获取Docker镜像详情失败:', error)
      commit('SET_ERROR', '获取Docker镜像详情失败')
      return null
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建Docker镜像
  async createDockerImage({ commit }, image) {
    commit('SET_LOADING', true)
    try {
      const response = await api.trainingCenter.createDockerImage(image)
      commit('ADD_DOCKER_IMAGE', response.data || response)
      return response.data || response
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新Docker镜像
  async updateDockerImage({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.trainingCenter.updateDockerImage(id, data)
      commit('UPDATE_DOCKER_IMAGE', response.data || response)
      return response.data || response
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除Docker镜像
  async deleteDockerImage({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await api.trainingCenter.deleteDockerImage(id)
      commit('DELETE_DOCKER_IMAGE', id)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取训练任务列表
  async fetchTrainingJobs({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.trainingCenter.getTrainingTasks()
      console.log('Training Jobs API Response:', response)
      
      // 处理API响应数据
      let jobs = []
      if (response && response.results) {
        jobs = response.results
      } else if (Array.isArray(response)) {
        jobs = response
      } else if (response && response.data) {
        jobs = Array.isArray(response.data) ? response.data : response.data.results || []
      }
      
      commit('SET_TRAINING_JOBS', jobs)
      commit('SET_ERROR', null)
      return jobs
    } catch (error) {
      console.error('获取训练任务列表失败:', error)
      commit('SET_ERROR', error.message || '获取训练任务列表失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取训练任务详情
  async fetchTrainingJobDetail({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const trainingJob = await api.training.getTrainingJobDetail(id)
      commit('SET_CURRENT_TRAINING_JOB', trainingJob)
      commit('SET_ERROR', null)
      return trainingJob
    } catch (error) {
      console.error('获取训练任务详情失败:', error)
      commit('SET_ERROR', '获取训练任务详情失败')
      return null
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 取消训练任务
  async cancelTrainingJob({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.trainingCenter.stopTrainingTask(id)
      commit('UPDATE_TRAINING_JOB', response.data || response)
      return response.data || response
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建训练任务
  async createTrainingJob({ commit }, job) {
    commit('SET_LOADING', true)
    try {
      const response = await api.trainingCenter.createTrainingTask(job)
      commit('ADD_TRAINING_JOB', response.data || response)
      return response.data || response
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新训练任务
  async updateTrainingJob({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.trainingCenter.updateTrainingTask(id, data)
      commit('UPDATE_TRAINING_JOB', response.data || response)
      return response.data || response
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除训练任务
  async deleteTrainingJob({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await api.trainingCenter.deleteTrainingJob(id)
      commit('DELETE_TRAINING_JOB', id)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取知识库在训练中心的使用情况
  async fetchKnowledgeBaseUsage({ commit }, knowledgeBaseId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      // 模拟获取知识库在训练任务中的使用情况
      const response = await new Promise(resolve => {
        setTimeout(() => {
          resolve({
            data: [
              {
                id: 1,
                name: '基于知识库的模型训练',
                created_at: new Date().toISOString(),
                status: 'completed',
                model_name: 'text-classification-v1'
              },
              {
                id: 2,
                name: '知识增强训练任务',
                created_at: new Date().toISOString(),
                status: 'running',
                model_name: 'knowledge-enhanced-gpt'
              }
            ]
          })
        }, 300)
      })
      return response
    } catch (error) {
      console.error('获取知识库训练使用情况失败:', error)
      commit('SET_ERROR', error.message || '获取知识库训练使用情况失败')
      return { data: [] }
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const getters = {
  // 获取模型列表
  models: state => state.models,
  
  // 获取当前模型
  currentModel: state => state.currentModel,
  
  // 获取Docker镜像列表
  dockerImages: state => state.dockerImages,
  
  // 获取当前Docker镜像
  currentDockerImage: state => state.currentDockerImage,
  
  // 获取训练任务列表
  trainingJobs: state => state.trainingJobs,
  
  // 获取当前训练任务
  currentTrainingJob: state => state.currentTrainingJob,
  
  // 获取加载状态
  loading: state => state.loading,
  
  // 获取错误信息
  error: state => state.error,
  
  // 获取已完成的模型
  completedModels: state => state.models.filter(model => model.status === 'completed'),
  
  // 获取训练中的模型
  trainingModels: state => state.models.filter(model => model.status === 'training'),
  
  // 获取草稿模型
  draftModels: state => state.models.filter(model => model.status === 'draft')
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 