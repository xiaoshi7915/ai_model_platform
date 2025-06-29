<template>
  <div class="dataset-management">
    <!-- 数据集列表视图 -->
    <div v-if="currentView === 'list'">
      <dataset-list
        @view="handleViewDataset"
        @create="handleCreateDataset"
        @edit="handleEditDataset"
        @delete="handleDeleteDataset"
      />
    </div>
    
    <!-- 数据集详情视图 -->
    <div v-else-if="currentView === 'detail'">
      <dataset-detail
        :dataset-id="currentDatasetId"
        @back="handleBackToList"
        @edit="handleEditDataset"
        @delete="handleDeleteAndBackToList"
      />
    </div>
    
    <!-- 数据集表单（创建/编辑） -->
    <el-dialog
      :title="formType === 'create' ? '上传数据集' : '编辑数据集'"
      :visible.sync="formVisible"
      width="70%"
      @closed="resetForm"
    >
      <dataset-form
        ref="datasetForm"
        :dataset="currentDataset"
        :type="formType"
        @submit="handleFormSubmit"
        @cancel="formVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script>
import DatasetList from './DatasetList.vue'
import DatasetDetail from './DatasetDetail.vue'
import DatasetForm from './DatasetForm.vue'

export default {
  name: 'DatasetManagement',
  components: {
    DatasetList,
    DatasetDetail,
    DatasetForm
  },
  data() {
    return {
      currentView: 'list', // 'list' 或 'detail'
      currentDatasetId: null,
      currentDataset: null,
      formVisible: false,
      formType: 'create' // 'create' 或 'edit'
    }
  },
  methods: {
    // 处理查看数据集
    handleViewDataset(dataset) {
      this.currentDatasetId = dataset.id
      this.currentView = 'detail'
    },
    
    // 处理返回列表
    handleBackToList() {
      this.currentView = 'list'
      this.currentDatasetId = null
    },
    
    // 处理创建数据集
    handleCreateDataset() {
      this.formType = 'create'
      this.currentDataset = {
        name: '',
        description: '',
        file: null
      }
      this.formVisible = true
    },
    
    // 处理编辑数据集
    handleEditDataset(dataset) {
      this.formType = 'edit'
      this.currentDataset = JSON.parse(JSON.stringify(dataset))
      this.formVisible = true
    },
    
    // 处理删除数据集
    handleDeleteDataset(dataset) {
      this.$confirm('此操作将永久删除该数据集, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('dataCenter/deleteDataset', dataset.id)
          .then(() => {
            this.$message.success('删除数据集成功')
          })
          .catch(error => {
            console.error('删除数据集失败:', error)
            this.$message.error('删除数据集失败')
          })
      }).catch(() => {})
    },
    
    // 处理删除并返回列表
    handleDeleteAndBackToList(dataset) {
      this.$confirm('此操作将永久删除该数据集, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('dataCenter/deleteDataset', dataset.id)
          .then(() => {
            this.$message.success('删除数据集成功')
            this.handleBackToList()
          })
          .catch(error => {
            console.error('删除数据集失败:', error)
            this.$message.error('删除数据集失败')
          })
      }).catch(() => {})
    },
    
    // 处理表单提交
    handleFormSubmit(formData) {
      if (this.formType === 'create') {
        // 创建数据集
        this.$store.dispatch('dataCenter/createDataset', {
          data: {
            name: formData.name,
            description: formData.description
          },
          file: formData.file,
          onProgress: this.handleUploadProgress
        })
          .then(() => {
            this.$message.success('上传数据集成功')
            this.formVisible = false
          })
          .catch(error => {
            console.error('上传数据集失败:', error)
            this.$message.error('上传数据集失败')
          })
      } else {
        // 更新数据集
        this.$store.dispatch('dataCenter/updateDataset', {
          id: formData.id,
          data: {
            name: formData.name,
            description: formData.description
          }
        })
          .then(() => {
            this.$message.success('更新数据集成功')
            this.formVisible = false
            
            // 如果当前在详情页，刷新详情
            if (this.currentView === 'detail' && this.currentDatasetId === formData.id) {
              this.$store.dispatch('dataCenter/fetchDatasetDetail', formData.id)
            }
          })
          .catch(error => {
            console.error('更新数据集失败:', error)
            this.$message.error('更新数据集失败')
          })
      }
    },
    
    // 处理上传进度
    handleUploadProgress(event) {
      console.log('上传进度:', event.percent)
    },
    
    // 重置表单
    resetForm() {
      if (this.$refs.datasetForm) {
        this.$refs.datasetForm.resetForm()
      }
    },
    
    // 手动刷新数据
    refreshDatasets() {
      this.$store.dispatch('dataCenter/fetchDatasets').then(() => {
        // 刷新数据成功，不显示调试信息
      }).catch(error => {
        console.error('刷新数据失败:', error);
      });
    }
  },
  created() {
    // 从路由参数中获取视图和数据集ID
    const { view, datasetId } = this.$route.query
    
    if (view) {
      this.currentView = view
    }
    
    if (datasetId) {
      this.currentDatasetId = datasetId
    }
  },
  watch: {
    // 监听视图和数据集ID变化，更新路由
    currentView(newVal) {
      const query = { ...this.$route.query, view: newVal }
      if (newVal !== 'detail') {
        delete query.datasetId
      }
      this.$router.replace({ query })
    },
    currentDatasetId(newVal) {
      if (newVal && this.currentView === 'detail') {
        this.$router.replace({ query: { ...this.$route.query, datasetId: newVal } })
      }
    }
  }
}
</script>

<style scoped>
.dataset-management {
  min-height: 500px;
}

.debug-info-card {
  margin: 10px 0;
  padding: 10px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.error-info {
  background-color: #fff0f0;
  padding: 10px;
  border-left: 3px solid red;
  margin-bottom: 10px;
}

.data-info {
  font-size: 14px;
}

.refresh-btn {
  background-color: #409EFF;
  color: white;
  border: none;
  padding: 5px 10px;
  margin-right: 10px;
  cursor: pointer;
  border-radius: 3px;
}

.toggle-btn {
  background-color: #67C23A;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 3px;
}

pre {
  background-color: #f5f5f5;
  padding: 10px;
  max-height: 200px;
  overflow: auto;
  border-radius: 3px;
}
</style> 