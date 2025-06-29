/**
 * 模拟数据工具函数
 * 用于前端开发阶段模拟API响应数据
 */

// 生成模拟应用数据
export const generateMockApplications = (count = 5) => {
  const statuses = ['running', 'stopped', 'deploying', 'error'];
  const modelNames = ['GPT-3.5', 'BERT', 'LLaMA', 'Gemini', 'Claude', 'Stable Diffusion'];
  const usernames = ['admin', 'user1', 'user2', 'developer'];
  const descriptions = [
    '用于问答的AI应用',
    '文本分类服务',
    '图像生成应用',
    '自然语言处理服务',
    '智能助手应用'
  ];

  return Array.from({ length: count }).map((_, index) => ({
    id: index + 1,
    name: `示例应用${index + 1}`,
    status: statuses[Math.floor(Math.random() * statuses.length)],
    model_name: modelNames[Math.floor(Math.random() * modelNames.length)],
    endpoint: `http://localhost:8000/api/predict/${index + 1}`,
    created_at: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
    created_by_username: usernames[Math.floor(Math.random() * usernames.length)],
    description: descriptions[Math.floor(Math.random() * descriptions.length)],
    config: {
      max_concurrency: 10,
      timeout: 30,
      log_level: 'info',
      cache_size: 100,
      batch_size: 16,
      use_quantization: Math.random() > 0.5
    }
  }));
};

// 生成模拟插件数据
export const generateMockPlugins = (count = 3) => {
  const versions = ['1.0.0', '1.2.0', '2.0.0', '0.9.5', '3.1.0'];
  const descriptions = [
    '日志分析插件，提供高级日志分析功能',
    '性能监控插件，实时监控应用性能',
    '数据预处理插件，优化输入数据格式',
    '安全检测插件，检测敏感信息泄露',
    '多语言支持插件，增加多语言翻译能力'
  ];

  return Array.from({ length: count }).map((_, index) => ({
    id: index + 1,
    name: `示例插件${index + 1}`,
    version: versions[Math.floor(Math.random() * versions.length)],
    description: descriptions[Math.floor(Math.random() * descriptions.length)],
    compatibility: { 
      'GPT-3.5': '兼容', 
      'BERT': Math.random() > 0.5 ? '兼容' : '部分兼容',
      'LLaMA': Math.random() > 0.7 ? '不兼容' : '兼容'
    },
    created_at: new Date(Date.now() - Math.random() * 60 * 24 * 60 * 60 * 1000).toISOString(),
    created_by_username: 'admin'
  }));
};

// 生成模拟监控数据
export const generateMockMonitoring = () => {
  return {
    cpu_usage: Math.random() * 100,
    memory_usage: Math.random() * 100,
    memory_used: Math.random() * 8 * 1024 * 1024 * 1024,
    memory_total: 8 * 1024 * 1024 * 1024,
    total_requests: Math.floor(Math.random() * 10000),
    avg_response_time: Math.random() * 500,
    error_rate: Math.random() * 5
  };
};

// 生成模拟日志数据
export const generateMockLogs = (count = 50) => {
  const logLevels = ['info', 'warning', 'error', 'debug'];
  const logMessages = [
    '应用启动成功',
    '接收到请求: /api/v1/predict',
    '模型加载完成',
    '处理请求耗时: 245ms',
    '内存使用率超过80%',
    '请求处理失败: 超时',
    '批处理队列已满',
    '缓存已清理'
  ];
  
  return Array.from({ length: count }).map(() => ({
    timestamp: new Date(Date.now() - Math.random() * 86400000),
    level: logLevels[Math.floor(Math.random() * logLevels.length)],
    message: logMessages[Math.floor(Math.random() * logMessages.length)]
  })).sort((a, b) => b.timestamp - a.timestamp);
};

// 生成模拟数据集数据
export const generateMockDatasets = (count = 8) => {
  const types = ['text', 'image', 'tabular', 'audio'];
  const statuses = ['ready', 'processing', 'error'];
  const sizes = ['1.2 MB', '58.6 MB', '512 KB', '2.3 GB', '16.5 MB'];
  const descriptions = [
    '用于文本分类的文本数据集',
    '高清图像识别数据集',
    '客户行为分析表格数据',
    '多语言文本翻译数据集',
    '语音识别训练数据'
  ];
  const formats = ['CSV', 'JSON', 'txt', 'png', 'mp3', 'wav'];

  return Array.from({ length: count }).map((_, index) => ({
    id: index + 1,
    name: `示例数据集${index + 1}`,
    type: types[Math.floor(Math.random() * types.length)],
    status: statuses[Math.floor(Math.random() * statuses.length)],
    size: sizes[Math.floor(Math.random() * sizes.length)],
    format: formats[Math.floor(Math.random() * formats.length)],
    created_at: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
    description: descriptions[Math.floor(Math.random() * descriptions.length)],
    sample_count: Math.floor(Math.random() * 10000) + 1000,
    created_by: 'admin'
  }));
};

// 生成模拟知识库数据
export const generateMockKnowledgeBases = (count = 5) => {
  const types = ['document', 'qa_pairs', 'structured'];
  const statuses = ['active', 'updating', 'archived'];
  const sources = ['manual', 'imported', 'crawled'];
  const descriptions = [
    '产品文档知识库',
    '常见问题解答库',
    '技术支持知识库',
    '客户服务指南',
    '内部培训资料库'
  ];

  return Array.from({ length: count }).map((_, index) => ({
    id: index + 1,
    name: `示例知识库${index + 1}`,
    type: types[Math.floor(Math.random() * types.length)],
    status: statuses[Math.floor(Math.random() * statuses.length)],
    source: sources[Math.floor(Math.random() * sources.length)],
    document_count: Math.floor(Math.random() * 100) + 10,
    created_at: new Date(Date.now() - Math.random() * 60 * 24 * 60 * 60 * 1000).toISOString(),
    description: descriptions[Math.floor(Math.random() * descriptions.length)],
    last_updated: new Date(Date.now() - Math.random() * 10 * 24 * 60 * 60 * 1000).toISOString(),
    created_by: 'admin'
  }));
};

// 生成模拟数据中心统计数据
export const generateMockDataCenterStats = () => {
  return {
    total_datasets: Math.floor(Math.random() * 50) + 20,
    total_knowledge_bases: Math.floor(Math.random() * 30) + 10,
    datasets_by_type: {
      text: Math.floor(Math.random() * 20) + 5,
      image: Math.floor(Math.random() * 15) + 3,
      tabular: Math.floor(Math.random() * 10) + 2,
      audio: Math.floor(Math.random() * 5) + 1
    },
    knowledge_bases_by_type: {
      document: Math.floor(Math.random() * 15) + 5,
      qa_pairs: Math.floor(Math.random() * 10) + 3,
      structured: Math.floor(Math.random() * 5) + 2
    },
    recent_activity: {
      datasets_created: Math.floor(Math.random() * 10) + 1,
      datasets_updated: Math.floor(Math.random() * 5) + 1,
      knowledge_bases_created: Math.floor(Math.random() * 5) + 1,
      knowledge_bases_updated: Math.floor(Math.random() * 8) + 1
    }
  };
};

// 提供默认的模拟数据，用于在API请求失败时显示

// 模拟模型数据
export const mockModels = [
  {
    id: 'model-1',
    name: 'GPT-3.5',
    version: '1.0',
    description: '通用语言模型，参数量约175B',
    parameter_count: 175,
    status: 'active',
    created_at: '2023-01-15T10:00:00Z',
    created_by: 'admin'
  },
  {
    id: 'model-2',
    name: 'LLaMA-7B',
    version: '2.0',
    description: '开源语言模型，参数量7B',
    parameter_count: 7,
    status: 'active',
    created_at: '2023-03-20T14:30:00Z',
    created_by: 'admin'
  },
  {
    id: 'model-3',
    name: 'Stable Diffusion',
    version: '2.1',
    description: '图像生成模型',
    parameter_count: 1.5,
    status: 'active',
    created_at: '2023-02-10T09:15:00Z',
    created_by: 'admin'
  }
]

// 模拟插件数据
export const mockPlugins = [
  {
    id: 'plugin-1',
    name: '内容过滤',
    version: '1.0',
    description: '过滤不适当内容的插件',
    status: 'active',
    created_at: '2023-01-20T11:30:00Z'
  },
  {
    id: 'plugin-2',
    name: '翻译助手',
    version: '1.2',
    description: '提供多语言翻译功能',
    status: 'active',
    created_at: '2023-02-15T13:45:00Z'
  },
  {
    id: 'plugin-3',
    name: '图像增强',
    version: '0.9',
    description: '增强生成图像质量',
    status: 'active',
    created_at: '2023-03-05T10:20:00Z'
  },
  {
    id: 'plugin-4',
    name: '代码生成',
    version: '1.1',
    description: '根据自然语言描述生成代码',
    status: 'active',
    created_at: '2023-03-10T16:00:00Z'
  }
]

// 模拟应用数据
export const mockApplications = [
  {
    id: 'app-1',
    name: '智能客服',
    description: '基于大模型的智能客服系统',
    model_id: 'model-1',
    model_name: 'GPT-3.5',
    status: 'running',
    api_endpoint: 'http://localhost:8000/api/predict/1',
    config: {
      max_concurrency: 5,
      timeout: 60,
      log_level: 'INFO',
      cache_size: 1000,
      batch_size: 4
    },
    plugins: [
      { id: 'plugin-1', name: '内容过滤', version: '1.0' }
    ],
    created_at: '2023-04-10T09:00:00Z',
    created_by: 'admin',
    created_by_username: 'admin'
  },
  {
    id: 'app-2',
    name: '图像生成器',
    description: '生成各种风格的图像',
    model_id: 'model-3',
    model_name: 'Stable Diffusion',
    status: 'stopped',
    api_endpoint: 'http://localhost:8000/api/predict/2',
    config: {
      max_concurrency: 2,
      timeout: 120,
      log_level: 'INFO',
      cache_size: 2000,
      batch_size: 1
    },
    plugins: [
      { id: 'plugin-3', name: '图像增强', version: '0.9' }
    ],
    created_at: '2023-04-15T14:30:00Z',
    created_by: 'admin',
    created_by_username: 'admin'
  }
]

// 模拟监控数据
export const mockMetrics = {
  cpu_usage: 25.4,
  memory_usage: 2048,
  total_requests: 1250,
  avg_response_time: 0.85,
  error_rate: 0.02
}

// 模拟日志数据
export const mockLogs = {
  count: 100,
  results: [
    {
      id: 'log-1',
      timestamp: '2023-05-01T10:30:45Z',
      level: 'INFO',
      message: '应用启动成功'
    },
    {
      id: 'log-2',
      timestamp: '2023-05-01T10:35:12Z',
      level: 'INFO',
      message: '收到用户请求: /api/predict'
    },
    {
      id: 'log-3',
      timestamp: '2023-05-01T10:35:14Z',
      level: 'INFO',
      message: '请求处理完成，耗时: 1.25s'
    },
    {
      id: 'log-4',
      timestamp: '2023-05-01T10:40:22Z',
      level: 'WARNING',
      message: '响应时间超过阈值: 2.5s'
    },
    {
      id: 'log-5',
      timestamp: '2023-05-01T11:15:30Z',
      level: 'ERROR',
      message: '模型预测失败: 内存不足'
    }
  ]
}

export default {
  generateMockApplications,
  generateMockPlugins,
  generateMockMonitoring,
  generateMockLogs,
  generateMockDatasets,
  generateMockKnowledgeBases,
  generateMockDataCenterStats
}; 