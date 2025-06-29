<template>
  <div class="model-management">
    <!-- 模型列表视图 -->
    <div v-if="currentView === 'list'">
      <model-list
        @view="handleViewModel"
        @create="handleCreateModel"
        @edit="handleEditModel"
      />
    </div>
    
    <!-- 模型详情视图 -->
    <div v-else-if="currentView === 'detail'">
      <model-detail
        :model-id="currentModelId"
        @back="handleBackToList"
        @edit="handleEditModel"
      />
    </div>
    
    <!-- 模型表单（创建/编辑） -->
    <el-dialog
      :title="formType === 'create' ? '创建模型' : '编辑模型'"
      :visible.sync="formVisible"
      width="70%"
      @closed="resetForm"
    >
      <model-form
        ref="modelForm"
        :model="currentModel"
        :type="formType"
        @submit="handleFormSubmit"
        @cancel="formVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script>
import ModelList from './ModelList.vue'
import ModelDetail from './ModelDetail.vue'
import ModelForm from './ModelForm.vue'

export default {
  name: 'ModelManagement',
  components: {
    ModelList,
    ModelDetail,
    ModelForm
  },
  data() {
    return {
      currentView: 'list', // 'list' 或 'detail'
      currentModelId: null,
      currentModel: null,
      formVisible: false,
      formType: 'create' // 'create' 或 'edit'
    }
  },
  methods: {
    // 处理查看模型
    handleViewModel(model) {
      this.currentModelId = model.id
      this.currentView = 'detail'
    },
    
    // 处理返回列表
    handleBackToList() {
      this.currentView = 'list'
      this.currentModelId = null
    },
    
    // 处理创建模型
    handleCreateModel() {
      this.formType = 'create'
      this.currentModel = {
        name: '',
        version: '1.0.0',
        description: '',
        dataset: null,
        parameters: {}
      }
      this.formVisible = true
    },
    
    // 处理编辑模型
    handleEditModel(model) {
      this.formType = 'edit'
      this.currentModel = JSON.parse(JSON.stringify(model))
      this.formVisible = true
    },
    
    // 处理表单提交
    handleFormSubmit(formData) {
      if (this.formType === 'create') {
        // 创建模型
        this.$store.dispatch('trainingCenter/createModel', formData)
          .then(() => {
            this.$message.success('创建模型成功')
            this.formVisible = false
          })
          .catch(error => {
            console.error('创建模型失败:', error)
            this.$message.error('创建模型失败')
          })
      } else {
        // 更新模型
        this.$store.dispatch('trainingCenter/updateModel', {
          id: formData.id,
          data: formData
        })
          .then(() => {
            this.$message.success('更新模型成功')
            this.formVisible = false
            
            // 如果当前在详情页，刷新详情
            if (this.currentView === 'detail' && this.currentModelId === formData.id) {
              this.$store.dispatch('trainingCenter/fetchModelDetail', formData.id)
            }
          })
          .catch(error => {
            console.error('更新模型失败:', error)
            this.$message.error('更新模型失败')
          })
      }
    },
    
    // 重置表单
    resetForm() {
      if (this.$refs.modelForm) {
        this.$refs.modelForm.resetForm()
      }
    }
  },
  created() {
    // 从路由参数中获取视图和模型ID
    const { view, modelId } = this.$route.query
    
    if (view) {
      this.currentView = view
    }
    
    if (modelId) {
      this.currentModelId = modelId
    }
  },
  watch: {
    // 监听视图和模型ID变化，更新路由
    currentView(newVal) {
      const query = { ...this.$route.query, view: newVal }
      if (newVal !== 'detail') {
        delete query.modelId
      }
      this.$router.replace({ query })
    },
    currentModelId(newVal) {
      if (newVal && this.currentView === 'detail') {
        this.$router.replace({ query: { ...this.$route.query, modelId: newVal } })
      }
    }
  }
}
</script>

<style scoped>
.model-management {
  min-height: 500px;
}
</style> 