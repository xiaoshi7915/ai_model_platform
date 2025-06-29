import axios from 'axios'

// 修改训练任务API路径 - 移除重复的api/v1前缀
const api = {
  getTrainingJobs: '/training-center/training-jobs/',
  createTrainingJob: '/training-center/training-jobs/',
  updateTrainingJob: (id) => `/training-center/training-jobs/${id}/`,
  deleteTrainingJob: (id) => `/training-center/training-jobs/${id}/`,
  getTrainingJobLogs: (id) => `/training-center/training-jobs/${id}/logs/`,
  stopTrainingJob: (id) => `/training-center/training-jobs/${id}/stop/`
}

// 缓存控制
const CACHE_EXPIRY = 2 * 60 * 1000; // 2分钟缓存过期时间（训练任务需要更频繁更新）
let lastFetchTime = 0;
let cachedJobs = null;

// 初始状态
const state = {
  trainingJobs: [], // 训练任务列表
  loading: false,   // 加载状态
  error: null       // 错误信息
}

// getter
const getters = {
  // 获取所有训练任务
  allTrainingJobs: state => state.trainingJobs,
  
  // 通过ID获取训练任务
  getTrainingJobById: state => id => {
    return state.trainingJobs.find(job => job.id === id)
  },
  
  // 获取加载状态
  isLoading: state => state.loading,
  
  // 获取错误信息
  getError: state => state.error
}

// actions
const actions = {
  // 获取所有训练任务
  async fetchTrainingJobs({ commit }, forceRefresh = false) {
    // 检查缓存是否有效（除非强制刷新）
    const now = Date.now();
    if (!forceRefresh && cachedJobs && (now - lastFetchTime < CACHE_EXPIRY)) {
      console.log('使用缓存的训练任务数据');
      commit('SET_TRAINING_JOBS', cachedJobs);
      return cachedJobs;
    }
    
    commit('SET_LOADING', true);
    commit('SET_ERROR', null);
    
    // 设置最大重试次数
    const maxRetries = 3;
    let retries = 0;
    
    const fetchWithRetry = async () => {
      try {
        // 使用更长的超时时间
        const response = await axios.get(api.getTrainingJobs, { timeout: 60000 });
        const data = response.data || [];
        
        // 更新缓存
        cachedJobs = data;
        lastFetchTime = now;
        
        commit('SET_TRAINING_JOBS', data);
        return data;
      } catch (error) {
        if (error.code === 'ECONNABORTED' && retries < maxRetries) {
          // 超时错误，进行重试
          retries++;
          console.log(`训练任务获取超时，正在进行第${retries}次重试...`);
          return fetchWithRetry();
        }
        
        // 达到最大重试次数或其他错误
        commit('SET_ERROR', error.message || '获取训练任务失败');
        
        // 如果是超时错误，返回空数组或缓存数据
        if (error.code === 'ECONNABORTED') {
          console.warn('训练任务获取超时，使用缓存或返回空数组');
          
          // 如果有缓存数据，使用缓存
          if (cachedJobs) {
            commit('SET_TRAINING_JOBS', cachedJobs);
            return cachedJobs;
          }
          
          // 否则返回空数组
          commit('SET_TRAINING_JOBS', []);
          return [];
        }
        
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    };
    
    return fetchWithRetry();
  },
  
  // 获取单个训练任务详情
  async fetchTrainingJob({ commit, state }, id) {
    // 先从本地状态查找
    const existingJob = state.trainingJobs.find(job => job.id === id);
    if (existingJob) {
      return existingJob;
    }
    
    commit('SET_LOADING', true);
    try {
      const response = await axios.get(api.updateTrainingJob(id));
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message || '获取训练任务详情失败');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },
  
  // 创建训练任务
  async createTrainingJob({ commit, dispatch }, jobData) {
    commit('SET_LOADING', true);
    try {
      const response = await axios.post(api.createTrainingJob, jobData);
      
      // 创建成功后清除缓存并重新获取列表
      cachedJobs = null;
      await dispatch('fetchTrainingJobs', true);
      
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message || '创建训练任务失败');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },
  
  // 更新训练任务
  async updateTrainingJob({ commit, dispatch }, jobData) {
    commit('SET_LOADING', true);
    try {
      const response = await axios.put(api.updateTrainingJob(jobData.id), jobData);
      
      // 更新成功后清除缓存并重新获取列表
      cachedJobs = null;
      await dispatch('fetchTrainingJobs', true);
      
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message || '更新训练任务失败');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },
  
  // 删除训练任务
  async deleteTrainingJob({ commit, dispatch }, id) {
    commit('SET_LOADING', true);
    try {
      await axios.delete(api.deleteTrainingJob(id));
      
      // 删除成功后清除缓存并重新获取列表
      cachedJobs = null;
      await dispatch('fetchTrainingJobs', true);
      
      return true;
    } catch (error) {
      commit('SET_ERROR', error.message || '删除训练任务失败');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },
  
  // 获取训练任务日志
  async fetchTrainingJobLogs({ commit }, id) {
    commit('SET_LOADING', true);
    try {
      const response = await axios.get(api.getTrainingJobLogs(id));
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message || '获取训练任务日志失败');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },
  
  // 停止训练任务
  async stopTrainingJob({ commit, dispatch }, id) {
    commit('SET_LOADING', true);
    try {
      const response = await axios.post(api.stopTrainingJob(id));
      
      // 操作成功后清除缓存并重新获取列表
      cachedJobs = null;
      await dispatch('fetchTrainingJobs', true);
      
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message || '停止训练任务失败');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  }
}

// mutations
const mutations = {
  // 设置训练任务列表
  SET_TRAINING_JOBS(state, trainingJobs) {
    state.trainingJobs = trainingJobs
  },
  
  // 设置加载状态
  SET_LOADING(state, status) {
    state.loading = status
  },
  
  // 设置错误信息
  SET_ERROR(state, error) {
    state.error = error
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
} 