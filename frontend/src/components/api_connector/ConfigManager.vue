<template>
  <div class="config-manager">
    <el-card>
      <div slot="header" class="card-header">
        <span>API连接器全局配置</span>
      </div>
      
      <el-form
        :model="formData"
        :rules="formRules"
        ref="configForm"
        label-width="180px"
        v-loading="loading"
      >
        <el-form-item label="默认请求超时(秒)" prop="default_timeout">
          <el-input-number 
            v-model="formData.default_timeout" 
            :min="1" 
            :max="300" 
            style="width: 180px;"
          ></el-input-number>
          <div class="form-tip">API请求的默认超时时间，单位为秒</div>
        </el-form-item>
        
        <el-form-item label="日志保留天数" prop="log_retention_days">
          <el-input-number 
            v-model="formData.log_retention_days" 
            :min="1" 
            :max="365" 
            style="width: 180px;"
          ></el-input-number>
          <div class="form-tip">API请求日志的保留时间，超过该时间的日志将被自动清理</div>
        </el-form-item>
        
        <el-form-item label="启用API请求日志" prop="enable_request_logging">
          <el-switch
            v-model="formData.enable_request_logging"
            active-text="启用"
            inactive-text="禁用">
          </el-switch>
          <div class="form-tip">记录所有API请求和响应的详细日志</div>
        </el-form-item>
        
        <el-form-item label="日志敏感信息脱敏" prop="mask_sensitive_data">
          <el-switch
            v-model="formData.mask_sensitive_data"
            active-text="启用"
            inactive-text="禁用">
          </el-switch>
          <div class="form-tip">在日志中对敏感信息（如API密钥、个人信息等）进行脱敏处理</div>
        </el-form-item>
        
        <el-form-item label="启用请求速率限制" prop="enable_rate_limiting">
          <el-switch
            v-model="formData.enable_rate_limiting"
            active-text="启用"
            inactive-text="禁用">
          </el-switch>
          <div class="form-tip">启用API请求的速率限制功能，防止过度请求</div>
        </el-form-item>
        
        <el-form-item v-if="formData.enable_rate_limiting" label="速率限制(次/分钟)" prop="rate_limit_per_minute">
          <el-input-number 
            v-model="formData.rate_limit_per_minute" 
            :min="1" 
            :max="1000" 
            style="width: 180px;"
          ></el-input-number>
          <div class="form-tip">每分钟允许的最大API请求次数</div>
        </el-form-item>
        
        <el-form-item label="启用缓存" prop="enable_caching">
          <el-switch
            v-model="formData.enable_caching"
            active-text="启用"
            inactive-text="禁用">
          </el-switch>
          <div class="form-tip">启用API响应缓存，可减少重复请求并提高性能</div>
        </el-form-item>
        
        <el-form-item v-if="formData.enable_caching" label="缓存过期时间(分钟)" prop="cache_ttl_minutes">
          <el-input-number 
            v-model="formData.cache_ttl_minutes" 
            :min="1" 
            :max="1440" 
            style="width: 180px;"
          ></el-input-number>
          <div class="form-tip">缓存的有效期，超过该时间后缓存将失效</div>
        </el-form-item>
        
        <el-form-item label="故障转移策略" prop="failover_strategy">
          <el-select v-model="formData.failover_strategy" style="width: 100%;">
            <el-option
              v-for="item in failoverStrategies"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <div class="form-tip">当API请求失败时的处理策略</div>
        </el-form-item>
        
        <el-form-item label="全局代理服务器" prop="proxy_url">
          <el-input v-model="formData.proxy_url" placeholder="http://proxy.example.com:8080"></el-input>
          <div class="form-tip">用于所有API请求的HTTP代理服务器地址</div>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="saveConfig" :loading="submitting">保存配置</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ConfigManager',
  data() {
    return {
      loading: false,
      submitting: false,
      formData: {
        default_timeout: 30,
        log_retention_days: 30,
        enable_request_logging: true,
        mask_sensitive_data: true,
        enable_rate_limiting: false,
        rate_limit_per_minute: 60,
        enable_caching: false,
        cache_ttl_minutes: 60,
        failover_strategy: 'none',
        proxy_url: ''
      },
      formRules: {
        default_timeout: [
          { required: true, message: '请输入默认超时时间', trigger: 'blur' }
        ],
        log_retention_days: [
          { required: true, message: '请输入日志保留天数', trigger: 'blur' }
        ],
        rate_limit_per_minute: [
          { required: true, message: '请输入速率限制', trigger: 'blur' }
        ],
        cache_ttl_minutes: [
          { required: true, message: '请输入缓存过期时间', trigger: 'blur' }
        ],
        proxy_url: [
          { pattern: '^(http|https)://.+|^$', message: '代理URL格式不正确', trigger: 'blur' }
        ]
      },
      failoverStrategies: [
        { label: '不启用', value: 'none' },
        { label: '重试', value: 'retry' },
        { label: '备用提供商', value: 'alternative_provider' },
        { label: '降级服务', value: 'degraded_service' }
      ]
    }
  },
  created() {
    this.loadConfig()
  },
  methods: {
    async loadConfig() {
      this.loading = true
      try {
        const response = await axios.get('/api/api-connector/config/')
        if (response.data) {
          this.formData = { ...this.formData, ...response.data }
        }
      } catch (error) {
        console.error('加载配置失败:', error)
        this.$message.error('加载配置失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
      } finally {
        this.loading = false
      }
    },
    async saveConfig() {
      this.$refs.configForm.validate(async valid => {
        if (!valid) return
        
        this.submitting = true
        try {
          await axios.put('/api/api-connector/config/', this.formData)
          this.$message.success('保存配置成功')
        } catch (error) {
          console.error('保存配置失败:', error)
          this.$message.error('保存失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
        } finally {
          this.submitting = false
        }
      })
    },
    resetForm() {
      this.$confirm('确定要重置表单吗？所有修改将丢失。', '确认重置', {
        type: 'warning'
      }).then(() => {
        this.loadConfig()
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.config-manager {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  line-height: 1.2;
}
</style> 