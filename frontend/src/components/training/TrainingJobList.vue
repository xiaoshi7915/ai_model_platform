<template>
  <div class="training-job-list">
    <!-- 搜索和过滤区域 -->
    <div class="table-actions">
      <div class="left-actions">
        <el-select 
          v-model="statusFilter" 
          placeholder="状态过滤" 
          clearable 
          @change="handleStatusChange"
          class="status-filter"
        >
          <el-option
            v-for="item in statusOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
        
        <el-select 
          v-model="modelFilter" 
          placeholder="模型过滤" 
          clearable 
          @change="handleModelChange"
          class="model-filter"
        >
          <el-option
            v-for="model in models"
            :key="model.id"
            :label="`${model.name} (${model.version})`"
            :value="model.id"
          ></el-option>
        </el-select>
      </div>
      
      <div class="right-actions">
        <el-button type="primary" @click="handleRefresh">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
      </div>
    </div>
    
    <!-- 训练任务列表表格 -->
    <el-table
      v-loading="loading"
      :data="filteredJobs"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="任务ID" width="80"></el-table-column>
      
      <el-table-column prop="model_name" label="模型名称" min-width="150">
        <template slot-scope="scope">
          <el-link type="primary" @click="handleViewModel(scope.row)">
            {{ scope.row.model_name }} ({{ scope.row.model_version }})
          </el-link>
        </template>
      </el-table-column>
      
      <el-table-column prop="status" label="状态" width="100">
        <template slot-scope="scope">
          <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="docker_image_name" label="Docker镜像" width="180">
        <template slot-scope="scope">
          {{ scope.row.docker_image_name }}:{{ scope.row.docker_image_tag }}
        </template>
      </el-table-column>
      
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="started_at" label="开始时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.started_at) || '未开始' }}
        </template>
      </el-table-column>
      
      <el-table-column prop="completed_at" label="完成时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.completed_at) || '未完成' }}
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="150" fixed="right">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            @click="handleViewLog(scope.row)"
          >查看日志</el-button>
          
          <el-button
            size="mini"
            type="text"
            class="danger-text"
            @click="handleCancel(scope.row)"
            v-if="scope.row.status === 'pending' || scope.row.status === 'running'"
          >取消</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalJobs"
      ></el-pagination>
    </div>
    
    <!-- 日志对话框 -->
    <el-dialog
      title="训练日志"
      :visible.sync="logDialogVisible"
      width="80%"
      class="log-dialog"
    >
      <div v-if="currentJob">
        <div class="log-header">
          <div>任务ID: {{ currentJob.id }}</div>
          <div>状态: <el-tag :type="getStatusType(currentJob.status)">{{ getStatusText(currentJob.status) }}</el-tag></div>
          <div>模型: {{ currentJob.model_name }} ({{ currentJob.model_version }})</div>
          <div>Docker镜像: {{ currentJob.docker_image_name }}:{{ currentJob.docker_image_tag }}</div>
        </div>
        
        <div class="log-content">
          <pre v-if="currentJob.log">{{ currentJob.log }}</pre>
          <div v-else class="empty-log">暂无日志</div>
        </div>
      </div>
      
      <div slot="footer" class="dialog-footer">
        <el-button @click="logDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'

export default {
  name: 'TrainingJobList',
  data() {
    return {
      statusFilter: '',
      modelFilter: '',
      currentPage: 1,
      pageSize: 10,
      logDialogVisible: false,
      currentJob: null,
      statusOptions: [
        { value: 'pending', label: '等待中' },
        { value: 'running', label: '运行中' },
        { value: 'completed', label: '已完成' },
        { value: 'failed', label: '失败' },
        { value: 'cancelled', label: '已取消' }
      ]
    }
  },
  computed: {
    ...mapState({
      trainingJobs: state => state.trainingCenter.trainingJobs,
      models: state => state.trainingCenter.models,
      loading: state => state.trainingCenter.loading
    }),
    // 过滤后的训练任务
    filteredJobs() {
      let result = this.trainingJobs
      
      // 状态过滤
      if (this.statusFilter) {
        result = result.filter(job => job.status === this.statusFilter)
      }
      
      // 模型过滤
      if (this.modelFilter) {
        result = result.filter(job => job.model === this.modelFilter)
      }
      
      // 分页
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      
      return result.slice(start, end)
    },
    // 总训练任务数量
    totalJobs() {
      return this.trainingJobs.length
    }
  },
  methods: {
    // 获取训练任务列表
    fetchTrainingJobs() {
      this.$store.dispatch('trainingCenter/fetchTrainingJobs')
    },
    
    // 获取模型列表
    fetchModels() {
      if (this.models.length === 0) {
        this.$store.dispatch('trainingCenter/fetchModels')
      }
    },
    
    // 处理状态过滤变化
    handleStatusChange() {
      this.currentPage = 1
    },
    
    // 处理模型过滤变化
    handleModelChange() {
      this.currentPage = 1
    },
    
    // 处理页面大小变化
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
    },
    
    // 处理当前页变化
    handleCurrentChange(page) {
      this.currentPage = page
    },
    
    // 处理刷新
    handleRefresh() {
      this.fetchTrainingJobs()
    },
    
    // 处理查看模型
    handleViewModel(job) {
      this.$emit('view-model', job.model)
    },
    
    // 处理查看日志
    handleViewLog(job) {
      this.currentJob = job
      this.logDialogVisible = true
    },
    
    // 处理取消训练任务
    handleCancel(job) {
      this.$confirm('此操作将取消该训练任务, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('trainingCenter/cancelTrainingJob', job.id)
          .then(() => {
            this.$message.success('取消训练任务成功')
            this.fetchTrainingJobs()
          })
          .catch(error => {
            console.error('取消训练任务失败:', error)
            this.$message.error('取消训练任务失败')
          })
      }).catch(() => {})
    },
    
    // 获取状态类型
    getStatusType(status) {
      const types = {
        'pending': 'info',
        'running': 'warning',
        'completed': 'success',
        'failed': 'danger',
        'cancelled': 'info'
      }
      return types[status] || 'info'
    },
    
    // 获取状态文本
    getStatusText(status) {
      const texts = {
        'pending': '等待中',
        'running': '运行中',
        'completed': '已完成',
        'failed': '失败',
        'cancelled': '已取消'
      }
      return texts[status] || status
    },
    
    // 格式化日期
    formatDate(date) {
      return date ? moment(date).format('YYYY-MM-DD HH:mm:ss') : null
    }
  },
  created() {
    this.fetchTrainingJobs()
    this.fetchModels()
  }
}
</script>

<style scoped>
.training-job-list {
  padding: 20px;
}

.table-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.left-actions {
  display: flex;
  align-items: center;
}

.status-filter, .model-filter {
  width: 180px;
  margin-right: 15px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.danger-text {
  color: #F56C6C;
}

.danger-text:hover {
  color: #f78989;
}

.log-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.log-content {
  background-color: #1e1e1e;
  color: #f1f1f1;
  padding: 15px;
  border-radius: 4px;
  overflow: auto;
  max-height: 500px;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-word;
}

.empty-log {
  text-align: center;
  padding: 20px;
  color: #909399;
}

.log-dialog >>> .el-dialog__body {
  padding: 10px 20px;
}
</style> 