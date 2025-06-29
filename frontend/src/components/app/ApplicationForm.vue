<template>
  <div class="application-form">
    <el-form
      ref="form"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="form-container"
    >
      <!-- 基本信息 -->
      <h3>基本信息</h3>
      <el-form-item label="应用名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入应用名称">
          <template slot="append">
            <el-tooltip content="应用名称将用于标识您的应用，建议使用有意义的名称" placement="top">
              <i class="el-icon-question"></i>
            </el-tooltip>
          </template>
        </el-input>
      </el-form-item>
      
      <el-form-item label="使用模型" prop="model_id">
        <el-select
          v-model="formData.model_id"
          placeholder="请选择模型"
          style="width: 100%"
          @change="handleModelChange"
          filterable
        >
          <el-option
            v-for="model in completedModels"
            :key="model.id"
            :label="`${model.name} (${model.version})`"
            :value="model.id"
          >
            <span style="float: left">{{ model.name }} ({{ model.version }})</span>
            <span style="float: right; color: #8492a6; font-size: 13px">
              {{ model.size ? formatSize(model.size) : '未知大小' }}
            </span>
          </el-option>
        </el-select>
        <div v-if="selectedModel" class="model-info">
          <span class="model-tag">{{ selectedModel.type || '通用模型' }}</span>
          <el-tooltip :content="selectedModel.description || '无描述信息'" placement="top">
            <i class="el-icon-info"></i>
          </el-tooltip>
        </div>
      </el-form-item>
      
      <el-form-item label="描述" prop="description">
        <el-input
          type="textarea"
          v-model="formData.description"
          :rows="3"
          placeholder="请输入应用描述"
          show-word-limit
          maxlength="200"
        ></el-input>
      </el-form-item>

      <!-- 配置参数 -->
      <h3>配置参数</h3>
      <el-form-item label="最大并发数" prop="config.max_concurrency">
        <el-input-number
          v-model="formData.config.max_concurrency"
          :min="1"
          :max="100"
        ></el-input-number>
        <el-tooltip content="同时处理的最大请求数，建议根据服务器性能和内存调整" placement="top">
          <i class="el-icon-question help-icon"></i>
        </el-tooltip>
        <span v-if="concurrencyRecommendation" class="recommendation-text">
          {{ concurrencyRecommendation }}
        </span>
      </el-form-item>
      
      <el-form-item label="超时时间(秒)" prop="config.timeout">
        <el-input-number
          v-model="formData.config.timeout"
          :min="1"
          :max="300"
        ></el-input-number>
        <el-tooltip content="单个请求的最大处理时间，超过此时间将自动中断" placement="top">
          <i class="el-icon-question help-icon"></i>
        </el-tooltip>
        <span v-if="timeoutRecommendation" class="recommendation-text">
          {{ timeoutRecommendation }}
        </span>
      </el-form-item>
      
      <el-form-item label="日志级别" prop="config.log_level">
        <el-select v-model="formData.config.log_level" placeholder="请选择日志级别">
          <el-option label="DEBUG" value="debug">
            <span>DEBUG</span>
            <span style="float: right; color: #8492a6; font-size: 13px">详细日志，适用于开发调试</span>
          </el-option>
          <el-option label="INFO" value="info">
            <span>INFO</span>
            <span style="float: right; color: #8492a6; font-size: 13px">信息日志，推荐生产环境使用</span>
          </el-option>
          <el-option label="WARNING" value="warning">
            <span>WARNING</span>
            <span style="float: right; color: #8492a6; font-size: 13px">警告日志，只记录警告和错误</span>
          </el-option>
          <el-option label="ERROR" value="error">
            <span>ERROR</span>
            <span style="float: right; color: #8492a6; font-size: 13px">错误日志，只记录错误信息</span>
          </el-option>
        </el-select>
      </el-form-item>

      <!-- 高级配置 -->
      <div class="advanced-settings">
        <el-collapse v-model="activeCollapse">
          <el-collapse-item title="高级配置" name="advanced">
            <el-form-item label="缓存大小(MB)" prop="config.cache_size">
              <el-input-number
                v-model="formData.config.cache_size"
                :min="0"
                :max="1024"
              ></el-input-number>
              <el-tooltip content="模型缓存大小，较大的缓存可提高性能但会占用更多内存" placement="top">
                <i class="el-icon-question help-icon"></i>
              </el-tooltip>
              <span v-if="cacheSizeRecommendation" class="recommendation-text">
                {{ cacheSizeRecommendation }}
              </span>
            </el-form-item>
            
            <el-form-item label="批处理大小" prop="config.batch_size">
              <el-input-number
                v-model="formData.config.batch_size"
                :min="1"
                :max="64"
              ></el-input-number>
              <el-tooltip content="一次处理的批次大小，更大的批次可提高吞吐量但会增加延迟" placement="top">
                <i class="el-icon-question help-icon"></i>
              </el-tooltip>
              <span v-if="batchSizeRecommendation" class="recommendation-text">
                {{ batchSizeRecommendation }}
              </span>
            </el-form-item>
            
            <el-form-item label="使用量化" prop="config.use_quantization">
              <el-switch v-model="formData.config.use_quantization"></el-switch>
              <el-tooltip content="开启量化可减少内存占用，但可能略微降低精度" placement="top">
                <i class="el-icon-question help-icon"></i>
              </el-tooltip>
              <span v-if="quantizationRecommendation" class="recommendation-text">
                {{ quantizationRecommendation }}
              </span>
            </el-form-item>
            
            <el-form-item label="自定义环境变量" class="env-vars-container">
              <div v-for="(env, index) in formData.config.env_vars" :key="index" class="env-var-item">
                <el-input
                  v-model="env.key"
                  placeholder="变量名"
                  class="env-var-key"
                ></el-input>
                <el-input
                  v-model="env.value"
                  placeholder="变量值"
                  class="env-var-value"
                  :type="env.key.toLowerCase().includes('key') || env.key.toLowerCase().includes('token') || env.key.toLowerCase().includes('secret') ? 'password' : 'text'"
                ></el-input>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  size="mini"
                  @click="removeEnvVar(index)"
                ></el-button>
              </div>
              <el-tooltip content="环境变量可用于配置API密钥、访问令牌等敏感信息" placement="left">
                <el-button type="primary" size="small" @click="addEnvVar" icon="el-icon-plus">添加环境变量</el-button>
              </el-tooltip>
            </el-form-item>
          </el-collapse-item>
        </el-collapse>
      </div>

      <!-- 表单按钮 -->
      <div class="form-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '保存' : '创建' }}
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'ApplicationForm',
  props: {
    // 如果是编辑模式，传入现有的应用数据
    applicationData: {
      type: Object,
      default: () => ({})
    },
    // 是否是编辑模式
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      submitting: false,
      activeCollapse: [],
      // 表单数据
      formData: {
        name: '',
        model_id: '',
        description: '',
        config: {
          max_concurrency: 10,
          timeout: 30,
          log_level: 'info',
          cache_size: 256,
          batch_size: 4,
          use_quantization: false,
          env_vars: []
        }
      },
      // 表单验证规则
      rules: {
        name: [
          { required: true, message: '请输入应用名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9\u4e00-\u9fa5_-]+$/, message: '应用名称只能包含字母、数字、中文、下划线和短横线', trigger: 'blur' }
        ],
        model_id: [
          { required: true, message: '请选择模型', trigger: 'change' }
        ],
        description: [
          { max: 200, message: '描述不能超过200个字符', trigger: 'blur' }
        ],
        'config.max_concurrency': [
          { type: 'number', min: 1, message: '并发数不能小于1', trigger: 'blur' }
        ],
        'config.timeout': [
          { type: 'number', min: 1, message: '超时时间不能小于1秒', trigger: 'blur' }
        ],
        'config.cache_size': [
          { type: 'number', min: 0, message: '缓存大小不能为负数', trigger: 'blur' }
        ],
        'config.batch_size': [
          { type: 'number', min: 1, message: '批处理大小不能小于1', trigger: 'blur' }
        ]
      },
      // 推荐设置提示
      concurrencyRecommendation: '',
      timeoutRecommendation: '',
      cacheSizeRecommendation: '',
      batchSizeRecommendation: '',
      quantizationRecommendation: ''
    }
  },
  computed: {
    ...mapState({
      models: state => state.models || []
    }),
    
    // 已完成训练的模型列表
    completedModels() {
      return this.models.filter(model => model.status === 'completed')
    },
    
    // 当前选择的模型
    selectedModel() {
      if (!this.formData.model_id) return null
      return this.models.find(model => model.id === this.formData.model_id)
    }
  },
  methods: {
    ...mapActions(['fetchModels']),
    
    // 格式化文件大小
    formatSize(size) {
      if (!size) return '未知大小'
      
      const units = ['B', 'KB', 'MB', 'GB', 'TB']
      let formattedSize = size
      let unitIndex = 0
      
      while (formattedSize >= 1024 && unitIndex < units.length - 1) {
        formattedSize /= 1024
        unitIndex++
      }
      
      return `${formattedSize.toFixed(2)} ${units[unitIndex]}`
    },
    
    // 处理模型变更，根据模型特性提供配置建议
    handleModelChange(modelId) {
      const selectedModel = this.models.find(model => model.id === modelId)
      if (selectedModel) {
        // 根据模型大小和类型自动调整推荐配置
        this.updateRecommendations(selectedModel)
        
        // 初步自动调整配置参数
        if (selectedModel.size > 10000000000) { // 大于10GB的大模型
          this.formData.config.cache_size = 512
          this.formData.config.batch_size = 2
          this.formData.config.max_concurrency = 5
          this.formData.config.timeout = 60
        } else if (selectedModel.size > 5000000000) { // 大于5GB的中型模型
          this.formData.config.cache_size = 256
          this.formData.config.batch_size = 4
          this.formData.config.max_concurrency = 10
          this.formData.config.timeout = 30
        } else { // 小型模型
          this.formData.config.cache_size = 128
          this.formData.config.batch_size = 8
          this.formData.config.max_concurrency = 20
          this.formData.config.timeout = 15
        }
      }
    },
    
    // 更新配置推荐信息
    updateRecommendations(model) {
      if (!model) {
        this.clearRecommendations()
        return
      }
      
      const size = model.size || 0
      const modelType = model.type || '通用'
      
      // 推荐并发数
      if (size > 10000000000) { // 大于10GB
        this.concurrencyRecommendation = '推荐值: 5-10（大型模型）'
      } else if (size > 5000000000) { // 大于5GB
        this.concurrencyRecommendation = '推荐值: 10-20（中型模型）'
      } else {
        this.concurrencyRecommendation = '推荐值: 20-50（小型模型）'
      }
      
      // 推荐超时时间
      if (modelType.includes('推理') || modelType.includes('生成')) {
        this.timeoutRecommendation = '推荐值: 30-60秒（生成式模型）'
      } else if (modelType.includes('分类') || modelType.includes('检测')) {
        this.timeoutRecommendation = '推荐值: 10-20秒（判别式模型）'
      } else {
        this.timeoutRecommendation = '推荐值: 20-30秒'
      }
      
      // 推荐缓存大小
      if (size > 10000000000) { // 大于10GB
        this.cacheSizeRecommendation = '推荐值: 512-1024MB（大型模型）'
      } else if (size > 5000000000) { // 大于5GB
        this.cacheSizeRecommendation = '推荐值: 256-512MB（中型模型）'
      } else {
        this.cacheSizeRecommendation = '推荐值: 128-256MB（小型模型）'
      }
      
      // 推荐批处理大小
      if (size > 10000000000) { // 大于10GB
        this.batchSizeRecommendation = '推荐值: 2-4（大型模型）'
      } else if (size > 5000000000) { // 大于5GB
        this.batchSizeRecommendation = '推荐值: 4-8（中型模型）'
      } else {
        this.batchSizeRecommendation = '推荐值: 8-16（小型模型）'
      }
      
      // 推荐量化设置
      if (size > 5000000000) { // 大于5GB
        this.quantizationRecommendation = '建议开启量化，可节省50%以上内存'
      } else {
        this.quantizationRecommendation = '小型模型可选择性开启量化'
      }
    },
    
    // 清除推荐信息
    clearRecommendations() {
      this.concurrencyRecommendation = ''
      this.timeoutRecommendation = ''
      this.cacheSizeRecommendation = ''
      this.batchSizeRecommendation = ''
      this.quantizationRecommendation = ''
    },
    
    // 添加环境变量
    addEnvVar() {
      this.formData.config.env_vars.push({ key: '', value: '' })
    },
    
    // 移除环境变量
    removeEnvVar(index) {
      this.formData.config.env_vars.splice(index, 1)
    },
    
    // 处理表单提交
    handleSubmit() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.submitting = true
          
          // 过滤空的环境变量
          const filteredEnvVars = this.formData.config.env_vars.filter(env => env.key.trim() !== '')
          
          // 构建提交数据
          const submitData = {
            ...this.formData,
            config: {
              ...this.formData.config,
              env_vars: filteredEnvVars
            }
          }
          
          // 触发提交事件
          this.$emit('submit', submitData)
        } else {
          // 滚动到第一个错误表单项位置
          setTimeout(() => {
            const firstErrorEl = document.querySelector('.el-form-item__error')
            if (firstErrorEl) {
              firstErrorEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
            }
          }, 100)
        }
      })
    },
    
    // 处理取消
    handleCancel() {
      this.$emit('cancel')
    },
    
    // 重置表单
    resetForm() {
      this.$refs.form.resetFields()
      this.submitting = false
      this.clearRecommendations()
    }
  },
  created() {
    // 获取模型列表
    this.fetchModels()
    
    // 如果是编辑模式，初始化表单数据
    if (this.isEdit && this.applicationData) {
      // 基本信息
      this.formData.name = this.applicationData.name || ''
      this.formData.model_id = this.applicationData.model_id || ''
      this.formData.description = this.applicationData.description || ''
      
      // 配置参数
      if (this.applicationData.config) {
        this.formData.config = {
          ...this.formData.config,
          ...this.applicationData.config
        }
        
        // 处理环境变量
        if (this.applicationData.config.env_vars) {
          if (Array.isArray(this.applicationData.config.env_vars)) {
            this.formData.config.env_vars = [...this.applicationData.config.env_vars]
          } else {
            // 如果是对象格式，转换为数组格式
            this.formData.config.env_vars = Object.entries(this.applicationData.config.env_vars).map(([key, value]) => ({ key, value }))
          }
        }
      }
      
      // 更新配置推荐信息
      if (this.formData.model_id) {
        const selectedModel = this.models.find(model => model.id === this.formData.model_id)
        if (selectedModel) {
          this.updateRecommendations(selectedModel)
        }
      }
    }
  }
}
</script>

<style scoped>
.application-form {
  padding: 20px;
}

.form-container {
  max-width: 800px;
  margin: 0 auto;
}

h3 {
  margin: 20px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
  color: #303133;
}

.advanced-settings {
  margin: 20px 0;
}

.env-vars-container {
  margin-bottom: 0;
}

.env-var-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.env-var-key {
  width: 200px;
  margin-right: 10px;
}

.env-var-value {
  flex: 1;
  margin-right: 10px;
}

.form-actions {
  margin-top: 40px;
  text-align: center;
}

.form-actions button {
  min-width: 120px;
  margin: 0 10px;
}

.help-icon {
  margin-left: 10px;
  color: #909399;
  cursor: pointer;
}

.recommendation-text {
  margin-left: 10px;
  font-size: 12px;
  color: #909399;
}

.model-info {
  margin-top: 5px;
  display: flex;
  align-items: center;
}

.model-tag {
  background-color: #f0f9eb;
  color: #67c23a;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 4px;
  margin-right: 10px;
}

/* 响应式调整 */
@media screen and (max-width: 768px) {
  .env-var-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .env-var-key,
  .env-var-value {
    width: 100%;
    margin-right: 0;
    margin-bottom: 10px;
  }
}
</style> 