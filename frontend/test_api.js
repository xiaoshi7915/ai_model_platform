// 测试API调用脚本
const axios = require('axios')

// 配置基础URL
const baseURL = 'http://localhost:5688/api/v1'

async function testAPIs() {
  console.log('=== 测试API调用 ===\n')

  const apis = [
    {
      name: '数据集列表',
      url: `${baseURL}/data-center/datasets/`
    },
    {
      name: '知识库列表',
      url: `${baseURL}/data-center/knowledge-bases/`
    },
    {
      name: '模型列表',
      url: `${baseURL}/training-center/models/`
    },
    {
      name: '训练任务列表',
      url: `${baseURL}/training-center/training-jobs/`
    },
    {
      name: 'Docker镜像列表',
      url: `${baseURL}/training-center/docker-images/`
    },
    {
      name: '应用列表',
      url: `${baseURL}/app-center/applications/`
    },
    {
      name: '插件列表',
      url: `${baseURL}/app-center/plugins/`
    },
    {
      name: '评测任务列表',
      url: `${baseURL}/evaluation-center/tasks/`
    },
    {
      name: '评测报告列表',
      url: `${baseURL}/evaluation-center/reports/`
    },
    {
      name: '模型比较列表',
      url: `${baseURL}/evaluation-center/comparisons/`
    }
  ]

  for (const api of apis) {
    try {
      console.log(`测试 ${api.name}...`)
      const response = await axios.get(api.url, {
        timeout: 5000,
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      console.log(`✅ ${api.name}: 状态码 ${response.status}`)
      console.log(`   数据类型: ${Array.isArray(response.data) ? 'Array' : typeof response.data}`)
      
      if (Array.isArray(response.data)) {
        console.log(`   数据量: ${response.data.length}`)
        if (response.data.length > 0) {
          console.log(`   示例: ${JSON.stringify(response.data[0], null, 2).substring(0, 100)}...`)
        }
      } else if (response.data && typeof response.data === 'object') {
        console.log(`   字段: ${Object.keys(response.data).join(', ')}`)
        if (response.data.results) {
          console.log(`   结果数量: ${response.data.results.length}`)
        }
      }
      
    } catch (error) {
      console.log(`❌ ${api.name}: ${error.message}`)
      if (error.response) {
        console.log(`   状态码: ${error.response.status}`)
        console.log(`   错误信息: ${error.response.data}`)
      }
    }
    console.log('')
  }
}

// 运行测试
testAPIs().catch(console.error) 