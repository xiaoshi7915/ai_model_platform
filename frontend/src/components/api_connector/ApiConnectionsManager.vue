<template>
  <div class="connections-manager">
    <div class="toolbar">
      <el-button type="primary" @click="showAddDialog">
        <i class="el-icon-plus"></i> 添加API连接
      </el-button>
      <el-select 
        v-model="providerFilter" 
        placeholder="按提供商筛选" 
        clearable
        @change="loadConnections"
        style="margin-left: 15px; width: 150px;"
      >
        <el-option
          v-for="item in providers"
          :key="item.id"
          :label="item.name"
          :value="item.id">
        </el-option>
      </el-select>
    </div>
    
    <el-table 
      :data="connections" 
      border 
      style="width: 100%; margin-top: 20px;"
      v-loading="loading"
    >
      <el-table-column prop="name" label="连接名称"></el-table-column>
      <el-table-column prop="provider_name" label="提供商"></el-table-column>
      <el-table-column label="默认" width="100" align="center">
        <template slot-scope="scope">
          <el-tag type="success" v-if="scope.row.is_default">默认</el-tag>
          <el-button 
            v-else 
            type="text" 
            size="small"
            @click="setAsDefault(scope.row)"
          >设为默认</el-button>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.is_active ? 'success' : 'info'">
            {{ scope.row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250" align="center">
        <template slot-scope="scope">
          <el-button 
            type="primary" 
            size="mini" 
            plain
            @click="editConnection(scope.row)"
          >编辑</el-button>
          <el-button 
            type="warning" 
            size="mini" 
            plain
            @click="testConnection(scope.row)"
          >测试</el-button>
          <el-button 
            type="danger" 
            size="mini" 
            plain
            @click="deleteConnection(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 添加/编辑连接对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="50%">
      <el-form 
        :model="formData" 
        :rules="formRules" 
        ref="connectionForm" 
        label-width="100px"
      >
        <el-form-item label="连接名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入API连接名称"></el-input>
        </el-form-item>
        
        <el-form-item label="API提供商" prop="provider">
          <el-select v-model="formData.provider" placeholder="请选择API提供商" style="width: 100%;">
            <el-option
              v-for="item in providers"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="API密钥" prop="api_key">
          <el-input v-model="formData.api_key" placeholder="请输入API密钥" type="password" show-password></el-input>
        </el-form-item>
        
        <el-form-item label="API密钥2" prop="api_secret" v-if="showSecretKey">
          <el-input v-model="formData.api_secret" placeholder="某些API需要第二个密钥（如Secret Key）" type="password" show-password></el-input>
        </el-form-item>
        
        <el-form-item label="组织ID" prop="org_id" v-if="showOrgId">
          <el-input v-model="formData.org_id" placeholder="某些API需要组织ID（如OpenAI Organization）"></el-input>
        </el-form-item>
        
        <el-form-item label="速率限制" prop="rate_limit">
          <el-input-number v-model="formData.rate_limit" :min="0" :step="1" placeholder="每分钟请求限制（0表示无限制）"></el-input-number>
        </el-form-item>
        
        <el-form-item label="默认连接">
          <el-switch v-model="formData.is_default"></el-switch>
          <span class="tip">设为默认后，同类型的其他连接将不再是默认</span>
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
        <el-button type="primary" @click="saveConnection" :loading="submitting">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import api from '@/api'

export default {
  name: 'ApiConnectionsManager',
  data() {
    return {
      connections: [],
      providers: [],
      loading: false,
      submitting: false,
      dialogVisible: false,
      dialogTitle: '添加API连接',
      isEdit: false,
      providerFilter: '',
      formData: this.getDefaultFormData(),
      formRules: {
        name: [
          { required: true, message: '请输入连接名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        provider: [
          { required: true, message: '请选择API提供商', trigger: 'change' }
        ],
        api_key: [
          { required: true, message: '请输入API密钥', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    showSecretKey() {
      // 对于百度等API，需要显示Secret Key输入框
      const provider = this.getSelectedProviderType()
      return ['baidu', 'custom'].includes(provider)
    },
    showOrgId() {
      // 对于OpenAI，需要显示Organization ID输入框
      const provider = this.getSelectedProviderType()
      return ['openai'].includes(provider)
    }
  },
  created() {
    this.loadProviders()
    this.loadConnections()
  },
  methods: {
    getDefaultFormData() {
      return {
        name: '',
        provider: '',
        api_key: '',
        api_secret: '',
        org_id: '',
        custom_headers: null,
        custom_params: null,
        rate_limit: 0,
        is_default: false,
        is_active: true
      }
    },
    getSelectedProviderType() {
      if (!this.formData.provider) return ''
      const provider = this.providers.find(p => p.id === this.formData.provider)
      return provider ? provider.provider_type : ''
    },
    async loadProviders() {
      try {
        const response = await api.apiConnector.getProviders()
        this.providers = response || []
      } catch (error) {
        console.error('加载API提供商失败:', error)
        this.$message.error('加载API提供商失败')
      }
    },
    async loadConnections() {
      this.loading = true
      try {
        let params = {}
        if (this.providerFilter) {
          params.provider = this.providerFilter
        }
        const response = await api.apiConnector.getConnections(params)
        this.connections = response || []
      } catch (error) {
        console.error('加载API连接失败:', error)
        this.$message.error('加载API连接失败')
      } finally {
        this.loading = false
      }
    },
    showAddDialog() {
      this.isEdit = false
      this.dialogTitle = '添加API连接'
      this.formData = this.getDefaultFormData()
      this.dialogVisible = true
    },
    editConnection(row) {
      this.isEdit = true
      this.dialogTitle = '编辑API连接'
      // 复制数据以避免直接修改表格数据
      this.formData = { ...row }
      this.dialogVisible = true
    },
    async saveConnection() {
      this.$refs.connectionForm.validate(async valid => {
        if (!valid) return
        
        this.submitting = true
        try {
          let response
          if (this.isEdit) {
            // 编辑现有连接
            response = await api.apiConnector.updateConnection(
              this.formData.id,
              this.formData
            )
          } else {
            // 添加新连接
            response = await api.apiConnector.createConnection(this.formData)
          }
          
          this.$message.success(this.isEdit ? '更新成功' : '添加成功')
          this.dialogVisible = false
          this.loadConnections()
        } catch (error) {
          console.error('保存API连接失败:', error)
          this.$message.error('保存失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
        } finally {
          this.submitting = false
        }
      })
    },
    async setAsDefault(row) {
      try {
        await api.apiConnector.setDefaultConnection(row.id)
        this.$message.success('已设为默认连接')
        this.loadConnections()
      } catch (error) {
        console.error('设置默认连接失败:', error)
        this.$message.error('设置失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
      }
    },
    async testConnection(row) {
      try {
        this.$message.info('正在测试连接，请稍候...')
        const response = await api.apiConnector.testConnection(row.id)
        if (response.status === 'success') {
          this.$message.success('连接测试成功')
        } else {
          this.$message.error('连接测试失败: ' + response.message)
        }
      } catch (error) {
        console.error('测试连接失败:', error)
        this.$message.error('测试失败: ' + (error.response?.data?.message || error.message || '未知错误'))
      }
    },
    async deleteConnection(row) {
      try {
        await this.$confirm('确定要删除这个API连接吗？此操作无法撤销', '确认删除', {
          type: 'warning'
        })
        
        await api.apiConnector.deleteConnection(row.id)
        this.$message.success('删除成功')
        this.loadConnections()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除API连接失败:', error)
          this.$message.error('删除失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
        }
      }
    }
  }
}
</script>

<style scoped>
.connections-manager {
  width: 100%;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.tip {
  font-size: 12px;
  color: #909399;
  margin-left: 10px;
}
</style> 