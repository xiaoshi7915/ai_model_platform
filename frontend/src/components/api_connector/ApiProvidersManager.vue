<template>
  <div class="providers-manager">
    <div class="toolbar">
      <el-button type="primary" @click="showAddDialog">
        <i class="el-icon-plus"></i> 添加API提供商
      </el-button>
    </div>
    
    <el-table 
      :data="providers" 
      border 
      style="width: 100%; margin-top: 20px;"
      v-loading="loading"
    >
      <el-table-column prop="name" label="提供商名称"></el-table-column>
      <el-table-column prop="provider_type_display" label="类型"></el-table-column>
      <el-table-column prop="base_url" label="基础URL" show-overflow-tooltip></el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.is_active ? 'success' : 'info'">
            {{ scope.row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" align="center">
        <template slot-scope="scope">
          <el-button 
            type="primary" 
            size="mini" 
            plain
            @click="editProvider(scope.row)"
          >编辑</el-button>
          <el-button 
            type="danger" 
            size="mini" 
            plain
            @click="deleteProvider(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 添加/编辑提供商对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="50%">
      <el-form 
        :model="formData" 
        :rules="formRules" 
        ref="providerForm" 
        label-width="100px"
      >
        <el-form-item label="提供商名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入提供商名称"></el-input>
        </el-form-item>
        
        <el-form-item label="提供商类型" prop="provider_type">
          <el-select v-model="formData.provider_type" placeholder="请选择提供商类型" style="width: 100%;">
            <el-option
              v-for="item in providerTypes"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input 
            type="textarea" 
            :rows="3" 
            v-model="formData.description" 
            placeholder="请输入提供商描述"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="基础URL" prop="base_url">
          <el-input 
            v-model="formData.base_url" 
            placeholder="请输入API的基础URL，例如: https://api.openai.com/v1/"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="文档URL" prop="docs_url">
          <el-input 
            v-model="formData.docs_url" 
            placeholder="请输入API文档URL（可选）"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-switch
            v-model="formData.is_active"
            active-text="启用"
            inactive-text="禁用">
          </el-switch>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProvider" :loading="submitting">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import api from '@/api'

export default {
  name: 'ApiProvidersManager',
  data() {
    return {
      providers: [],
      providerTypes: [],
      loading: false,
      submitting: false,
      dialogVisible: false,
      dialogTitle: '添加API提供商',
      isEdit: false,
      formData: this.getDefaultFormData(),
      formRules: {
        name: [
          { required: true, message: '请输入提供商名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        provider_type: [
          { required: true, message: '请选择提供商类型', trigger: 'change' }
        ],
        base_url: [
          { required: true, message: '请输入基础URL', trigger: 'blur' },
          { pattern: /^https?:\/\/.+/, message: 'URL必须以http://或https://开头', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.loadProviderTypes()
    this.loadProviders()
  },
  methods: {
    getDefaultFormData() {
      return {
        name: '',
        provider_type: '',
        description: '',
        base_url: '',
        docs_url: '',
        is_active: true
      }
    },
    async loadProviderTypes() {
      try {
        const response = await api.apiConnector.getProviderTypes()
        this.providerTypes = response || []
      } catch (error) {
        console.error('加载提供商类型失败:', error)
        this.$message.error('加载提供商类型失败')
      }
    },
    async loadProviders() {
      this.loading = true
      try {
        const response = await api.apiConnector.getProviders({ all: true })
        this.providers = response || []
      } catch (error) {
        console.error('加载API提供商失败:', error)
        this.$message.error('加载API提供商失败')
      } finally {
        this.loading = false
      }
    },
    showAddDialog() {
      this.isEdit = false
      this.dialogTitle = '添加API提供商'
      this.formData = this.getDefaultFormData()
      this.dialogVisible = true
    },
    editProvider(row) {
      this.isEdit = true
      this.dialogTitle = '编辑API提供商'
      // 复制数据以避免直接修改表格数据
      this.formData = { ...row }
      this.dialogVisible = true
    },
    async saveProvider() {
      this.$refs.providerForm.validate(async valid => {
        if (!valid) return
        
        this.submitting = true
        try {
          let response
          if (this.isEdit) {
            // 编辑现有提供商
            response = await api.apiConnector.updateProvider(
              this.formData.id, 
              this.formData
            )
          } else {
            // 添加新提供商
            response = await api.apiConnector.createProvider(this.formData)
          }
          
          this.$message.success(this.isEdit ? '更新成功' : '添加成功')
          this.dialogVisible = false
          this.loadProviders()
        } catch (error) {
          console.error('保存API提供商失败:', error)
          this.$message.error('保存失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
        } finally {
          this.submitting = false
        }
      })
    },
    async deleteProvider(row) {
      try {
        await this.$confirm('删除提供商将同时删除与其关联的所有连接。确定要删除吗？', '确认删除', {
          type: 'warning'
        })
        
        await api.apiConnector.deleteProvider(row.id)
        this.$message.success('删除成功')
        this.loadProviders()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除API提供商失败:', error)
          this.$message.error('删除失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
        }
      }
    }
  }
}
</script>

<style scoped>
.providers-manager {
  width: 100%;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}
</style> 