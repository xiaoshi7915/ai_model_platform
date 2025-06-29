import axios from 'axios'

// 修改数据集API路径 - 从训练中心移到数据中心
const api = {
  getDatasets: '/data-center/datasets/',
  createDataset: '/data-center/datasets/',
  updateDataset: (id) => `/data-center/datasets/${id}/`,
  deleteDataset: (id) => `/data-center/datasets/${id}/`
}

// 缓存控制
const CACHE_EXPIRY = 5 * 60 * 1000; // 5分钟缓存过期时间
let lastFetchTime = 0;
let cachedDatasets = null; 