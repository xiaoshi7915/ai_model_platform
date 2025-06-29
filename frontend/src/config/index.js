// 全局配置文件
// 包含API基础URL和其他全局配置

// API版本号 - 后端已经不需要显式指定版本号
export const API_VERSION = ''

// API基础URL，优先使用环境变量中的配置
export const API_BASE_URL = process.env.VUE_APP_API_URL || ``

// 默认请求超时时间（毫秒）
export const REQUEST_TIMEOUT = 30000

// 默认分页大小
export const DEFAULT_PAGE_SIZE = 10

// 默认语言
export const DEFAULT_LANGUAGE = 'zh-CN'

// 默认主题
export const DEFAULT_THEME = 'light'

// 导出默认配置对象
export default {
  baseURL: API_BASE_URL,
  apiVersion: API_VERSION,
  timeout: REQUEST_TIMEOUT,
  pageSize: DEFAULT_PAGE_SIZE,
  language: DEFAULT_LANGUAGE,
  theme: DEFAULT_THEME
} 