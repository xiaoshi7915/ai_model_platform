<template>
  <div class="evaluation-task-detail">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!taskDetail" class="empty-container">
      <el-empty description="未找到评测任务详情"></el-empty>
    </div>
    
    <div v-else>
      <!-- 任务基本信息卡片 -->
      <el-card class="detail-card">
        <div slot="header" class="card-header">
          <span>基本信息</span>
          <div class="header-actions">
            <el-tag :type="getStatusType(taskDetail.status)">
              {{ getStatusText(taskDetail.status) }}
            </el-tag>
          </div>
        </div>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="任务名称">{{ taskDetail.name }}</el-descriptions-item>
          <el-descriptions-item label="任务ID">{{ taskDetail.id }}</el-descriptions-item>
          <el-descriptions-item label="评测模型">{{ taskDetail.model_name }} ({{ taskDetail.model_version }})</el-descriptions-item>
          <el-descriptions-item label="评测数据集">{{ taskDetail.dataset_name }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(taskDetail.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ formatDate(taskDetail.updated_at) }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ taskDetail.description || '无' }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
      
      <!-- 评测配置卡片 -->
      <el-card class="detail-card">
        <div slot="header" class="card-header">
          <span>评测配置</span>
        </div>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="评测指标">
            <el-tag v-for="metric in taskDetail.metrics" :key="metric" style="margin-right: 5px">
              {{ metric }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="数据集大小">{{ taskDetail.dataset_size || '未知' }}</el-descriptions-item>
          <el-descriptions-item label="评测参数" :span="2">
            <pre v-if="taskDetail.parameters">{{ JSON.stringify(taskDetail.parameters, null, 2) }}</pre>
            <span v-else>无</span>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
      
      <!-- 评测进度卡片 -->
      <el-card class="detail-card" v-if="taskDetail.status === 'running'">
        <div slot="header" class="card-header">
          <span>评测进度</span>
        </div>
        
        <div class="progress-container">
          <el-progress 
            :percentage="taskDetail.progress || 0" 
            :format="percentageFormat"
            :status="taskDetail.progress >= 100 ? 'success' : ''"
          ></el-progress>
          
          <div class="progress-info">
            <span>已完成: {{ taskDetail.completed_samples || 0 }} / {{ taskDetail.total_samples || 0 }}</span>
            <span>预计剩余时间: {{ taskDetail.estimated_time_remaining || '计算中...' }}</span>
          </div>
        </div>
      </el-card>
      
      <!-- 评测结果卡片 -->
      <el-card class="detail-card" v-if="taskDetail.status === 'completed'">
        <div slot="header" class="card-header">
          <span>评测结果摘要</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleViewFullReport">查看完整报告</el-button>
          </div>
        </div>
        
        <div class="result-summary">
          <el-row :gutter="20">
            <el-col :span="8" v-for="(value, key) in taskDetail.result_summary" :key="key">
              <div class="metric-card">
                <div class="metric-name">{{ key }}</div>
                <div class="metric-value">{{ formatMetricValue(value) }}</div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>
      
      <!-- 错误信息卡片 -->
      <el-card class="detail-card error-card" v-if="taskDetail.status === 'failed'">
        <div slot="header" class="card-header">
          <span>错误信息</span>
        </div>
        
        <div class="error-container">
          <pre>{{ taskDetail.error_message || '未知错误' }}</pre>
        </div>
      </el-card>
      
      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button @click="handleBack">返回</el-button>
        
        <el-button 
          type="primary" 
          @click="handleStart" 
          v-if="taskDetail.status === 'pending'"
        >开始评测</el-button>
        
        <el-button 
          type="warning" 
          @click="handleCancel" 
          v-if="taskDetail.status === 'running'"
        >取消评测</el-button>
        
        <el-button 
          type="success" 
          @click="handleViewFullReport" 
          v-if="taskDetail.status === 'completed'"
        >查看完整报告</el-button>
        
        <el-button 
          type="danger" 
          @click="handleDelete" 
          :disabled="taskDetail.status === 'running'"
        >删除任务</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import moment from 'moment'

export default {
  name: 'EvaluationTaskDetail',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  
  data() {
    return {
      loading: false,
      progressTimer: null
    }
  },
  
  computed: {
    ...mapState('evaluationCenter', ['currentTask']),
    
    taskDetail() {
      return this.currentTask
    },
    
    isRunning() {
      return this.taskDetail && this.taskDetail.status === 'running'
    }
  },
  
  created() {
    this.fetchTaskDetail()
    this.startProgressPolling()
  },
  
  beforeDestroy() {
    this.stopProgressPolling()
  },
  
  methods: {
    ...mapActions('evaluationCenter', [
      'fetchEvaluationTaskDetail',
      'startEvaluationTask',
      'cancelEvaluationTask',
      'deleteEvaluationTask',
      'fetchEvaluationTaskProgress'
    ]),
    
    // 获取评测任务详情
    async fetchTaskDetail() {
      this.loading = true
      try {
        await this.fetchEvaluationTaskDetail(this.id)
      } catch (error) {
        this.$message.error('获取评测任务详情失败')
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    
    // 开始进度轮询
    startProgressPolling() {
      if (this.isRunning) {
        this.progressTimer = setInterval(this.fetchProgress, 5000)
      }
    },
    
    // 停止进度轮询
    stopProgressPolling() {
      if (this.progressTimer) {
        clearInterval(this.progressTimer)
        this.progressTimer = null
      }
    },
    
    // 获取任务进度
    async fetchProgress() {
      if (!this.isRunning) {
        this.stopProgressPolling()
        return
      }
      
      try {
        const progress = await this.fetchEvaluationTaskProgress(this.id)
        if (progress.status !== 'running') {
          this.stopProgressPolling()
          this.fetchTaskDetail()
        }
      } catch (error) {
        console.error('获取任务进度失败:', error)
      }
    },
    
    // 处理返回
    handleBack() {
      this.$router.push('/evaluation-center/tasks')
    },
    
    // 处理开始评测
    async handleStart() {
      try {
        await this.startEvaluationTask(this.id)
        this.$message.success('开始评测任务成功')
        await this.fetchTaskDetail()
        this.startProgressPolling()
      } catch (error) {
        this.$message.error('开始评测任务失败')
        console.error(error)
      }
    },
    
    // 处理取消评测
    async handleCancel() {
      try {
        await this.cancelEvaluationTask(this.id)
        this.$message.success('取消评测任务成功')
        await this.fetchTaskDetail()
        this.stopProgressPolling()
      } catch (error) {
        this.$message.error('取消评测任务失败')
        console.error(error)
      }
    },
    
    // 处理删除任务
    async handleDelete() {
      try {
        await this.deleteEvaluationTask(this.id)
        this.$message.success('删除评测任务成功')
        this.$router.push('/evaluation-center/tasks')
      } catch (error) {
        this.$message.error('删除评测任务失败')
        console.error(error)
      }
    },
    
    // 处理查看完整报告
    handleViewFullReport() {
      if (this.taskDetail && this.taskDetail.report_id) {
        this.$router.push(`/evaluation-center/reports/${this.taskDetail.report_id}`)
      }
    },
    
    // 获取状态类型
    getStatusType(status) {
      const types = {
        pending: 'info',
        running: 'warning',
        completed: 'success',
        failed: 'danger',
        cancelled: 'info'
      }
      return types[status] || 'info'
    },
    
    // 获取状态文本
    getStatusText(status) {
      const texts = {
        pending: '等待中',
        running: '运行中',
        completed: '已完成',
        failed: '失败',
        cancelled: '已取消'
      }
      return texts[status] || status
    },
    
    // 格式化日期
    formatDate(date) {
      if (!date) return '-'
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    
    // 格式化进度百分比
    percentageFormat(percentage) {
      return percentage ? `${percentage}%` : '0%'
    },
    
    // 格式化指标值
    formatMetricValue(value) {
      if (typeof value === 'number') {
        return value.toFixed(4)
      }
      return value
    }
  }
}
</script>

<style scoped>
.evaluation-task-detail {
  padding: 20px;
}

.loading-container, .empty-container {
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.detail-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.progress-container {
  padding: 20px 0;
}

.progress-info {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  color: #606266;
}

.result-summary {
  padding: 10px 0;
}

.metric-card {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 15px;
  text-align: center;
}

.metric-name {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.error-card {
  border: 1px solid #f56c6c;
}

.error-container {
  background-color: #fef0f0;
  padding: 15px;
  border-radius: 4px;
  color: #f56c6c;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style> 