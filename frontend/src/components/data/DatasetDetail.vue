<template>
  <div class="dataset-detail">
    <div class="page-header">
      <el-page-header @back="handleBack" :content="datasetDetail ? datasetDetail.name : '数据集详情'"></el-page-header>
      
      <div class="header-actions" v-if="datasetDetail">
        <el-button type="primary" size="small" @click="handleEdit">编辑</el-button>
        <el-button type="danger" size="small" @click="handleDelete">删除</el-button>
      </div>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!datasetDetail" class="empty-container">
      <el-empty description="未找到数据集详情"></el-empty>
    </div>
    
    <div v-else>
      <!-- 基本信息卡片 -->
      <el-card class="detail-card">
        <div slot="header">
          <span>基本信息</span>
        </div>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="数据集名称">{{ datasetDetail.name }}</el-descriptions-item>
          <el-descriptions-item label="数据集ID">{{ datasetDetail.id }}</el-descriptions-item>
          <el-descriptions-item label="文件格式">{{ fileFormat }}</el-descriptions-item>
          <el-descriptions-item label="文件大小">{{ fileSize }}</el-descriptions-item>
          <el-descriptions-item label="创建者">{{ createdBy }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ createdAt }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ updatedAt }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ datasetDetail.description || '暂无描述' }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
      
      <!-- 数据预览卡片 -->
      <el-card class="detail-card">
        <div slot="header">
          <span>数据预览</span>
          <el-button 
            style="float: right; padding: 3px 0" 
            type="text"
            @click="handleDownload"
          >下载数据集</el-button>
        </div>
        
        <div v-if="previewLoading" class="loading-container">
          <el-skeleton :rows="5" animated />
        </div>
        
        <div v-else-if="!previewData || previewData.length === 0" class="empty-container">
          <el-empty description="暂无预览数据"></el-empty>
        </div>
        
        <div v-else>
          <!-- CSV/表格数据预览 -->
          <el-table
            v-if="isTableData"
            :data="previewData"
            border
            style="width: 100%"
            max-height="400"
          >
            <el-table-column
              v-for="(column, index) in tableColumns"
              :key="index"
              :prop="column"
              :label="column"
              min-width="120"
            ></el-table-column>
          </el-table>
          
          <!-- JSON数据预览 -->
          <pre v-else-if="isJsonData" class="json-preview">{{ formatJson(previewData) }}</pre>
          
          <!-- 文本数据预览 -->
          <pre v-else class="text-preview">{{ previewData }}</pre>
        </div>
      </el-card>
      
      <!-- 使用情况卡片 -->
      <el-card class="detail-card">
        <div slot="header">
          <span>使用情况</span>
        </div>
        
        <div v-if="usageLoading" class="loading-container">
          <el-skeleton :rows="3" animated />
        </div>
        
        <div v-else-if="!usageData || usageData.length === 0" class="empty-container">
          <el-empty description="暂无使用记录"></el-empty>
        </div>
        
        <div v-else>
          <el-table
            :data="usageData"
            border
            style="width: 100%"
          >
            <el-table-column prop="type" label="使用类型" width="120"></el-table-column>
            <el-table-column prop="name" label="名称" min-width="150"></el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180">
              <template slot-scope="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template slot-scope="scope">
                <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="text"
                  @click="handleViewUsage(scope.row)"
                >查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import { mapState } from 'vuex'

export default {
  name: 'DatasetDetail',
  props: {
    datasetId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      previewLoading: true,
      usageLoading: true,
      previewData: null,
      usageData: [],
      isTableData: false,
      isJsonData: false,
      tableColumns: []
    }
  },
  computed: {
    ...mapState('dataCenter', {
      dataset: state => state.currentDataset,
      isLoading: state => state.loading
    }),
    loading: {
      get() {
        return this.isLoading
      },
      set(value) {
        this.$store.commit('dataCenter/SET_LOADING', value)
      }
    },
    datasetDetail() {
      return this.dataset
    },
    fileFormat() {
      return this.dataset?.file_format || '未知'
    },
    fileSize() {
      if (!this.dataset?.file_size) return '0 B'
      return this.formatFileSize(this.dataset.file_size)
    },
    createdAt() {
      return this.dataset ? moment(this.dataset.created_at).format('YYYY-MM-DD HH:mm:ss') : '-'
    },
    updatedAt() {
      return this.dataset ? moment(this.dataset.updated_at).format('YYYY-MM-DD HH:mm:ss') : '-'
    },
    createdBy() {
      return this.dataset?.created_by_username || '-'
    }
  },
  methods: {
    async fetchDataset() {
      if (!this.datasetId) return
      
      try {
        const response = await this.$store.dispatch('dataCenter/fetchDatasetDetail', this.datasetId)
        if (response && response.data) {
          this.fetchDataPreview()
          this.fetchUsageData()
        }
      } catch (error) {
        console.error('获取数据集详情失败:', error)
        this.$message.error('获取数据集详情失败')
      }
    },
    // 获取数据预览
    async fetchDataPreview() {
      if (!this.dataset) return
      
      this.previewLoading = true
      try {
        const response = await this.$store.dispatch('dataCenter/fetchDatasetPreview', this.datasetId)
        if (response && response.data) {
          const format = this.dataset.file_format.toLowerCase()
          if (format === 'csv') {
            this.isTableData = true
            this.isJsonData = false
            this.handleCsvPreview(response.data)
          } else if (format === 'json') {
            this.isTableData = false
            this.isJsonData = true
            this.previewData = response.data
          } else {
            this.isTableData = false
            this.isJsonData = false
            this.previewData = response.data
          }
        }
      } catch (error) {
        console.error('获取数据预览失败:', error)
        this.$message.warning('获取数据预览失败')
      } finally {
        this.previewLoading = false
      }
    },
    
    // 处理CSV预览数据
    handleCsvPreview(data) {
      if (Array.isArray(data) && data.length > 0) {
        // 获取所有列名
        this.tableColumns = Object.keys(data[0])
        this.previewData = data
      } else {
        this.tableColumns = []
        this.previewData = []
      }
    },
    
    // 获取使用情况数据
    async fetchUsageData() {
      if (!this.dataset) return
      
      this.usageLoading = true
      try {
        const response = await this.$store.dispatch('dataCenter/fetchDatasetUsage', this.datasetId)
        if (response && response.data) {
          this.usageData = response.data
        }
      } catch (error) {
        console.error('获取使用情况失败:', error)
        this.$message.warning('获取使用情况失败')
      } finally {
        this.usageLoading = false
      }
    },
    
    // 处理返回
    handleBack() {
      this.$emit('back')
    },
    
    // 处理编辑
    handleEdit() {
      this.$emit('edit', this.dataset)
    },
    
    // 处理删除
    handleDelete() {
      this.$confirm('此操作将永久删除该数据集, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await this.$store.dispatch('dataCenter/deleteDataset', this.datasetId)
          this.$message.success('删除成功')
          this.$emit('back')
        } catch (error) {
          this.$message.error('删除失败')
        }
      }).catch(() => {})
    },
    
    // 处理下载
    async handleDownload() {
      try {
        await this.$store.dispatch('dataCenter/downloadDataset', this.datasetId)
        this.$message.success('下载成功')
      } catch (error) {
        this.$message.error('下载失败')
      }
    },
    
    // 处理查看使用情况
    handleViewUsage(usage) {
      const { type, id } = usage
      switch (type.toLowerCase()) {
        case '训练':
          this.$router.push(`/training-center/tasks/${id}`)
          break
        case '评测':
          this.$router.push(`/evaluation-center/tasks/${id}`)
          break
        case '应用':
          this.$router.push(`/app-center/applications/${id}`)
          break
        default:
          this.$message.warning('暂不支持查看该类型的使用情况')
      }
    },
    
    // 格式化日期
    formatDate(date) {
      return date ? moment(date).format('YYYY-MM-DD HH:mm:ss') : '未知'
    },
    
    // 格式化文件大小
    formatFileSize(size) {
      if (size === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(size) / Math.log(k))
      return parseFloat((size / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    
    // 格式化JSON
    formatJson(json) {
      return JSON.stringify(json, null, 2)
    },
    
    // 获取状态类型
    getStatusType(status) {
      const types = {
        'completed': 'success',
        'running': 'warning',
        'failed': 'danger',
        'pending': 'info',
        'cancelled': 'info'
      }
      return types[status] || 'info'
    }
  },
  created() {
    this.fetchDataset()
  },
  watch: {
    datasetId: {
      handler(newVal) {
        if (newVal) {
          this.fetchDataset()
        }
      },
      immediate: true
    },
    dataset: {
      handler(newVal) {
        if (newVal) {
          this.fetchDataPreview()
          this.fetchUsageData()
        }
      },
      immediate: true
    }
  }
}
</script>

<style scoped>
.dataset-detail {
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

.json-preview, .text-preview {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  overflow: auto;
  max-height: 400px;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-word;
}
</style> 