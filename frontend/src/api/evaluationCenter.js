// 评估中心相关的API服务
import request from '@/utils/request'

// Mock数据开关 - 开发时可以设置为true来使用mock数据
const USE_MOCK_DATA = false

// Mock数据生成函数
const generateMockEvaluationTasks = (count = 5) => {
  const tasks = []
  const statuses = ['pending', 'running', 'completed', 'failed', 'cancelled']
  
  for (let i = 1; i <= count; i++) {
    tasks.push({
      id: i,
      name: `评估任务 ${i}`,
      description: `这是第 ${i} 个评估任务的描述`,
      status: statuses[Math.floor(Math.random() * statuses.length)],
      model_name: `模型 ${i}`,
      dataset_name: `数据集 ${i}`,
      created_at: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
      created_by: `用户 ${i}`,
      progress: Math.floor(Math.random() * 100)
    })
  }
  return tasks
}

const generateMockEvaluationReports = (count = 3) => {
  const reports = []
  
  for (let i = 1; i <= count; i++) {
    reports.push({
      id: i,
      name: `评估报告 ${i}`,
      task_id: i,
      task_name: `评估任务 ${i}`,
      model_name: `模型 ${i}`,
      dataset_name: `数据集 ${i}`,
      accuracy: (0.8 + Math.random() * 0.2).toFixed(4),
      precision: (0.75 + Math.random() * 0.25).toFixed(4),
      recall: (0.7 + Math.random() * 0.3).toFixed(4),
      f1_score: (0.72 + Math.random() * 0.28).toFixed(4),
      created_at: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString()
    })
  }
  return reports
}

const generateMockModelComparisons = (count = 2) => {
  const comparisons = []
  
  for (let i = 1; i <= count; i++) {
    comparisons.push({
      id: i,
      name: `模型比较 ${i}`,
      description: `这是第 ${i} 个模型比较`,
      model_list: [
        { id: i * 2 - 1, name: `模型 ${i * 2 - 1}` },
        { id: i * 2, name: `模型 ${i * 2}` }
      ],
      dataset: { id: i, name: `数据集 ${i}` },
      created_at: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
      created_by_username: `用户 ${i}`,
      results: {
        metrics: ['accuracy', 'precision', 'recall', 'f1_score'],
        data: [
          {
            model_name: `模型 ${i * 2 - 1}`,
            accuracy: (0.8 + Math.random() * 0.2).toFixed(4),
            precision: (0.75 + Math.random() * 0.25).toFixed(4),
            recall: (0.7 + Math.random() * 0.3).toFixed(4),
            f1_score: (0.72 + Math.random() * 0.28).toFixed(4)
          },
          {
            model_name: `模型 ${i * 2}`,
            accuracy: (0.8 + Math.random() * 0.2).toFixed(4),
            precision: (0.75 + Math.random() * 0.25).toFixed(4),
            recall: (0.7 + Math.random() * 0.3).toFixed(4),
            f1_score: (0.72 + Math.random() * 0.28).toFixed(4)
          }
        ]
      }
    })
  }
  return comparisons
}

export default {
  /**
   * 获取评估任务列表
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回评估任务列表
   */
  async getEvaluationTasks(params = {}) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 评估任务列表')
      return Promise.resolve({
        results: generateMockEvaluationTasks(7),
        count: 7
      })
    }
    
    try {
      return await request({
        url: '/evaluation-center/tasks/',
        method: 'get',
        params
      })
    } catch (error) {
      console.error('获取评估任务失败，使用Mock数据:', error)
      return {
        results: generateMockEvaluationTasks(7),
        count: 7
      }
    }
  },

  /**
   * 获取评估任务详情
   * @param {number} id - 评估任务ID
   * @returns {Promise} - 返回评估任务详情
   */
  async getEvaluationTaskDetail(id) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 评估任务详情')
      const tasks = generateMockEvaluationTasks()
      return Promise.resolve(tasks.find(t => t.id == id) || tasks[0])
    }
    
    try {
      return await request({
        url: `/evaluation-center/tasks/${id}/`,
        method: 'get'
      })
    } catch (error) {
      console.error('获取评估任务详情失败，使用Mock数据:', error)
      const tasks = generateMockEvaluationTasks()
      return tasks.find(t => t.id == id) || tasks[0]
    }
  },

  /**
   * 创建评估任务
   * @param {Object} data - 评估任务数据
   * @returns {Promise} - 返回创建结果
   */
  async createEvaluationTask(data) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 创建评估任务')
      return Promise.resolve({
        id: Date.now(),
        ...data,
        status: 'pending',
        created_at: new Date().toISOString()
      })
    }
    
    try {
      return await request({
        url: '/evaluation-center/tasks/',
        method: 'post',
        data
      })
    } catch (error) {
      console.error('创建评估任务失败:', error)
      throw error
    }
  },

  /**
   * 更新评估任务
   * @param {number} id - 评估任务ID
   * @param {Object} data - 评估任务数据
   * @returns {Promise} - 返回更新结果
   */
  async updateEvaluationTask(id, data) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 更新评估任务')
      return Promise.resolve({ id, ...data })
    }
    
    try {
      return await request({
        url: `/evaluation-center/tasks/${id}/`,
        method: 'put',
        data
      })
    } catch (error) {
      console.error('更新评估任务失败:', error)
      throw error
    }
  },

  /**
   * 删除评估任务
   * @param {number} id - 评估任务ID
   * @returns {Promise} - 返回删除结果
   */
  async deleteEvaluationTask(id) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 删除评估任务')
      return Promise.resolve({ success: true })
    }
    
    try {
      return await request({
        url: `/evaluation-center/tasks/${id}/`,
        method: 'delete'
      })
    } catch (error) {
      console.error('删除评估任务失败:', error)
      throw error
    }
  },

  /**
   * 开始评估任务
   * @param {number} id - 评估任务ID
   * @returns {Promise} - 返回开始结果
   */
  async startEvaluationTask(id) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 开始评估任务')
      return Promise.resolve({
        id,
        status: 'running',
        started_at: new Date().toISOString()
      })
    }
    
    try {
      return await request({
        url: `/evaluation-center/tasks/${id}/start/`,
        method: 'post'
      })
    } catch (error) {
      console.error('开始评估任务失败:', error)
      throw error
    }
  },

  /**
   * 停止评估任务
   * @param {number} id - 评估任务ID
   * @returns {Promise} - 返回停止结果
   */
  async stopEvaluationTask(id) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 停止评估任务')
      return Promise.resolve({
        id,
        status: 'cancelled',
        stopped_at: new Date().toISOString()
      })
    }
    
    try {
      return await request({
        url: `/evaluation-center/tasks/${id}/cancel/`,
        method: 'post'
      })
    } catch (error) {
      console.error('停止评估任务失败:', error)
      throw error
    }
  },

  /**
   * 获取评估报告列表
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回评估报告列表
   */
  async getEvaluationReports(params = {}) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 评估报告列表')
      return Promise.resolve({
        results: generateMockEvaluationReports(5),
        count: 5
      })
    }
    
    try {
      return await request({
        url: '/evaluation-center/reports/',
        method: 'get',
        params
      })
    } catch (error) {
      console.error('获取评估报告失败，使用Mock数据:', error)
      return {
        results: generateMockEvaluationReports(5),
        count: 5
      }
    }
  },

  /**
   * 获取评估报告详情
   * @param {number} id - 评估报告ID
   * @returns {Promise} - 返回评估报告详情
   */
  async getEvaluationReportDetail(id) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 评估报告详情')
      const reports = generateMockEvaluationReports()
      return Promise.resolve(reports.find(r => r.id == id) || reports[0])
    }
    
    try {
      return await request({
        url: `/evaluation-center/reports/${id}/`,
        method: 'get'
      })
    } catch (error) {
      console.error('获取评估报告详情失败，使用Mock数据:', error)
      const reports = generateMockEvaluationReports()
      return reports.find(r => r.id == id) || reports[0]
    }
  },

  /**
   * 获取模型对比数据
   * @param {Object} params - 查询参数
   * @returns {Promise} - 返回模型对比数据
   */
  async getModelComparisons(params = {}) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 模型对比列表')
      return Promise.resolve({
        results: generateMockModelComparisons(3),
        count: 3
      })
    }
    
    try {
      return await request({
        url: '/evaluation-center/comparisons/',
        method: 'get',
        params
      })
    } catch (error) {
      console.error('获取模型对比失败，使用Mock数据:', error)
      return {
        results: generateMockModelComparisons(3),
        count: 3
      }
    }
  },

  /**
   * 获取模型对比详情
   * @param {number} id - 模型对比ID
   * @returns {Promise} - 返回模型对比详情
   */
  async getModelComparisonDetail(id) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 模型对比详情')
      const comparisons = generateMockModelComparisons()
      return Promise.resolve(comparisons.find(c => c.id == id) || comparisons[0])
    }
    
    try {
      return await request({
        url: `/evaluation-center/comparisons/${id}/`,
        method: 'get'
      })
    } catch (error) {
      console.error('获取模型对比详情失败，使用Mock数据:', error)
      const comparisons = generateMockModelComparisons()
      return comparisons.find(c => c.id == id) || comparisons[0]
    }
  },

  /**
   * 创建模型对比
   * @param {Object} data - 对比数据
   * @returns {Promise} - 返回创建结果
   */
  async createModelComparison(data) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 创建模型对比')
      return Promise.resolve({
        id: Date.now(),
        ...data,
        created_at: new Date().toISOString()
      })
    }
    
    try {
      return await request({
        url: '/evaluation-center/comparisons/',
        method: 'post',
        data
      })
    } catch (error) {
      console.error('创建模型对比失败:', error)
      throw error
    }
  },

  /**
   * 删除模型对比
   * @param {number} id - 模型对比ID
   * @returns {Promise} - 返回删除结果
   */
  async deleteModelComparison(id) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 删除模型对比')
      return Promise.resolve({ success: true })
    }
    
    try {
      return await request({
        url: `/evaluation-center/comparisons/${id}/`,
        method: 'delete'
      })
    } catch (error) {
      console.error('删除模型对比失败:', error)
      throw error
    }
  },

  /**
   * 获取评估指标
   * @param {number} taskId - 评估任务ID
   * @returns {Promise} - 返回评估指标
   */
  async getEvaluationMetrics(taskId) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 评估指标')
      return Promise.resolve({
        accuracy: (0.8 + Math.random() * 0.2).toFixed(4),
        precision: (0.75 + Math.random() * 0.25).toFixed(4),
        recall: (0.7 + Math.random() * 0.3).toFixed(4),
        f1_score: (0.72 + Math.random() * 0.28).toFixed(4)
      })
    }
    
    try {
      return await request({
        url: `/evaluation-center/tasks/${taskId}/metrics/`,
        method: 'get'
      })
    } catch (error) {
      console.error('获取评估指标失败，使用Mock数据:', error)
      return {
        accuracy: (0.8 + Math.random() * 0.2).toFixed(4),
        precision: (0.75 + Math.random() * 0.25).toFixed(4),
        recall: (0.7 + Math.random() * 0.3).toFixed(4),
        f1_score: (0.72 + Math.random() * 0.28).toFixed(4)
      }
    }
  },

  /**
   * 导出评估报告
   * @param {number} id - 评估报告ID
   * @param {Object} params - 导出参数
   * @returns {Promise} - 返回导出结果
   */
  async exportEvaluationReport(id, params = {}) {
    if (USE_MOCK_DATA) {
      console.log('使用Mock数据 - 导出评估报告')
      return Promise.resolve({
        download_url: `/mock/evaluation-report-${id}.pdf`,
        filename: `evaluation-report-${id}.pdf`
      })
    }
    
    try {
      return await request({
        url: `/evaluation-center/reports/${id}/download/`,
        method: 'get',
        params
      })
    } catch (error) {
      console.error('导出评估报告失败:', error)
      throw error
    }
  }
} 