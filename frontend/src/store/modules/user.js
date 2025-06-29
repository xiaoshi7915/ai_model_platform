import api from '@/api'

const state = {
  token: localStorage.getItem('token') || '',
  refreshToken: localStorage.getItem('refreshToken') || '',
  userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
  loading: false,
  error: null
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
    localStorage.setItem('token', token)
  },
  SET_REFRESH_TOKEN(state, refreshToken) {
    state.refreshToken = refreshToken
    localStorage.setItem('refreshToken', refreshToken)
  },
  SET_USER_INFO(state, userInfo) {
    state.userInfo = userInfo
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
  },
  CLEAR_USER(state) {
    state.token = ''
    state.refreshToken = ''
    state.userInfo = {}
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('userInfo')
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  }
}

const actions = {
  // 登录
  async login({ commit }, credentials) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      console.log('Vuex login action 开始:', credentials)
      const response = await api.auth.login(credentials)
      console.log('Vuex login action 响应:', response)
      
      // 检查响应格式
      if (response && response.access) {
        commit('SET_TOKEN', response.access)
        
        // 保存refresh token，如果有的话
        if (response.refresh) {
          commit('SET_REFRESH_TOKEN', response.refresh)
        }
        
        return response
      } else {
        console.error('响应中没有 access token:', response)
        throw new Error('登录响应格式不正确')
      }
    } catch (error) {
      console.error('Vuex login action 错误:', error)
      commit('SET_ERROR', error.message || '登录失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 注册
  async register({ commit }, userData) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      console.log('注册开始:', userData)
      const response = await api.auth.register(userData)
      console.log('注册响应:', response)
      
      // 检查响应格式
      if (response && response.access) {
        commit('SET_TOKEN', response.access)
        
        // 保存refresh token，如果有的话
        if (response.refresh) {
          commit('SET_REFRESH_TOKEN', response.refresh)
        }
        
        return response
      } else {
        console.error('响应中没有 access token:', response)
        throw new Error('注册响应格式不正确')
      }
    } catch (error) {
      console.error('注册错误:', error)
      commit('SET_ERROR', error.message || '注册失败')
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取用户信息
  getUserInfo({ commit }) {
    return new Promise((resolve, reject) => {
      api.auth.getProfile()
        .then(response => {
          commit('SET_USER_INFO', response)
          resolve(response)
        })
        .catch(error => {
          reject(error)
        })
    })
  },
  
  // 刷新Token
  refreshToken({ commit, state }) {
    return new Promise((resolve, reject) => {
      // 如果没有refresh token，则直接失败
      if (!state.refreshToken) {
        return reject(new Error('没有可用的刷新令牌'));
      }
      
      // 发起刷新请求
      api.auth.refreshToken({ refresh: state.refreshToken })
        .then(response => {
          if (response && response.access) {
            commit('SET_TOKEN', response.access);
            
            // 如果返回了新的refresh token，更新它
            if (response.refresh) {
              commit('SET_REFRESH_TOKEN', response.refresh);
            }
            
            resolve(response);
          } else {
            reject(new Error('刷新令牌响应格式不正确'));
          }
        })
        .catch(error => {
          console.error('刷新令牌失败:', error);
          // 清除token，下次需重新登录
          commit('CLEAR_USER');
          reject(error);
        });
    });
  },
  
  // 登出
  logout({ commit }) {
    return new Promise((resolve, reject) => {
      api.auth.logout()
        .then(() => {
          commit('CLEAR_USER')
          resolve()
        })
        .catch(error => {
          // 即使API登出失败，也要清除本地存储的用户信息
          commit('CLEAR_USER')
          resolve() // 仍然认为登出成功
        })
    })
  },
  
  // 重置Token (不需要API调用)
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('CLEAR_USER')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 