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
    
    <!-- 快速操作 -->
    <el-card class="dashboard-card">
      <div slot="header" class="card-header">
        <span>快速操作</span>
      </div>
      <el-row :gutter="20" class="quick-actions">
        <el-col :span="6">
          <router-link to="/data-center/datasets" class="quick-action-item">
            <i class="el-icon-upload2"></i>
            <span>上传数据集</span>
          </router-link>
        </el-col>
        <el-col :span="6">
          <router-link to="/training-center/models" class="quick-action-item">
            <i class="el-icon-cpu"></i>
            <span>创建模型</span>
          </router-link>
        </el-col>
        <el-col :span="6">
          <router-link to="/app-center/applications" class="quick-action-item">
            <i class="el-icon-s-promotion"></i>
            <span>部署应用</span>
          </router-link>
        </el-col>
        <el-col :span="6">
          <router-link to="/evaluation-center/tasks" class="quick-action-item">
            <i class="el-icon-data-board"></i>
            <span>创建评测</span>
          </router-link>
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
      }
    }
  },
  created() {
    this.fetchDashboardData()
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
      this.loading.trainingJobs = true
      this.loading.evaluationTasks = true
      
      try {
        // 获取真实的统计数据
        try {
          const datasets = await this.$store.dispatch('dataCenter/fetchDatasets');
          this.stats.datasets = datasets?.results?.length || datasets?.length || 0;
        } catch (error) {
          console.error('获取数据集统计失败:', error);
          this.stats.datasets = 0;
        }
        
        try {
          const evaluationTasks = await this.$store.dispatch('evaluationCenter/fetchEvaluationTasks');
          this.stats.evaluationTasks = evaluationTasks?.results?.length || evaluationTasks?.length || 0;
          this.recentEvaluationTasks = (evaluationTasks?.results || evaluationTasks || []).slice(0, 5);
        } catch (error) {
          console.error('获取评测任务统计失败:', error);
          this.stats.evaluationTasks = 0;
          this.recentEvaluationTasks = [];
        }
        
        // 尝试从API获取真实数据
        try {
          // 获取应用数据
          const applications = await this.fetchApplications();
          if (applications && applications.length) {
            this.stats.applications = applications.length;
          }
          
          // 获取插件数据
          await this.fetchPlugins();
        } catch (apiError) {
          console.log('使用模拟数据，API请求失败:', apiError);
        }
      } catch (error) {
        console.error('获取仪表盘数据失败:', error);
        this.$message.error('获取仪表盘数据失败，已显示模拟数据');
      } finally {
        this.loading.stats = false;
        this.loading.trainingJobs = false;
        this.loading.evaluationTasks = false;
      }
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

.quick-actions {
  padding: 10px 0;
}

.quick-action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 120px;
  background-color: #f9f9f9;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  text-decoration: none;
  color: #303133;
  transition: all 0.3s ease;
  cursor: pointer;
}

.quick-action-item i {
  font-size: 36px;
  margin-bottom: 12px;
  color: #409EFF;
  transition: all 0.3s ease;
}

.quick-action-item span {
  font-size: 16px;
}

.quick-action-item:hover {
  background-color: #ecf5ff;
  border-color: #c6e2ff;
  color: #409EFF;
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.quick-action-item:hover i {
  transform: scale(1.2);
}
</style> 