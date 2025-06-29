<template>
  <div class="model-detail">
    <div class="page-header">
      <el-page-header @back="handleBack" :content="modelDetail ? modelDetail.name : '模型详情'"></el-page-header>
      
      <div class="header-actions" v-if="modelDetail">
        <el-button 
          type="primary" 
          size="small" 
          @click="handleEdit"
          :disabled="!['draft', 'failed'].includes(modelDetail.status)"
        >编辑</el-button>
        <el-button 
          type="success" 
          size="small" 
          @click="handleTrain"
          :disabled="modelDetail.status === 'training'"
        >训练</el-button>
        <el-button 
          type="danger" 
          size="small" 
          @click="handleDelete"
          :disabled="modelDetail.status === 'training'"
        >删除</el-button>
      </div>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!modelDetail" class="empty-container">
      <el-empty description="未找到模型详情"></el-empty>
    </div>
    
    <div v-else>
      <!-- 基本信息卡片 -->
      <el-card class="detail-card">
        <div slot="header">
          <span>基本信息</span>
        </div>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="模型名称">{{ modelDetail.name }}</el-descriptions-item>
          <el-descriptions-item label="模型ID">{{ modelDetail.id }}</el-descriptions-item>
          <el-descriptions-item label="版本">{{ modelDetail.version }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(modelDetail.status)">{{ getStatusText(modelDetail.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="训练数据集">{{ modelDetail.dataset_name || '未指定' }}</el-descriptions-item>
          <el-descriptions-item label="创建者">{{ modelDetail.created_by_username }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(modelDetail.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ formatDate(modelDetail.updated_at) }}</el-descriptions-item>
          <el-descriptions-item label="训练开始时间">{{ formatDate(modelDetail.training_started_at) || '未开始' }}</el-descriptions-item>
          <el-descriptions-item label="训练完成时间">{{ formatDate(modelDetail.training_completed_at) || '未完成' }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ modelDetail.description || '暂无描述' }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
      
      <!-- 训练参数卡片 -->
      <el-card class="detail-card">
        <div slot="header">
          <span>训练参数</span>
        </div>
        
        <div v-if="!modelDetail.parameters || Object.keys(modelDetail.parameters).length === 0" class="empty-container">
          <el-empty description="暂无训练参数"></el-empty>
        </div>
        
        <div v-else>
          <pre class="json-preview">{{ formatJson(modelDetail.parameters) }}</pre>
        </div>
      </el-card>
      
      <!-- 性能指标卡片 -->
      <el-card class="detail-card">
        <div slot="header">
          <span>性能指标</span>
        </div>
        
        <div v-if="!modelDetail.metrics || Object.keys(modelDetail.metrics).length === 0" class="empty-container">
          <el-empty description="暂无性能指标"></el-empty>
        </div>
        
        <div v-else>
          <el-table :data="metricsData" border style="width: 100%">
            <el-table-column prop="name" label="指标名称" width="180"></el-table-column>
            <el-table-column prop="value" label="指标值"></el-table-column>
          </el-table>
        </div>
      </el-card>
      
      <!-- 训练任务卡片 -->
      <el-card class="detail-card">
        <div slot="header">
          <span>训练任务</span>
        </div>
        
        <div v-if="trainingJobsLoading" class="loading-container">
          <el-skeleton :rows="3" animated />
        </div>
        
        <div v-else-if="!trainingJobs || trainingJobs.length === 0" class="empty-container">
          <el-empty description="暂无训练任务"></el-empty>
        </div>
        
        <div v-else>
          <el-table :data="trainingJobs" border style="width: 100%">
            <el-table-column prop="id" label="任务ID" width="80"></el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template slot-scope="scope">
                <el-tag :type="getJobStatusType(scope.row.status)">{{ getJobStatusText(scope.row.status) }}</el-tag>
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
            <el-table-column label="操作" width="120" fixed="right">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="text"
                  @click="handleViewLog(scope.row)"
                >查看日志</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
    
    <!-- 训练对话框 -->
    <el-dialog
      title="开始训练"
      :visible.sync="trainDialogVisible"
      width="600px"
    >
      <div v-if="modelDetail">
        <p>您确定要开始训练模型 <strong>{{ modelDetail.name }}</strong> (版本: {{ modelDetail.version }}) 吗？</p>
        
        <el-form ref="trainForm" :model="trainForm" label-width="120px">
          <el-form-item label="Docker镜像">
            <el-select v-model="trainForm.docker_image_id" placeholder="请选择Docker镜像" style="width: 100%">
              <el-option
                v-for="image in dockerImages"
                :key="image.id"
                :label="`${image.name}:${image.tag}`"
                :value="image.id"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="训练参数">
            <el-input
              type="textarea"
              :rows="5"
              placeholder="请输入训练参数（JSON格式）"
              v-model="trainForm.parameters"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
      
      <div slot="footer" class="dialog-footer">
        <el-button @click="trainDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmTrain" :loading="trainLoading">确定</el-button>
      </div>
    </el-dialog>
    
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
          <div>状态: <el-tag :type="getJobStatusType(currentJob.status)">{{ getJobStatusText(currentJob.status) }}</el-tag></div>
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
  name: 'ModelDetail',
  components: {
    
  },
  props: {
    modelId: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      loading: false,
      trainingJobsLoading: false,
      trainDialogVisible: false,
      logDialogVisible: false,
      trainForm: {
        docker_image_id: '',
        parameters: '{}'
      },
      trainLoading: false,
      currentJob: null
    }
  },
  computed: {
    ...mapState({
      modelDetail: state => state.trainingCenter.currentModel,
      dockerImages: state => state.dockerImages?.dockerImages || [],
      trainingJobs: state => state.trainingCenter.trainingJobs,
      error: state => state.trainingCenter.error
    }),
    // 处理性能指标数据
    metricsData() {
      if (!this.modelDetail || !this.modelDetail.metrics) return []
      
      return Object.entries(this.modelDetail.metrics).map(([name, value]) => ({
        name,
        value: typeof value === 'object' ? JSON.stringify(value) : value
      }))
    }
  },
  methods: {
    // 获取模型详情
    fetchModelDetail() {
      this.loading = true
      this.$store.dispatch('trainingCenter/fetchModelDetail', this.modelId)
        .then((response) => {
          this.loading = false
          if (response) {
            this.fetchTrainingJobs()
          } else {
            this.$message.error('获取模型详情失败，模型可能不存在')
          }
        })
        .catch(error => {
          console.error('获取模型详情失败:', error)
          this.$message.error(error.message || '获取模型详情失败')
          this.loading = false
        })
    },
    
    // 获取训练任务列表
    fetchTrainingJobs() {
      this.trainingJobsLoading = true
      this.$store.dispatch('trainingCenter/fetchTrainingJobs', { model: this.modelId })
        .then(() => {
          this.trainingJobsLoading = false
        })
        .catch(error => {
          console.error('获取训练任务列表失败:', error)
          this.$message.error(error.message || '获取训练任务列表失败')
          this.trainingJobsLoading = false
        })
    },
    
    // 获取Docker镜像列表
    fetchDockerImages() {
      this.$store.dispatch('dockerImages/fetchDockerImages')
        .catch(error => {
          console.error('获取Docker镜像列表失败:', error)
        })
    },
    
    // 处理返回
    handleBack() {
      this.$emit('back')
    },
    
    // 处理编辑
    handleEdit() {
      if (this.modelDetail) {
        this.$emit('edit', this.modelDetail)
      }
    },
    
    // 处理训练
    handleTrain() {
      if (!this.modelDetail) {
        this.$message.error('模型信息不完整，无法开始训练')
        return
      }
      
      this.trainForm = {
        docker_image_id: '',
        parameters: JSON.stringify(this.modelDetail.parameters || {}, null, 2)
      }
      this.trainDialogVisible = true
    },
    
    // 确认训练
    confirmTrain() {
      if (!this.trainForm.docker_image_id) {
        this.$message.warning('请选择Docker镜像')
        return
      }
      
      try {
        // 验证参数是否为有效的JSON
        const parameters = JSON.parse(this.trainForm.parameters)
        
        this.trainLoading = true
        
        // 调用训练API
        this.$store.dispatch('trainingCenter/trainModel', {
          id: this.modelId,
          data: {
            docker_image_id: this.trainForm.docker_image_id,
            parameters: parameters
          }
        }).then(() => {
          this.$message.success('模型训练任务已提交')
          this.trainDialogVisible = false
          this.fetchModelDetail() // 刷新模型详情
        }).catch(error => {
          console.error('训练模型失败:', error)
          this.$message.error(error.message || '训练模型失败')
        }).finally(() => {
          this.trainLoading = false
        })
      } catch (error) {
        this.$message.error('训练参数格式不正确，请输入有效的JSON格式')
      }
    },
    
    // 处理删除
    handleDelete() {
      if (!this.modelDetail) return;
      
      this.$confirm('此操作将永久删除该模型, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('trainingCenter/deleteModel', this.modelId)
          .then(success => {
            if (success) {
              this.$message.success('删除模型成功')
              this.handleBack()
            } else {
              this.$message.error('删除模型失败')
            }
          })
          .catch(error => {
            console.error('删除模型失败:', error)
            this.$message.error(error.message || '删除模型失败')
          })
      }).catch(() => {})
    },
    
    // 处理查看日志
    handleViewLog(job) {
      if (job) {
        this.currentJob = job
        this.logDialogVisible = true
      }
    },
    
    // 获取状态类型
    getStatusType(status) {
      const types = {
        'draft': 'info',
        'training': 'warning',
        'completed': 'success',
        'failed': 'danger'
      }
      return types[status] || 'info'
    },
    
    // 获取状态文本
    getStatusText(status) {
      const texts = {
        'draft': '草稿',
        'training': '训练中',
        'completed': '已完成',
        'failed': '失败'
      }
      return texts[status] || status
    },
    
    // 获取任务状态类型
    getJobStatusType(status) {
      const types = {
        'pending': 'info',
        'running': 'warning',
        'completed': 'success',
        'failed': 'danger',
        'cancelled': 'info'
      }
      return types[status] || 'info'
    },
    
    // 获取任务状态文本
    getJobStatusText(status) {
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
    },
    
    // 格式化JSON
    formatJson(json) {
      return JSON.stringify(json, null, 2)
    }
  },
  created() {
    this.fetchModelDetail()
    this.fetchDockerImages()
  },
  watch: {
    modelId: {
      handler(newVal) {
        if (newVal) {
          this.fetchModelDetail()
        }
      },
      immediate: true
    }
  }
}
</script>

<style scoped>
.model-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.loading-container, .empty-container {
  min-height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.detail-card {
  margin-bottom: 20px;
}

.json-preview {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  overflow: auto;
  max-height: 400px;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-word;
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