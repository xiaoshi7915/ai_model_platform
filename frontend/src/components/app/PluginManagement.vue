<template>
  <div class="plugin-management">
    <!-- 列表模式 -->
    <div v-if="currentView === 'list'">
      <plugin-list
        @create="handleCreate"
        @detail="handleViewDetail"
        @edit="handleEdit"
        @delete="handleDelete"
      ></plugin-list>
    </div>

    <!-- 详情模式 -->
    <div v-else-if="currentView === 'detail'">
      <div class="detail-header">
        <el-button icon="el-icon-back" @click="currentView = 'list'">返回列表</el-button>
      </div>
      <plugin-detail
        :plugin="currentPlugin"
        @edit="handleEdit"
        @delete="handleDelete"
      ></plugin-detail>
    </div>

    <!-- 表单模式 -->
    <div v-else-if="currentView === 'form'">
      <div class="form-header">
        <el-button icon="el-icon-back" @click="currentView = 'list'">返回列表</el-button>
      </div>
      <plugin-form
        :plugin-data="currentPlugin"
        :is-edit="isEdit"
        @submit="handleFormSubmit"
        @cancel="currentView = 'list'"
        ref="pluginForm"
      ></plugin-form>
    </div>

    <!-- 确认删除对话框 -->
    <el-dialog
      title="确认删除"
      :visible.sync="deleteDialogVisible"
      width="30%"
    >
      <p>确定要删除插件 "{{ pluginToDelete?.name }} {{ pluginToDelete?.version }}" 吗？此操作不可恢复。</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmDelete" :loading="deleting">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import PluginList from './PluginList.vue'
import PluginDetail from './PluginDetail.vue'
import PluginForm from './PluginForm.vue'
import { mapActions } from 'vuex'

export default {
  name: 'PluginManagement',
  components: {
    PluginList,
    PluginDetail,
    PluginForm
  },
  data() {
    return {
      currentView: 'list', // list, detail, form
      currentPlugin: null,
      isEdit: false,
      deleteDialogVisible: false,
      pluginToDelete: null,
      deleting: false
    }
  },
  methods: {
    ...mapActions('appCenter', [
      'createPlugin',
      'updatePlugin',
      'deletePlugin'
    ]),
    
    // 处理创建插件
    handleCreate() {
      this.currentPlugin = null
      this.isEdit = false
      this.currentView = 'form'
    },
    
    // 处理查看详情
    handleViewDetail(plugin) {
      this.currentPlugin = plugin
      this.currentView = 'detail'
    },
    
    // 处理编辑插件
    handleEdit(plugin) {
      this.currentPlugin = plugin
      this.isEdit = true
      this.currentView = 'form'
    },
    
    // 处理表单提交
    async handleFormSubmit(formData) {
      try {
        if (this.isEdit) {
          // 添加ID
          formData.append('id', this.currentPlugin.id)
          await this.updatePlugin(formData)
          this.$message.success('插件更新成功')
        } else {
          await this.createPlugin(formData)
          this.$message.success('插件上传成功')
        }
        this.currentView = 'list'
      } catch (error) {
        this.$message.error(error.message || '操作失败')
      } finally {
        this.$refs.pluginForm.resetForm()
      }
    },
    
    // 处理删除插件
    handleDelete(plugin) {
      this.pluginToDelete = plugin
      this.deleteDialogVisible = true
    },
    
    // 确认删除
    async confirmDelete() {
      if (!this.pluginToDelete) return
      
      this.deleting = true
      try {
        await this.deletePlugin(this.pluginToDelete.id)
        this.$message.success('插件已删除')
        this.deleteDialogVisible = false
        
        // 如果当前在详情页面且删除的是当前查看的插件，则返回列表页
        if (this.currentView === 'detail' && this.currentPlugin.id === this.pluginToDelete.id) {
          this.currentView = 'list'
        }
      } catch (error) {
        this.$message.error(error.message || '删除失败')
      } finally {
        this.deleting = false
        this.pluginToDelete = null
      }
    }
  }
}
</script>

<style scoped>
.plugin-management {
  padding: 20px;
  min-height: calc(100vh - 84px);
  background-color: #f5f7fa;
}

.detail-header,
.form-header {
  margin-bottom: 20px;
}
</style> 