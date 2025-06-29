<template>
  <div class="knowledge-base-management">
    <!-- 知识库列表视图 -->
    <div v-if="currentView === 'list'">
      <knowledge-base-list
        @view="handleViewKnowledgeBase"
        @create="handleCreateKnowledgeBase"
        @edit="handleEditKnowledgeBase"
        @delete="handleDeleteKnowledgeBase"
      />
    </div>
    
    <!-- 知识库详情视图 -->
    <div v-else-if="currentView === 'detail'">
      <knowledge-base-detail
        :knowledge-base-id="currentKnowledgeBaseId"
        @back="handleBackToList"
        @edit="handleEditKnowledgeBase"
        @delete="handleDeleteAndBackToList"
      />
    </div>
    
    <!-- 知识库表单（创建/编辑） -->
    <el-dialog
      :title="formType === 'create' ? '创建知识库' : '编辑知识库'"
      :visible.sync="formVisible"
      width="70%"
      @closed="resetForm"
    >
      <knowledge-base-form
        ref="knowledgeBaseForm"
        :knowledge-base="currentKnowledgeBase"
        :type="formType"
        @submit="handleFormSubmit"
        @cancel="formVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script>
import KnowledgeBaseList from './KnowledgeBaseList.vue'
import KnowledgeBaseDetail from './KnowledgeBaseDetail.vue'
import KnowledgeBaseForm from './KnowledgeBaseForm.vue'

export default {
  name: 'KnowledgeBaseManagement',
  components: {
    KnowledgeBaseList,
    KnowledgeBaseDetail,
    KnowledgeBaseForm
  },
  data() {
    return {
      currentView: 'list', // 'list' 或 'detail'
      currentKnowledgeBaseId: null,
      currentKnowledgeBase: null,
      formVisible: false,
      formType: 'create' // 'create' 或 'edit'
    }
  },
  methods: {
    // 处理查看知识库
    handleViewKnowledgeBase(knowledgeBase) {
      this.currentKnowledgeBaseId = knowledgeBase.id
      this.currentView = 'detail'
    },
    
    // 处理返回列表
    handleBackToList() {
      this.currentView = 'list'
      this.currentKnowledgeBaseId = null
    },
    
    // 处理创建知识库
    handleCreateKnowledgeBase() {
      this.formType = 'create'
      this.currentKnowledgeBase = {
        name: '',
        description: '',
        content: ''
      }
      this.formVisible = true
    },
    
    // 处理编辑知识库
    handleEditKnowledgeBase(knowledgeBase) {
      this.formType = 'edit'
      this.currentKnowledgeBase = JSON.parse(JSON.stringify(knowledgeBase))
      this.formVisible = true
    },
    
    // 处理删除知识库
    handleDeleteKnowledgeBase(knowledgeBase) {
      this.$confirm('此操作将永久删除该知识库, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('dataCenter/deleteKnowledgeBase', knowledgeBase.id)
          .then(() => {
            this.$message.success('删除知识库成功')
            // 刷新知识库列表
            this.$store.dispatch('dataCenter/fetchKnowledgeBases')
          })
          .catch(error => {
            console.error('删除知识库失败:', error)
            this.$message.error(error.message || '删除知识库失败，请检查您的权限')
          })
      }).catch(() => {
        // 用户取消删除操作
      })
    },
    
    // 处理删除并返回列表
    handleDeleteAndBackToList(knowledgeBase) {
      this.$confirm('此操作将永久删除该知识库, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('dataCenter/deleteKnowledgeBase', knowledgeBase.id)
          .then(() => {
            this.$message.success('删除知识库成功')
            this.handleBackToList()
          })
          .catch(error => {
            console.error('删除知识库失败:', error)
            this.$message.error('删除知识库失败')
          })
      }).catch(() => {})
    },
    
    // 处理表单提交
    handleFormSubmit(formData) {
      if (this.formType === 'create') {
        // 创建知识库
        this.$store.dispatch('dataCenter/createKnowledgeBase', formData)
          .then((response) => {
            this.$message.success('创建知识库成功')
            this.formVisible = false
            // 刷新知识库列表
            this.$store.dispatch('dataCenter/fetchKnowledgeBases')
          })
          .catch(error => {
            console.error('创建知识库失败:', error)
            this.$message.error(error.message || '创建知识库失败，请检查您的权限')
          })
      } else {
        // 更新知识库
        this.$store.dispatch('dataCenter/updateKnowledgeBase', {
          id: formData.id,
          data: formData
        })
          .then((response) => {
            this.$message.success('更新知识库成功')
            this.formVisible = false
            
            // 如果当前在详情页，刷新详情
            if (this.currentView === 'detail' && this.currentKnowledgeBaseId === formData.id) {
              this.$store.dispatch('dataCenter/fetchKnowledgeBaseDetail', formData.id)
            }
            // 刷新知识库列表
            this.$store.dispatch('dataCenter/fetchKnowledgeBases')
          })
          .catch(error => {
            console.error('更新知识库失败:', error)
            this.$message.error(error.message || '更新知识库失败，请检查您的权限')
          })
      }
    },
    
    // 重置表单
    resetForm() {
      if (this.$refs.knowledgeBaseForm) {
        this.$refs.knowledgeBaseForm.resetForm()
      }
    },
    
    // 刷新知识库数据
    refreshKnowledgeBases() {
      this.$store.dispatch('dataCenter/fetchKnowledgeBases').then(() => {
        this.$notify({
          title: '刷新成功',
          message: `加载了${this.$store.state.dataCenter.knowledgeBases.length}个知识库`,
          type: 'success'
        });
      }).catch(error => {
        this.$notify.error({
          title: '刷新失败',
          message: error.message || '未知错误'
        });
      });
    },
    
    // 打开创建知识库对话框
    openCreateDialog() {
      this.formType = 'create'
      this.currentKnowledgeBase = {
        name: '',
        description: '',
        content: ''
      }
      this.formVisible = true
    }
  }
}
</script>

<style scoped>
.knowledge-base-management {
  min-height: 500px;
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

.create-btn {
  background-color: #67C23A;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 3px;
}
</style> 