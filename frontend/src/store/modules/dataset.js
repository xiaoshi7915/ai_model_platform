import api from '@/api'

const state = {
  datasets: [],
  currentDataset: null
}

const mutations = {
  SET_DATASETS(state, datasets) {
    state.datasets = datasets
  },
  SET_CURRENT_DATASET(state, dataset) {
    state.currentDataset = dataset
  },
  ADD_DATASET(state, dataset) {
    state.datasets.push(dataset)
  },
  UPDATE_DATASET(state, updatedDataset) {
    const index = state.datasets.findIndex(dataset => dataset.id === updatedDataset.id)
    if (index !== -1) {
      state.datasets.splice(index, 1, updatedDataset)
    }
  },
  REMOVE_DATASET(state, datasetId) {
    state.datasets = state.datasets.filter(dataset => dataset.id !== datasetId)
  }
}

const actions = {
  // 获取数据集列表
  getDatasets({ commit }) {
    return new Promise((resolve, reject) => {
      api.dataset.getDatasets()
        .then(response => {
          commit('SET_DATASETS', response)
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  
  // 获取数据集详情
  getDatasetDetail({ commit }, id) {
    return new Promise((resolve, reject) => {
      api.dataset.getDatasetDetail(id)
        .then(response => {
          commit('SET_CURRENT_DATASET', response)
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  
  // 创建数据集
  createDataset({ commit }, data) {
    return new Promise((resolve, reject) => {
      api.dataset.createDataset(data)
        .then(response => {
          commit('ADD_DATASET', response)
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  
  // 更新数据集
  updateDataset({ commit }, { id, data }) {
    return new Promise((resolve, reject) => {
      api.dataset.updateDataset(id, data)
        .then(response => {
          commit('UPDATE_DATASET', response)
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  
  // 删除数据集
  deleteDataset({ commit }, id) {
    return new Promise((resolve, reject) => {
      api.dataset.deleteDataset(id)
        .then(() => {
          commit('REMOVE_DATASET', id)
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