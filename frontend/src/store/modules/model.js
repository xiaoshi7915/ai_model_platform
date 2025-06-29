import api from '@/api'

const state = {
  models: [],
  currentModel: null
}

const mutations = {
  SET_MODELS(state, models) {
    state.models = models
  },
  SET_CURRENT_MODEL(state, model) {
    state.currentModel = model
  },
  ADD_MODEL(state, model) {
    state.models.push(model)
  },
  UPDATE_MODEL(state, updatedModel) {
    const index = state.models.findIndex(model => model.id === updatedModel.id)
    if (index !== -1) {
      state.models.splice(index, 1, updatedModel)
    }
  },
  REMOVE_MODEL(state, modelId) {
    state.models = state.models.filter(model => model.id !== modelId)
  }
}

const actions = {
  // 获取模型列表
  getModels({ commit }) {
    return new Promise((resolve, reject) => {
      api.model.getModels()
        .then(response => {
          commit('SET_MODELS', response)
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  
  // 获取模型详情
  getModelDetail({ commit }, id) {
    return new Promise((resolve, reject) => {
      api.model.getModelDetail(id)
        .then(response => {
          commit('SET_CURRENT_MODEL', response)
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  
  // 创建模型
  createModel({ commit }, data) {
    return new Promise((resolve, reject) => {
      api.model.createModel(data)
        .then(response => {
          commit('ADD_MODEL', response)
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  
  // 更新模型
  updateModel({ commit }, { id, data }) {
    return new Promise((resolve, reject) => {
      api.model.updateModel(id, data)
        .then(response => {
          commit('UPDATE_MODEL', response)
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  
  // 删除模型
  deleteModel({ commit }, id) {
    return new Promise((resolve, reject) => {
      api.model.deleteModel(id)
        .then(() => {
          commit('REMOVE_MODEL', id)
          resolve()
        })
        .catch(error => {
          reject(error)
        })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 