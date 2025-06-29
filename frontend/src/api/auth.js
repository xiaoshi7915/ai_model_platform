// 认证相关的API服务
// 包括登录、注册、登出和获取用户信息

import request from '@/utils/request'

/**
 * 用户登录
 * @param {Object} credentials - 登录凭证
 * @param {string} credentials.username - 用户名
 * @param {string} credentials.password - 密码
 * @returns {Promise} - 返回登录结果
 */
const login = (credentials) => {
  console.log('发送登录请求:', credentials);
  return request({
    url: '/auth/login/',
    method: 'post',
    data: credentials
  }).then(response => {
    console.log('登录响应原始数据:', response);
    // 确保返回正确的数据格式
    if (response.data && response.data.access) {
      return response.data;
    } else if (response.access) {
      return response;
    } else {
      console.error('响应中没有识别到access token:', response);
      throw new Error('登录响应格式不正确');
    }
  }).catch(error => {
    console.error('登录请求错误:', error);
    throw error;
  });
}

/**
 * 用户注册
 * @param {Object} userData - 用户数据
 * @param {string} userData.username - 用户名
 * @param {string} userData.email - 邮箱
 * @param {string} userData.password - 密码
 * @param {string} userData.password2 - 确认密码
 * @returns {Promise} - 返回注册结果
 */
const register = (userData) => {
  console.log('发送注册请求:', userData);
  return request({
    url: '/auth/register/',
    method: 'post',
    data: userData
  }).then(response => {
    console.log('注册响应原始数据:', response);
    // 确保返回正确的数据格式
    if (response.data && response.data.access) {
      return response.data;
    } else if (response.access) {
      return response;
    } else {
      console.error('响应中没有识别到access token:', response);
      throw new Error('注册响应格式不正确');
    }
  }).catch(error => {
    console.error('注册请求错误:', error);
    throw error;
  });
}

/**
 * 刷新Token
 * @param {Object} refreshData - 刷新数据
 * @param {string} refreshData.refresh - 刷新令牌
 * @returns {Promise} - 返回新的访问令牌
 */
const refreshToken = (refreshData) => {
  console.log('发送刷新Token请求:', refreshData);
  return request({
    url: '/auth/refresh/',
    method: 'post',
    data: refreshData
  }).then(response => {
    console.log('刷新Token响应:', response);
    // 确保返回正确的数据格式
    if (response.data && response.data.access) {
      return response.data;
    } else if (response.access) {
      return response;
    } else {
      console.error('响应中没有识别到access token:', response);
      throw new Error('刷新Token响应格式不正确');
    }
  }).catch(error => {
    console.error('刷新Token请求错误:', error);
    throw error;
  });
}

/**
 * 用户登出
 * @returns {Promise} - 返回登出结果
 */
const logout = () => {
  return request({
    url: '/auth/logout/',
    method: 'post'
  })
}

/**
 * 获取用户信息
 * @returns {Promise} - 返回用户信息
 */
const getProfile = () => {
  return request({
    url: '/auth/profile/',
    method: 'get'
  })
}

/**
 * 更新用户信息
 * @param {Object} userData - 用户数据
 * @returns {Promise} - 返回更新结果
 */
const updateProfile = (userData) => {
  return request({
    url: '/auth/profile/',
    method: 'put',
    data: userData
  })
}

export default {
  login,
  register,
  logout,
  getProfile,
  updateProfile,
  refreshToken  // 导出刷新Token方法
} 