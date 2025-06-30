<template>
  <div class="dashboard-container">
    <div class="page-header">
      <h2 class="page-title">仪表盘</h2>
      <p class="page-description">欢迎使用大型模型构建管理平台</p>
    </div>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="dashboard-stats">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stats-card">
          <div class="stats-icon">
            <i class="el-icon-folder"></i>
          </div>
          <div class="stats-info">
            <div class="stats-title">数据集</div>
            <div class="stats-value">{{ stats.datasets }}</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stats-card">
          <div class="stats-icon">
            <i class="el-icon-cpu"></i>
          </div>
          <div class="stats-info">
            <div class="stats-title">模型</div>
            <div class="stats-value">{{ stats.models }}</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stats-card">
          <div class="stats-icon">
            <i class="el-icon-s-platform"></i>
          </div>
          <div class="stats-info">
            <div class="stats-title">应用</div>
            <div class="stats-value">{{ stats.applications }}</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stats-card">
          <div class="stats-icon">
            <i class="el-icon-data-analysis"></i>
          </div>
          <div class="stats-info">
            <div class="stats-title">评测任务</div>
            <div class="stats-value">{{ stats.evaluationTasks }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快速访问 -->
    <el-card class="dashboard-card">
      <div slot="header" class="card-header">
        <span>快速访问</span>
      </div>
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="(item, index) in quickAccess" :key="index">
          <router-link :to="item.path" class="quick-access-item">
            <i :class="item.icon"></i>
            <span>{{ item.title }}</span>
          </router-link>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 系统概览 -->
    <el-card class="dashboard-card">
      <div slot="header" class="card-header">
        <span>系统概览</span>
      </div>
      <el-row :gutter="20" class="overview-metrics">
        <el-col :xs="24" :sm="12" :md="6">
          <div class="metric-item">
            <div class="metric-icon">
              <i class="el-icon-check"></i>
            </div>
            <div class="metric-content">
              <div class="metric-value">{{ systemMetrics.completedModels }}</div>
              <div class="metric-label">已完成模型</div>
            </div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <div class="metric-item">
            <div class="metric-icon running">
              <i class="el-icon-loading"></i>
            </div>
            <div class="metric-content">
              <div class="metric-value">{{ systemMetrics.runningApps }}</div>
              <div class="metric-label">运行中应用</div>
            </div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <div class="metric-item">
            <div class="metric-icon success">
              <i class="el-icon-success"></i>
            </div>
            <div class="metric-content">
              <div class="metric-value">{{ systemMetrics.completedTasks }}</div>
              <div class="metric-label">完成评测</div>
            </div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <div class="metric-item">
            <div class="metric-icon storage">
              <i class="el-icon-folder"></i>
            </div>
            <div class="metric-content">
              <div class="metric-value">{{ systemMetrics.totalDataSize }}</div>
              <div class="metric-label">数据总量</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 最近活动 -->
    <el-row :gutter="20" class="dashboard-activities">
      <el-col :xs="24" :md="12">
        <el-card class="dashboard-card">
          <div slot="header" class="card-header">
            <span>最近训练任务</span>
            <router-link to="/training-center/jobs" class="card-more">查看更多</router-link>
          </div>
          <el-table :data="recentTrainingJobs" style="width: 100%" v-loading="loading.trainingJobs">
            <el-table-column prop="model_name" label="模型名称" width="180"></el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template slot-scope="scope">
                <el-tag :type="getStatusType(scope.row.status)" size="small">{{ getStatusText(scope.row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间">
              <template slot-scope="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :md="12">
        <el-card class="dashboard-card">
          <div slot="header" class="card-header">
            <span>最近评测任务</span>
            <router-link to="/evaluation-center/tasks" class="card-more">查看更多</router-link>
          </div>
          <el-table :data="recentEvaluationTasks" style="width: 100%" v-loading="loading.evaluationTasks">
            <el-table-column prop="name" label="任务名称" width="180"></el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template slot-scope="scope">
                <el-tag :type="getStatusType(scope.row.status)" size="small">{{ getStatusText(scope.row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间">
              <template slot-scope="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {
        datasets: 0,
        models: 0,
        applications: 0,
        evaluationTasks: 0
      },
      quickAccess: [
        { title: '上传数据集', path: '/data-center/datasets', icon: 'el-icon-upload' },
        { title: '创建模型', path: '/training-center/models', icon: 'el-icon-plus' },
        { title: '部署应用', path: '/app-center/applications', icon: 'el-icon-s-promotion' },
        { title: '创建评测', path: '/evaluation-center/tasks', icon: 'el-icon-s-claim' }
      ],
      recentTrainingJobs: [],
      recentEvaluationTasks: [],
      loading: {
        stats: false,
        trainingJobs: false,
        evaluationTasks: false
      },
      systemMetrics: {
        completedModels: 0,
        runningApps: 0,
        completedTasks: 0,
        totalDataSize: '0 GB'
      },
      retryCount: 0
    }
  },
  async mounted() {
    // 清除旧的认证信息，确保重新登录
    console.log('Dashboard mounted - 清除旧的认证信息')
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('userInfo')
    
    // 重置store中的用户状态
    this.$store.commit('user/CLEAR_USER')
    
    console.log('开始获取仪表盘数据')
    await this.fetchDashboardData()
  },
  methods: {
    ...mapActions([
      'fetchDatasets',
      'fetchModels',
      'fetchEvaluationTasks',
      'fetchTrainingJobs'
    ]),
    ...mapActions('appCenter', [
      'fetchApplications',
      'fetchPlugins'
    ]),
    async fetchDashboardData() {
      this.loading.stats = true
      
      try {
        console.log('=== 开始Dashboard数据获取流程 ===')
        
        // 检查token是否存在
        const token = this.$store.getters.token
        console.log('当前token状态:', token ? '存在' : '不存在')
        
        if (!token) {
          console.log('没有token，开始自动登录流程...')
          
          // 清除旧的token和用户信息
          await this.$store.dispatch('user/resetToken')
          
          // 尝试自动登录
          const loginResult = await this.$store.dispatch('user/login', { 
            username: 'admin', 
            password: 'admin123456@' 
          })
          console.log('自动登录结果:', loginResult)
          
          // 检查登录后的token
          const newToken = this.$store.getters.token
          console.log('登录后token状态:', newToken ? '已获取' : '未获取')
        }

        console.log('开始获取仪表盘数据...')
        
        // 先只测试一个API调用
        try {
          const datasets = await this.$store.dispatch('dataCenter/fetchDatasets')
          console.log('数据集API调用成功:', datasets)
          this.stats.datasets = datasets?.count || datasets?.results?.length || 0
        } catch (apiError) {
          console.error('数据集API调用失败:', apiError)
          throw apiError
        }
        
        // 暂时使用模拟数据
        this.stats.models = 14
        this.stats.applications = 12
        this.stats.evaluationTasks = 17
        
        // 计算系统概览指标
        this.calculateSystemMetrics()
        
        console.log('最终统计数据:', this.stats)
        console.log('=== Dashboard数据获取完成 ===')
        
      } catch (error) {
        console.error('=== Dashboard数据获取失败 ===')
        console.error('错误详情:', error)
        
        // 如果是401错误，尝试重新登录
        if (error.response && error.response.status === 401) {
          try {
            console.log('检测到401错误，清除token并重新登录...')
            await this.$store.dispatch('user/resetToken')
            
            const retryLoginResult = await this.$store.dispatch('user/login', { 
              username: 'admin', 
              password: 'admin123456@' 
            })
            console.log('重新登录结果:', retryLoginResult)
            
            // 递归调用，但加个标记避免无限循环
            if (!this.retryCount) {
              this.retryCount = 1
              await this.fetchDashboardData()
            }
            return
          } catch (loginError) {
            console.error('重新登录失败:', loginError)
            this.$message.error('身份验证失败，请刷新页面重试')
          }
        } else {
          this.$message.error('获取仪表盘数据失败: ' + (error.message || '未知错误'))
        }
      } finally {
        this.loading.stats = false
        this.loading.trainingJobs = false
        this.loading.evaluationTasks = false
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    getStatusType(status) {
      const statusMap = {
        'pending': 'warning',
        'running': 'primary',
        'completed': 'success',
        'failed': 'danger',
        'cancelled': 'info',
        'stopped': 'info',
        'error': 'danger'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        'pending': '等待中',
        'running': '运行中',
        'completed': '已完成',
        'failed': '失败',
        'cancelled': '已取消',
        'stopped': '已停止',
        'error': '错误'
      }
      return statusMap[status] || status
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
    },
    calculateSystemMetrics() {
      // 实现计算系统概览指标的逻辑
      // 这里使用模拟数据，可以根据实际情况调整
      this.systemMetrics = {
        completedModels: Math.floor(this.stats.models * 0.3), // 假设30%的模型已完成
        runningApps: Math.floor(this.stats.applications * 0.7), // 假设70%的应用正在运行
        completedTasks: Math.floor(this.stats.evaluationTasks * 0.4), // 假设40%的评测任务已完成
        totalDataSize: this.formatFileSize(1024 * 1024 * 1024 * 1.2) // 假设1.2GB的数据
      }
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-stats {
  margin-bottom: 20px;
}

.stats-card {
  display: flex;
  align-items: center;
  padding: 20px;
  margin-bottom: 20px;
  height: 100px;
}

.stats-icon {
  font-size: 48px;
  color: #409EFF;
  margin-right: 20px;
}

.stats-info {
  flex: 1;
}

.stats-title {
  font-size: 16px;
  color: #606266;
  margin-bottom: 5px;
}

.stats-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.dashboard-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-more {
  font-size: 14px;
  color: #409EFF;
  text-decoration: none;
}

.quick-access-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 20px;
  text-decoration: none;
  color: #606266;
  transition: all 0.3s;
}

.quick-access-item i {
  font-size: 32px;
  margin-bottom: 10px;
  color: #409EFF;
}

.quick-access-item:hover {
  background-color: #ecf5ff;
  color: #409EFF;
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.dashboard-activities {
  margin-top: 20px;
}

.overview-metrics {
  padding: 10px 0;
}

.metric-item {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  cursor: default;
}

.metric-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  background-color: #409EFF;
  color: white;
  font-size: 24px;
  transition: all 0.3s ease;
}

.metric-icon.running {
  background-color: #E6A23C;
  animation: pulse 2s infinite;
}

.metric-icon.success {
  background-color: #67C23A;
}

.metric-icon.storage {
  background-color: #909399;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.metric-content {
  flex: 1;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 14px;
  color: #606266;
}

.metric-item:hover {
  background-color: #ecf5ff;
  border-color: #c6e2ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.metric-item:hover .metric-icon {
  transform: scale(1.1);
}
</style> 