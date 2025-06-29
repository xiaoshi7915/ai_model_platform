<template>
  <div class="application-management">
    <!-- 列表模式 -->
    <div v-if="currentView === 'list'">
      <application-list
        @create="handleCreate"
        @create-wizard="handleCreateWizard"
        @view="handleView"
        @edit="handleEdit"
        @deploy="handleDeploy"
        @stop="handleStop"
        @delete="handleDelete"
      ></application-list>
    </div>

    <!-- 详情模式 -->
    <div v-else-if="currentView === 'detail'">
      <div class="detail-header">
        <el-button icon="el-icon-back" @click="currentView = 'list'">返回列表</el-button>
      </div>
      <application-detail
        :application-id="currentApplicationId"
        @back="handleBack"
        @edit="handleEdit"
        @deploy="handleDeploy"
        @stop="handleStop"
        @delete="handleDelete"
      ></application-detail>
    </div>

    <!-- 表单模式 -->
    <div v-else-if="currentView === 'form'">
      <div class="form-header">
        <el-button icon="el-icon-back" @click="currentView = 'list'">返回列表</el-button>
      </div>
      <application-form
        :edit-mode="editMode"
        :application-id="currentApplicationId"
        @success="handleFormSuccess"
        @cancel="handleBack"
        ref="applicationForm"
      ></application-form>
    </div>
    
    <!-- 向导模式 -->
    <div v-else-if="currentView === 'wizard'">
      <div class="wizard-header">
        <el-button icon="el-icon-back" @click="currentView = 'list'">返回列表</el-button>
      </div>
      <application-wizard
        :is-edit="editMode"
        :application="currentApplication"
        @complete="handleFormSuccess"
        @cancel="handleBack"
      ></application-wizard>
    </div>

    <!-- 确认删除对话框 -->
    <el-dialog
      title="确认删除"
      :visible.sync="deleteDialogVisible"
      width="30%"
    >
      <p>确定要删除应用 "{{ applicationToDelete?.name }}" 吗？此操作不可恢复。</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmDelete" :loading="deleting">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import ApplicationList from './ApplicationList.vue'
import ApplicationDetail from './ApplicationDetail.vue'
import ApplicationForm from './ApplicationForm.vue'
import ApplicationWizard from './ApplicationWizard.vue'
import { mapActions, mapState } from 'vuex'

export default {
  name: 'ApplicationManagement',
  components: {
    ApplicationList,
    ApplicationDetail,
    ApplicationForm,
    ApplicationWizard
  },
  data() {
    return {
      currentView: 'list', // list, detail, form, wizard
      currentApplicationId: null,
      editMode: false,
      deleteDialogVisible: false,
      deleting: false,
      applicationToDelete: null
    }
  },
  computed: {
    ...mapState('app', ['applications']),
    currentApplication() {
      if (!this.currentApplicationId) return null
      return this.applications.find(app => app.id === this.currentApplicationId)
    }
  },
  methods: {
    ...mapActions({
      fetchApplications: 'app/fetchApplications',
      createApplication: 'app/createApplication',
      updateApplication: 'app/updateApplication',
      deleteApplication: 'app/deleteApplication',
      deployApplication: 'app/deployApplication',
      stopApplication: 'app/stopApplication'
    }),
    
    // 处理创建应用
    handleCreate() {
      this.editMode = false
      this.currentApplicationId = null
      this.currentView = 'form'
    },
    
    // 处理创建应用(向导模式)
    handleCreateWizard() {
      this.editMode = false
      this.currentApplicationId = null
      this.currentView = 'wizard'
    },
    
    // 处理查看详情
    handleView(applicationId) {
      this.currentApplicationId = applicationId
      this.currentView = 'detail'
    },
    
    // 处理编辑应用
    handleEdit(applicationId) {
      this.editMode = true
      this.currentApplicationId = applicationId
      this.currentView = 'form'
    },
    
    // 处理表单提交
    async handleFormSubmit(formData) {
      try {
        if (this.editMode) {
          await this.updateApplication({
            id: this.currentApplicationId,
            ...formData
          })
          this.$message.success('应用更新成功')
        } else {
          await this.createApplication(formData)
          this.$message.success('应用创建成功')
        }
        this.currentView = 'list'
      } catch (error) {
        this.$message.error(error.message || '操作失败')
      } finally {
        this.$refs.applicationForm.resetForm()
      }
    },
    
    // 处理向导提交
    async handleWizardSubmit(formData) {
      try {
        if (this.editMode) {
          await this.updateApplication({
            id: this.currentApplicationId,
            ...formData
          })
          this.$message.success('应用更新成功')
        } else {
          await this.createApplication(formData)
          this.$message.success('应用创建成功')
        }
        this.currentView = 'list'
      } catch (error) {
        this.$message.error(error.message || '操作失败')
      }
    },
    
    // 处理部署应用
    async handleDeploy(applicationId) {
      try {
        await this.deployApplication(applicationId)
        this.$message.success('应用部署请求已提交')
        
        // 如果当前在详情页面，刷新应用数据
        if (this.currentView === 'detail' && this.currentApplicationId === applicationId) {
          // 这里应该有一个获取单个应用详情的API调用
          // 暂时使用简单的状态更新
          this.currentApplicationId = null
        }
      } catch (error) {
        this.$message.error(error.message || '部署失败')
      }
    },
    
    // 处理停止应用
    async handleStop(applicationId) {
      try {
        await this.stopApplication(applicationId)
        this.$message.success('应用停止请求已提交')
        
        // 如果当前在详情页面，刷新应用数据
        if (this.currentView === 'detail' && this.currentApplicationId === applicationId) {
          // 这里应该有一个获取单个应用详情的API调用
          // 暂时使用简单的状态更新
          this.currentApplicationId = null
        }
      } catch (error) {
        this.$message.error(error.message || '停止失败')
      }
    },
    
    // 处理删除应用
    handleDelete(applicationId) {
      this.applicationToDelete = applicationId
      this.deleteDialogVisible = true
    },
    
    // 确认删除
    async confirmDelete() {
      if (!this.applicationToDelete) return
      
      this.deleting = true
      try {
        await this.deleteApplication(this.applicationToDelete)
        this.$message.success('应用已删除')
        this.deleteDialogVisible = false
        
        // 如果当前在详情页面且删除的是当前查看的应用，则返回列表页
        if (this.currentView === 'detail' && this.currentApplicationId === this.applicationToDelete) {
          this.currentView = 'list'
        }
      } catch (error) {
        this.$message.error(error.message || '删除失败')
      } finally {
        this.deleting = false
        this.applicationToDelete = null
      }
    },
    
    // 处理表单成功
    handleFormSuccess() {
      this.$message.success('操作成功')
      this.currentView = 'list'
    },
    
    // 处理返回
    handleBack() {
      this.currentView = 'list'
      this.currentApplicationId = null
      this.editMode = false
    }
  }
}
</script>

<style scoped>
.application-management {
  padding: 20px;
  min-height: calc(100vh - 84px);
  background-color: #f5f7fa;
}

.detail-header,
.form-header,
.wizard-header {
  margin-bottom: 20px;
}
</style> 