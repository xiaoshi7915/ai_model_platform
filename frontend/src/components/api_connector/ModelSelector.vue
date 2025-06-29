<template>
  <div class="model-selector">
    <!-- 提供商选择 -->
    <div class="selector-row">
      <label class="selector-label">AI提供商</label>
      <el-select 
        v-model="selectedProvider" 
        placeholder="选择API提供商" 
        @change="handleProviderChange"
        :loading="loadingProviders"
        filterable
        class="selector-input"
      >
        <el-option
          v-for="provider in activeProviders"
          :key="provider.id"
          :label="provider.name"
          :value="provider.id">
          <span style="float: left">{{ provider.name }}</span>
          <span style="float: right; color: #8492a6; font-size: 13px">{{ provider.code }}</span>
        </el-option>
      </el-select>
    </div>
    
    <!-- 模型选择 -->
    <div class="selector-row">
      <label class="selector-label">模型</label>
      <el-select 
        v-model="selectedModel" 
        placeholder="选择模型" 
        @change="handleModelChange"
        :loading="loadingModels"
        filterable
        :disabled="!selectedProvider || providerModels.length === 0"
        class="selector-input"
      >
        <el-option-group
          v-for="group in modelGroups"
          :key="group.type"
          :label="getModelTypeText(group.type)">
          <el-option
            v-for="model in group.models"
            :key="model.id"
            :label="model.name"
            :value="model.id">
            <div class="model-option">
              <div>
                <span class="model-name">{{ model.name }}</span>
                <el-tag size="mini" :type="getModelTypeTag(model.type)" class="model-type-tag">
                  {{ getModelTypeText(model.type) }}
                </el-tag>
              </div>
              <div class="model-details">
                <span v-if="model.token_limit" class="model-token-limit">
                  <i class="el-icon-coin"></i> {{ model.token_limit }}
                </span>
                <span v-if="model.pricing" class="model-pricing">
                  <i class="el-icon-price-tag"></i> 
                  ${{ model.pricing.input || 0 }} / ${{ model.pricing.output || 0 }}
                </span>
              </div>
            </div>
          </el-option>
        </el-option-group>
      </el-select>
    </div>
    
    <!-- 高级选项按钮 -->
    <div v-if="showAdvancedOptions && selectedModel" class="advanced-toggle">
      <el-button 
        type="text" 
        size="small" 
        @click="advancedOptionsVisible = !advancedOptionsVisible">
        {{ advancedOptionsVisible ? '隐藏高级选项' : '显示高级选项' }}
        <i :class="advancedOptionsVisible ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
      </el-button>
    </div>
    
    <!-- 高级选项面板 -->
    <div v-if="showAdvancedOptions && advancedOptionsVisible && selectedModel" class="advanced-options">
      <el-divider content-position="left">高级选项</el-divider>
      
      <!-- 通用模型参数 -->
      <div class="parameter-section">
        <div class="parameter-row">
          <label class="parameter-label">Temperature</label>
          <el-tooltip content="控制输出的随机性，较高的值会使输出更加随机和创意，较低的值会使输出更加确定和集中" placement="top">
            <el-slider 
              v-model="modelParams.temperature" 
              :min="0" 
              :max="2" 
              :step="0.1"
              :format-tooltip="value => value.toFixed(1)"
              show-input
              class="parameter-slider"
            ></el-slider>
          </el-tooltip>
        </div>
        
        <div class="parameter-row">
          <label class="parameter-label">最大输出Tokens</label>
          <el-tooltip :content="`控制模型生成的最大token数量 (0-${currentModel?.token_limit || 4096})`" placement="top">
            <el-input-number 
              v-model="modelParams.max_tokens" 
              :min="0" 
              :max="currentModel?.token_limit || 4096"
              class="parameter-input"
            ></el-input-number>
          </el-tooltip>
        </div>

        <div class="parameter-row">
          <label class="parameter-label">Top P</label>
          <el-tooltip content="核采样，控制模型考虑的概率质量，较低的值会使输出更加确定" placement="top">
            <el-slider 
              v-model="modelParams.top_p" 
              :min="0" 
              :max="1" 
              :step="0.05"
              :format-tooltip="value => value.toFixed(2)"
              show-input
              class="parameter-slider"
            ></el-slider>
          </el-tooltip>
        </div>
        
        <div class="parameter-row">
          <label class="parameter-label">Presence Penalty</label>
          <el-tooltip content="抑制重复出现的主题和内容" placement="top">
            <el-slider 
              v-model="modelParams.presence_penalty" 
              :min="-2" 
              :max="2" 
              :step="0.1"
              :format-tooltip="value => value.toFixed(1)"
              show-input
              class="parameter-slider"
            ></el-slider>
          </el-tooltip>
        </div>
        
        <div class="parameter-row">
          <label class="parameter-label">Frequency Penalty</label>
          <el-tooltip content="抑制重复使用的词汇和短语" placement="top">
            <el-slider 
              v-model="modelParams.frequency_penalty" 
              :min="-2" 
              :max="2" 
              :step="0.1"
              :format-tooltip="value => value.toFixed(1)"
              show-input
              class="parameter-slider"
            ></el-slider>
          </el-tooltip>
        </div>
      </div>
      
      <!-- 提供商特定参数 -->
      <div v-if="selectedProviderCode === 'anthropic'" class="parameter-section">
        <div class="parameter-row">
          <label class="parameter-label">Top K</label>
          <el-tooltip content="限制模型只考虑概率最高的K个令牌" placement="top">
            <el-input-number 
              v-model="modelParams.top_k" 
              :min="0" 
              :max="100"
              class="parameter-input"
            ></el-input-number>
          </el-tooltip>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ModelSelector',
  props: {
    // 是否显示高级选项
    showAdvancedOptions: {
      type: Boolean,
      default: true
    },
    // 预设选择的提供商ID
    presetProviderId: {
      type: [Number, String],
      default: null
    },
    // 预设选择的模型ID
    presetModelId: {
      type: [Number, String],
      default: null
    },
    // 模型类型过滤
    modelTypeFilter: {
      type: [String, Array],
      default: null
    }
  },
  data() {
    return {
      // 提供商相关
      providers: [],
      selectedProvider: null,
      loadingProviders: false,
      selectedProviderCode: '',
      
      // 模型相关
      providerModels: [],
      selectedModel: null,
      loadingModels: false,
      currentModel: null,
      
      // 高级选项
      advancedOptionsVisible: false,
      modelParams: {
        temperature: 0.7,
        max_tokens: 1024,
        top_p: 1,
        presence_penalty: 0,
        frequency_penalty: 0,
        top_k: 40
      }
    }
  },
  computed: {
    // 只返回激活状态的提供商
    activeProviders() {
      return this.providers.filter(provider => provider.is_active)
    },
    
    // 按模型类型分组
    modelGroups() {
      const groups = {}
      
      // 根据类型筛选模型
      let filteredModels = this.providerModels
      if (this.modelTypeFilter) {
        const filterTypes = Array.isArray(this.modelTypeFilter) 
          ? this.modelTypeFilter 
          : [this.modelTypeFilter]
        
        filteredModels = this.providerModels.filter(model => 
          filterTypes.includes(model.type)
        )
      }
      
      // 按类型分组
      filteredModels.forEach(model => {
        if (!groups[model.type]) {
          groups[model.type] = {
            type: model.type,
            models: []
          }
        }
        groups[model.type].models.push(model)
      })
      
      // 转换为数组并排序
      return Object.values(groups).sort((a, b) => {
        // 优先显示chat类型模型
        if (a.type === 'chat') return -1
        if (b.type === 'chat') return 1
        return 0
      })
    }
  },
  created() {
    this.loadProviders()
    
    // 如果有预设值，设置初始选择
    if (this.presetProviderId) {
      this.selectedProvider = this.presetProviderId
      this.loadProviderModels()
    }
  },
  methods: {
    // 加载所有提供商
    async loadProviders() {
      this.loadingProviders = true
      try {
        const response = await axios.get('/api/api-connector/providers/')
        this.providers = response.data
        
        // 如果有预设提供商，选择它
        if (this.presetProviderId) {
          this.selectedProvider = this.presetProviderId
          this.loadProviderModels()
        } 
        // 否则尝试自动选择第一个活跃的提供商
        else if (this.activeProviders.length > 0 && !this.selectedProvider) {
          this.selectedProvider = this.activeProviders[0].id
          this.loadProviderModels()
        }
      } catch (error) {
        console.error('加载提供商列表失败:', error)
        this.$message.error('加载提供商列表失败')
      } finally {
        this.loadingProviders = false
      }
    },
    
    // 提供商改变时加载相应的模型
    handleProviderChange(providerId) {
      this.selectedModel = null
      this.currentModel = null
      this.loadProviderModels()
      
      // 获取当前提供商代码
      const provider = this.providers.find(p => p.id === providerId)
      if (provider) {
        this.selectedProviderCode = provider.code
      }
      
      this.$emit('provider-change', provider)
    },
    
    // 加载提供商支持的模型
    async loadProviderModels() {
      if (!this.selectedProvider) return
      
      this.loadingModels = true
      try {
        const response = await axios.get(`/api/api-connector/providers/${this.selectedProvider}/models/`)
        this.providerModels = response.data
        
        // 如果有预设模型，选择它
        if (this.presetModelId) {
          this.selectedModel = this.presetModelId
          this.updateCurrentModel()
        } 
        // 否则自动选择第一个合适类型的模型
        else if (this.providerModels.length > 0) {
          // 如果有过滤器，尝试选择符合条件的第一个模型
          if (this.modelTypeFilter) {
            const filterTypes = Array.isArray(this.modelTypeFilter) 
              ? this.modelTypeFilter 
              : [this.modelTypeFilter]
            
            const filteredModel = this.providerModels.find(model => 
              filterTypes.includes(model.type)
            )
            
            if (filteredModel) {
              this.selectedModel = filteredModel.id
              this.updateCurrentModel()
              return
            }
          }
          
          // 优先选择chat类型的模型
          const chatModel = this.providerModels.find(model => model.type === 'chat')
          if (chatModel) {
            this.selectedModel = chatModel.id
          } else {
            this.selectedModel = this.providerModels[0].id
          }
          this.updateCurrentModel()
        }
      } catch (error) {
        console.error('加载模型列表失败:', error)
        this.$message.error('加载模型列表失败')
      } finally {
        this.loadingModels = false
      }
    },
    
    // 模型改变时更新模型相关信息
    handleModelChange(modelId) {
      this.updateCurrentModel()
      this.$emit('model-change', this.currentModel)
    },
    
    // 更新当前模型对象
    updateCurrentModel() {
      if (!this.selectedModel) {
        this.currentModel = null
        return
      }
      
      this.currentModel = this.providerModels.find(model => model.id === this.selectedModel)
      
      // 调整最大token上限
      if (this.currentModel && this.currentModel.token_limit) {
        // 将最大输出token默认设为模型上限的一半
        this.modelParams.max_tokens = Math.min(
          Math.floor(this.currentModel.token_limit / 2),
          this.modelParams.max_tokens
        )
      }
    },
    
    // 获取模型类型标签颜色
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
    
    // 获取模型类型文本
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
    
    // 获取选择结果
    getSelectionResult() {
      return {
        provider: this.providers.find(p => p.id === this.selectedProvider),
        model: this.currentModel,
        parameters: { ...this.modelParams }
      }
    },
    
    // 重置选择
    reset() {
      this.selectedProvider = null
      this.selectedModel = null
      this.currentModel = null
      this.modelParams = {
        temperature: 0.7,
        max_tokens: 1024,
        top_p: 1,
        presence_penalty: 0,
        frequency_penalty: 0,
        top_k: 40
      }
    },
    
    // 设置参数值
    setParameters(params) {
      if (!params) return
      
      this.modelParams = {
        ...this.modelParams,
        ...params
      }
    }
  }
}
</script>

<style scoped>
.model-selector {
  width: 100%;
  margin-bottom: 15px;
}

.selector-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.selector-label {
  width: 80px;
  text-align: right;
  margin-right: 10px;
  font-weight: 500;
  color: #606266;
}

.selector-input {
  flex: 1;
}

.model-option {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.model-name {
  font-weight: 500;
}

.model-type-tag {
  margin-left: 8px;
}

.model-details {
  font-size: 12px;
  color: #909399;
  display: flex;
  gap: 15px;
}

.model-token-limit, .model-pricing {
  display: flex;
  align-items: center;
  gap: 4px;
}

.advanced-toggle {
  display: flex;
  justify-content: flex-end;
  margin-top: 5px;
}

.advanced-options {
  margin-top: 5px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.parameter-section {
  margin-bottom: 15px;
}

.parameter-row {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.parameter-label {
  width: 140px;
  text-align: right;
  margin-right: 10px;
  font-weight: 500;
  color: #606266;
}

.parameter-slider {
  flex: 1;
}

.parameter-input {
  width: 120px;
}
</style> 