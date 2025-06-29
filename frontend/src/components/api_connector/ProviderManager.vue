<template>
  <div class="provider-manager">
    <el-card>
      <div slot="header" class="card-header">
        <span>API提供商管理</span>
        <div class="header-actions">
          <el-button 
            size="small" 
            type="primary" 
            icon="el-icon-plus" 
            @click="handleAddProvider"
          >添加提供商</el-button>
        </div>
      </div>
      
      <!-- 提供商列表 -->
      <el-table
        :data="providersList"
        style="width: 100%"
        v-loading="loading"
        border
        stripe
      >
        <el-table-column
          type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="provider-detail">
              <el-form-item label="提供商代码">
                <span>{{ props.row.code }}</span>
              </el-form-item>
              <el-form-item label="创建时间">
                <span>{{ formatDate(props.row.created_at) }}</span>
              </el-form-item>
              <el-form-item label="更新时间">
                <span>{{ formatDate(props.row.updated_at) }}</span>
              </el-form-item>
              <el-form-item label="API基础URL" v-if="props.row.base_url">
                <span>{{ props.row.base_url }}</span>
              </el-form-item>
              <el-form-item label="描述" v-if="props.row.description">
                <span>{{ props.row.description }}</span>
              </el-form-item>
              
              <!-- 模型列表 -->
              <div class="model-list-container">
                <h4>支持的模型</h4>
                <el-table
                  :data="props.row.models || []"
                  style="width: 100%"
                  border
                  size="small">
                  <el-table-column prop="model_id" label="模型ID" width="180"></el-table-column>
                  <el-table-column prop="name" label="模型名称" width="180"></el-table-column>
                  <el-table-column prop="type" label="类型">
                    <template slot-scope="scope">
                      <el-tag size="mini" :type="getModelTypeTag(scope.row.type)">
                        {{ getModelTypeText(scope.row.type) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="token_limit" label="Token上限"></el-table-column>
                  <el-table-column prop="pricing" label="定价($/1K tokens)">
                    <template slot-scope="scope">
                      <div v-if="scope.row.pricing">
                        输入: ${{ scope.row.pricing.input || 0 }} / 
                        输出: ${{ scope.row.pricing.output || 0 }}
                      </div>
                      <div v-else>-</div>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-form>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="name"
          label="提供商名称"
          width="150">
        </el-table-column>
        
        <el-table-column
          prop="code"
          label="提供商代码"
          width="120">
        </el-table-column>
        
        <el-table-column
          label="状态"
          width="100">
          <template slot-scope="scope">
            <el-switch
              v-model="scope.row.is_active"
              @change="(val) => handleStatusChange(scope.row, val)"
              active-color="#13ce66"
              inactive-color="#ff4949">
            </el-switch>
          </template>
        </el-table-column>
        
        <el-table-column
          label="身份验证类型"
          width="150">
          <template slot-scope="scope">
            <el-tag size="medium">{{ getAuthTypeText(scope.row.auth_type) }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="auth_credentials.is_configured"
          label="凭证配置"
          width="100">
          <template slot-scope="scope">
            <el-tag 
              size="medium" 
              :type="scope.row.auth_credentials?.is_configured ? 'success' : 'danger'">
              {{ scope.row.auth_credentials?.is_configured ? '已配置' : '未配置' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="models_count"
          label="模型数量"
          width="100">
          <template slot-scope="scope">
            <el-tag size="medium" type="info">{{ scope.row.models?.length || 0 }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column
          label="操作"
          width="250">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              icon="el-icon-key"
              @click="openCredentialsDialog(scope.row)">配置凭证</el-button>
            <el-button
              size="mini"
              type="success"
              icon="el-icon-refresh"
              @click="syncModels(scope.row)"
              :disabled="!scope.row.auth_credentials?.is_configured">同步模型</el-button>
            <el-button
              size="mini"
              type="danger"
              icon="el-icon-delete"
              @click="handleDelete(scope.row)"
              :disabled="!scope.row.can_delete">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加提供商弹窗 -->
    <el-dialog
      title="添加API提供商"
      :visible.sync="addDialogVisible"
      width="500px">
      <el-form :model="providerForm" :rules="providerFormRules" ref="providerForm" label-width="120px">
        <el-form-item label="提供商名称" prop="name">
          <el-input v-model="providerForm.name" placeholder="例如: OpenAI"></el-input>
        </el-form-item>
        
        <el-form-item label="提供商代码" prop="code">
          <el-input v-model="providerForm.code" placeholder="例如: openai"></el-input>
        </el-form-item>
        
        <el-form-item label="API基础URL" prop="base_url">
          <el-input v-model="providerForm.base_url" placeholder="例如: https://api.openai.com/v1"></el-input>
        </el-form-item>
        
        <el-form-item label="认证类型" prop="auth_type">
          <el-select v-model="providerForm.auth_type" placeholder="请选择认证类型" style="width: 100%;">
            <el-option label="API Key" value="api_key"></el-option>
            <el-option label="OAuth 2.0" value="oauth2"></el-option>
            <el-option label="基本认证" value="basic"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="providerForm.description" placeholder="提供商描述信息"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitProviderForm" :loading="submitting">确定</el-button>
      </span>
    </el-dialog>
    
    <!-- 配置凭证弹窗 -->
    <el-dialog
      :title="`配置 ${currentProvider?.name || ''} 凭证`"
      :visible.sync="credentialsDialogVisible"
      width="600px">
      <el-form :model="credentialsForm" :rules="credentialsFormRules" ref="credentialsForm" label-width="120px" v-if="currentProvider">
        <!-- API Key认证 -->
        <template v-if="currentProvider.auth_type === 'api_key'">
          <el-form-item label="API Key" prop="api_key">
            <el-input v-model="credentialsForm.api_key" placeholder="输入API Key" type="password" show-password></el-input>
          </el-form-item>
          
          <el-form-item label="组织ID" prop="organization_id" v-if="currentProvider.code === 'openai'">
            <el-input v-model="credentialsForm.organization_id" placeholder="输入OpenAI组织ID (可选)"></el-input>
          </el-form-item>
        </template>
        
        <!-- OAuth2认证 -->
        <template v-if="currentProvider.auth_type === 'oauth2'">
          <el-form-item label="客户端ID" prop="client_id">
            <el-input v-model="credentialsForm.client_id" placeholder="输入客户端ID"></el-input>
          </el-form-item>
          
          <el-form-item label="客户端密钥" prop="client_secret">
            <el-input v-model="credentialsForm.client_secret" placeholder="输入客户端密钥" type="password" show-password></el-input>
          </el-form-item>
          
          <el-form-item label="Token URL" prop="token_url">
            <el-input v-model="credentialsForm.token_url" placeholder="输入Token获取URL"></el-input>
          </el-form-item>
          
          <el-form-item label="授权范围" prop="scope">
            <el-input v-model="credentialsForm.scope" placeholder="输入授权范围 (多个用空格分隔)"></el-input>
          </el-form-item>
        </template>
        
        <!-- 基本认证 -->
        <template v-if="currentProvider.auth_type === 'basic'">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="credentialsForm.username" placeholder="输入用户名"></el-input>
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input v-model="credentialsForm.password" placeholder="输入密码" type="password" show-password></el-input>
          </el-form-item>
        </template>
        
        <!-- Azure OpenAI特殊配置 -->
        <template v-if="currentProvider.code === 'azure'">
          <el-form-item label="API版本" prop="api_version">
            <el-input v-model="credentialsForm.api_version" placeholder="例如: 2023-05-15"></el-input>
          </el-form-item>
          
          <el-form-item label="资源名称" prop="resource_name">
            <el-input v-model="credentialsForm.resource_name" placeholder="Azure资源名称"></el-input>
          </el-form-item>
        </template>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="credentialsDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCredentials" :loading="submitting">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProviderManager',
  data() {
    return {
      // 提供商列表
      providersList: [],
      loading: false,
      
      // 添加提供商
      addDialogVisible: false,
      providerForm: {
        name: '',
        code: '',
        base_url: '',
        auth_type: 'api_key',
        description: ''
      },
      providerFormRules: {
        name: [
          { required: true, message: '请输入提供商名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        code: [
          { required: true, message: '请输入提供商代码', trigger: 'blur' },
          { pattern: /^[a-z0-9_]+$/, message: '只能包含小写字母、数字和下划线', trigger: 'blur' }
        ],
        auth_type: [
          { required: true, message: '请选择认证类型', trigger: 'change' }
        ]
      },
      
      // 凭证配置
      credentialsDialogVisible: false,
      currentProvider: null,
      credentialsForm: {},
      credentialsFormRules: {
        api_key: [
          { required: true, message: '请输入API Key', trigger: 'blur' }
        ],
        client_id: [
          { required: true, message: '请输入客户端ID', trigger: 'blur' }
        ],
        client_secret: [
          { required: true, message: '请输入客户端密钥', trigger: 'blur' }
        ],
        token_url: [
          { required: true, message: '请输入Token URL', trigger: 'blur' }
        ],
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      submitting: false
    }
  },
  created() {
    this.loadProviders()
  },
  methods: {
    // 加载提供商列表
    async loadProviders() {
      this.loading = true
      try {
        const response = await axios.get('/api/api-connector/providers/')
        this.providersList = response.data
      } catch (error) {
        console.error('加载提供商失败:', error)
        this.$message.error('加载提供商失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.loading = false
      }
    },
    
    // 添加提供商
    handleAddProvider() {
      this.providerForm = {
        name: '',
        code: '',
        base_url: '',
        auth_type: 'api_key',
        description: ''
      }
      this.addDialogVisible = true
      this.$nextTick(() => {
        this.$refs.providerForm && this.$refs.providerForm.clearValidate()
      })
    },
    
    // 提交添加提供商表单
    submitProviderForm() {
      this.$refs.providerForm.validate(async (valid) => {
        if (!valid) return
        
        this.submitting = true
        try {
          await axios.post('/api/api-connector/providers/', this.providerForm)
          this.$message.success('提供商添加成功')
          this.addDialogVisible = false
          this.loadProviders()
        } catch (error) {
          console.error('添加提供商失败:', error)
          this.$message.error('添加提供商失败: ' + (error.response?.data?.detail || error.message))
        } finally {
          this.submitting = false
        }
      })
    },
    
    // 打开凭证配置弹窗
    openCredentialsDialog(provider) {
      this.currentProvider = provider
      this.credentialsForm = {}
      this.credentialsDialogVisible = true
      
      // 获取已有凭证配置
      this.getProviderCredentials(provider.id)
    },
    
    // 获取提供商凭证信息（只获取配置结构，不返回敏感数据）
    async getProviderCredentials(providerId) {
      try {
        const response = await axios.get(`/api/api-connector/providers/${providerId}/credentials/`)
        // 凭证信息通常只返回结构，不返回实际值
        this.credentialsForm = response.data || {}
      } catch (error) {
        console.error('获取凭证信息失败:', error)
        this.$message.warning('获取凭证信息失败，请重新配置')
      }
    },
    
    // 保存凭证配置
    saveCredentials() {
      if (!this.currentProvider) return
      
      this.$refs.credentialsForm.validate(async (valid) => {
        if (!valid) return
        
        this.submitting = true
        try {
          await axios.put(`/api/api-connector/providers/${this.currentProvider.id}/credentials/`, this.credentialsForm)
          this.$message.success('凭证配置成功')
          this.credentialsDialogVisible = false
          this.loadProviders()
        } catch (error) {
          console.error('保存凭证失败:', error)
          this.$message.error('保存凭证失败: ' + (error.response?.data?.detail || error.message))
        } finally {
          this.submitting = false
        }
      })
    },
    
    // 同步模型列表
    async syncModels(provider) {
      try {
        this.$message.info('正在同步模型列表，请稍候...')
        await axios.post(`/api/api-connector/providers/${provider.id}/sync-models/`)
        this.$message.success('模型同步成功')
        this.loadProviders()
      } catch (error) {
        console.error('同步模型失败:', error)
        this.$message.error('同步模型失败: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    // 修改提供商状态
    async handleStatusChange(provider, status) {
      try {
        await axios.patch(`/api/api-connector/providers/${provider.id}/`, {
          is_active: status
        })
        this.$message.success(`${provider.name} ${status ? '已启用' : '已禁用'}`)
      } catch (error) {
        console.error('修改状态失败:', error)
        this.$message.error('修改状态失败')
        // 还原状态
        provider.is_active = !status
      }
    },
    
    // 删除提供商
    handleDelete(provider) {
      this.$confirm(`确定要删除提供商 ${provider.name} 吗？此操作不可恢复！`, '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await axios.delete(`/api/api-connector/providers/${provider.id}/`)
          this.$message.success('提供商删除成功')
          this.loadProviders()
        } catch (error) {
          console.error('删除提供商失败:', error)
          this.$message.error('删除提供商失败: ' + (error.response?.data?.detail || error.message))
        }
      }).catch(() => {
        // 取消删除
      })
    },
    
    // 获取认证类型显示文本
    getAuthTypeText(authType) {
      const authTypes = {
        'api_key': 'API Key',
        'oauth2': 'OAuth 2.0',
        'basic': '基本认证'
      }
      return authTypes[authType] || authType
    },
    
    // 获取模型类型标签
    getModelTypeTag(type) {
      const typeColors = {
        'text': 'success',
        'chat': 'primary',
        'embedding': 'warning',
        'image': 'danger',
        'audio': 'info'
      }
      return typeColors[type] || ''
    },
    
    // 获取模型类型显示文本
    getModelTypeText(type) {
      const typeTexts = {
        'text': '文本生成',
        'chat': '对话',
        'embedding': '嵌入向量',
        'image': '图像生成',
        'audio': '语音处理'
      }
      return typeTexts[type] || type
    },
    
    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleString()
    }
  }
}
</script>

<style scoped>
.provider-manager {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.provider-detail {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.provider-detail .el-form-item {
  margin-right: 30px;
  margin-bottom: 15px;
}

.model-list-container {
  width: 100%;
  margin-top: 15px;
}

.model-list-container h4 {
  margin-bottom: 10px;
  font-weight: bold;
}
</style> 