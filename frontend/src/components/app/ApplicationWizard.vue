<template>
  <div class="application-wizard">
    <el-card class="wizard-card">
      <div slot="header" class="wizard-header">
        <h2>{{ editMode ? '编辑应用' : '创建应用向导' }}</h2>
        <span class="wizard-steps">步骤 {{ currentStep }}/{{ totalSteps }}</span>
      </div>
      
      <!-- 步骤进度条 -->
      <el-steps :active="currentStep - 1" finish-status="success" align-center>
        <el-step title="基本信息" description="应用名称和模型选择"></el-step>
        <el-step title="配置参数" description="运行参数配置"></el-step>
        <el-step title="插件选择" description="可选功能插件"></el-step>
        <el-step title="确认提交" description="检查并创建"></el-step>
      </el-steps>
      
      <!-- 第一步：基本信息 -->
      <div v-if="currentStep === 1" class="wizard-step-content">
        <el-form ref="basicForm" :model="formData" :rules="basicRules" label-width="120px" label-position="left">
          <el-form-item label="应用名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入应用名称"></el-input>
          </el-form-item>
          
          <el-form-item label="选择模型" prop="model_id">
            <el-select 
              v-model="formData.model_id" 
              filterable 
              placeholder="请选择模型" 
              style="width: 100%"
              @change="handleModelChange"
            >
              <el-option 
                v-for="model in models" 
                :key="model.id" 
                :label="`${model.name} (${model.version})`" 
                :value="model.id"
              >
                <div class="model-option">
                  <span>{{ model.name }} ({{ model.version }})</span>
                  <el-tag size="mini" :type="getModelStatusType(model.status)">
                    {{ getModelStatusText(model.status) }}
                  </el-tag>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="描述" prop="description">
            <el-input 
              v-model="formData.description" 
              type="textarea" 
              :rows="4"
              placeholder="请输入应用描述（可选）"
            ></el-input>
          </el-form-item>
        </el-form>
        
        <div v-if="selectedModel" class="model-info-card">
          <h3>模型信息</h3>
          <div class="model-info-item">
            <span class="label">名称：</span>
            <span>{{ selectedModel.name }}</span>
          </div>
          <div class="model-info-item">
            <span class="label">版本：</span>
            <span>{{ selectedModel.version }}</span>
          </div>
          <div class="model-info-item">
            <span class="label">描述：</span>
            <span>{{ selectedModel.description || '无' }}</span>
          </div>
          <div class="model-info-item">
            <span class="label">参数量：</span>
            <span>{{ getModelSize(selectedModel) }}</span>
          </div>
        </div>
      </div>
      
      <!-- 第二步：配置参数 -->
      <div v-if="currentStep === 2" class="wizard-step-content">
        <div class="config-recommendation" v-if="hasRecommendations">
          <el-alert
            title="系统已根据您选择的模型，自动推荐以下配置参数"
            type="success"
            :closable="false"
            show-icon
          >
            <div slot="description">
              您可以根据需要调整这些参数，系统会自动检查配置是否合理
            </div>
          </el-alert>
        </div>
        
        <el-form ref="configForm" :model="formData.config" :rules="configRules" label-width="140px" label-position="left">
          <el-form-item label="最大并发数" prop="max_concurrency">
            <el-input-number
              v-model="formData.config.max_concurrency"
              :min="1"
              :max="100"
              :step="1"
            ></el-input-number>
            <span class="param-hint">推荐值：{{ getRecommendation('max_concurrency') }}</span>
          </el-form-item>
          
          <el-form-item label="超时时间 (秒)" prop="timeout">
            <el-input-number
              v-model="formData.config.timeout"
              :min="1"
              :max="300"
              :step="1"
            ></el-input-number>
            <span class="param-hint">推荐值：{{ getRecommendation('timeout') }}</span>
          </el-form-item>
          
          <el-form-item label="日志等级" prop="log_level">
            <el-select v-model="formData.config.log_level" style="width: 100%">
              <el-option label="DEBUG" value="debug"></el-option>
              <el-option label="INFO" value="info"></el-option>
              <el-option label="WARNING" value="warning"></el-option>
              <el-option label="ERROR" value="error"></el-option>
            </el-select>
            <span class="param-hint">推荐值：{{ getRecommendation('log_level') }}</span>
          </el-form-item>
          
          <el-form-item label="缓存大小 (MB)" prop="cache_size">
            <el-input-number
              v-model="formData.config.cache_size"
              :min="0"
              :max="10000"
              :step="100"
            ></el-input-number>
            <span class="param-hint">推荐值：{{ getRecommendation('cache_size') }}</span>
          </el-form-item>
          
          <el-form-item label="批处理大小" prop="batch_size">
            <el-input-number
              v-model="formData.config.batch_size"
              :min="1"
              :max="64"
              :step="1"
            ></el-input-number>
            <span class="param-hint">推荐值：{{ getRecommendation('batch_size') }}</span>
          </el-form-item>
          
          <el-form-item label="环境变量" v-if="showAdvancedSettings">
            <div v-for="(envVar, index) in formData.env_vars" :key="index" class="env-var-item">
              <el-input v-model="envVar.key" placeholder="变量名" style="width: 40%; margin-right: 10px;" />
              <el-input v-model="envVar.value" placeholder="变量值" style="width: 40%; margin-right: 10px;" />
              <el-button type="danger" icon="el-icon-delete" circle @click="removeEnvVar(index)"></el-button>
            </div>
            <el-button type="primary" plain @click="addEnvVar">添加环境变量</el-button>
            <div class="tip">
              <i class="el-icon-info"></i>
              环境变量将作为容器启动参数传入，可用于配置应用的运行环境
            </div>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 第三步：插件选择 -->
      <div v-if="currentStep === 3" class="wizard-step-content">
        <el-alert
          v-if="plugins.length === 0"
          title="当前没有可用的插件"
          type="info"
          :closable="false"
          show-icon
        ></el-alert>
        
        <template v-else>
          <div class="plugins-hint">
            <p>选择需要为应用启用的插件，选择的插件将在应用部署时自动加载</p>
          </div>
          
          <el-transfer
            v-model="selectedPluginIds"
            :data="pluginsData"
            :titles="['可用插件', '已选插件']"
            :button-texts="['移除', '添加']"
            :format="{
              noChecked: '${total}',
              hasChecked: '${checked}/${total}'
            }"
          >
            <template slot-scope="{ option }">
              <div class="plugin-transfer-item">
                <span>{{ option.label }}</span>
                <el-tag size="mini" :type="getPluginStatusType(option.status)">
                  {{ getPluginStatusText(option.status) }}
                </el-tag>
              </div>
            </template>
          </el-transfer>
          
          <div class="selected-plugins-info" v-if="selectedPluginIds.length > 0">
            <h3>已选插件信息</h3>
            <el-table :data="selectedPlugins" border size="small">
              <el-table-column prop="name" label="插件名称" width="180"></el-table-column>
              <el-table-column prop="version" label="版本" width="100"></el-table-column>
              <el-table-column prop="description" label="描述"></el-table-column>
            </el-table>
          </div>
        </template>
      </div>
      
      <!-- 第四步：确认提交 -->
      <div v-if="currentStep === 4" class="wizard-step-content">
        <el-alert
          title="请确认以下应用信息，确认无误后点击提交按钮创建应用"
          type="info"
          :closable="false"
          show-icon
        ></el-alert>
        
        <div class="confirmation-section">
          <h3>基本信息</h3>
          <el-descriptions border :column="1">
            <el-descriptions-item label="应用名称">{{ formData.name }}</el-descriptions-item>
            <el-descriptions-item label="模型">{{ getSelectedModelName() }}</el-descriptions-item>
            <el-descriptions-item label="描述">{{ formData.description || '无' }}</el-descriptions-item>
          </el-descriptions>
        </div>
        
        <div class="confirmation-section">
          <h3>配置参数</h3>
          <el-descriptions border :column="2">
            <el-descriptions-item label="最大并发数">{{ formData.config.max_concurrency }}</el-descriptions-item>
            <el-descriptions-item label="超时时间 (秒)">{{ formData.config.timeout }}</el-descriptions-item>
            <el-descriptions-item label="日志等级">{{ formData.config.log_level.toUpperCase() }}</el-descriptions-item>
            <el-descriptions-item label="缓存大小 (MB)">{{ formData.config.cache_size }}</el-descriptions-item>
            <el-descriptions-item label="批处理大小">{{ formData.config.batch_size }}</el-descriptions-item>
          </el-descriptions>
          
          <div v-if="formData.env_vars.length > 0" class="env-vars-confirmation">
            <h4>环境变量</h4>
            <el-table :data="formData.env_vars" border size="small">
              <el-table-column prop="key" label="变量名" width="180"></el-table-column>
              <el-table-column prop="value" label="变量值"></el-table-column>
            </el-table>
          </div>
        </div>
        
        <div class="confirmation-section" v-if="selectedPluginIds.length > 0">
          <h3>已选插件 ({{ selectedPluginIds.length }}个)</h3>
          <el-table :data="selectedPlugins" border size="small">
            <el-table-column prop="name" label="插件名称" width="180"></el-table-column>
            <el-table-column prop="version" label="版本" width="100"></el-table-column>
            <el-table-column prop="description" label="描述"></el-table-column>
          </el-table>
        </div>
      </div>
      
      <!-- 按钮区域 -->
      <div class="wizard-actions">
        <el-button 
          v-if="currentStep > 1" 
          @click="prevStep"
        >上一步</el-button>
        
        <el-button 
          v-if="currentStep < totalSteps" 
          type="primary" 
          @click="nextStep"
        >下一步</el-button>
        
        <el-button 
          v-if="currentStep === totalSteps" 
          type="success" 
          @click="submitForm"
          :loading="submitting"
        >提交</el-button>
        
        <el-button @click="cancel">取消</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import moment from 'moment'

export default {
  name: 'ApplicationWizard',
  props: {
    application: {
      type: Object,
      default: () => null
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      editMode: this.isEdit,
      currentStep: 1,
      totalSteps: 4,
      submitting: false,
      models: [],
      plugins: [],
      availablePlugins: [],
      showAdvancedSettings: false,
      formData: {
        name: '',
        model_id: '',
        description: '',
        config: {
          max_concurrency: 5,
          timeout: 60,
          log_level: 'INFO',
          cache_size: 1000,
          batch_size: 4
        },
        env_vars: [],
      },
      selectedPluginIds: [],
      recommendations: {
        small: {
          max_concurrency: 10,
          timeout: 30,
          log_level: 'info',
          cache_size: 1000,
          batch_size: 8
        },
        medium: {
          max_concurrency: 5,
          timeout: 60,
          log_level: 'info',
          cache_size: 2000,
          batch_size: 4
        },
        large: {
          max_concurrency: 2,
          timeout: 120,
          log_level: 'info',
          cache_size: 4000,
          batch_size: 1
        }
      },
      basicRules: {
        name: [
          { required: true, message: '请输入应用名称', trigger: 'blur' },
          { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
        ],
        model_id: [
          { required: true, message: '请选择模型', trigger: 'change' }
        ]
      },
      configRules: {
        max_concurrency: [
          { required: true, message: '请输入最大并发数', trigger: 'blur' },
          { type: 'number', message: '必须为数字值', trigger: 'blur' }
        ],
        timeout: [
          { required: true, message: '请输入超时时间', trigger: 'blur' },
          { type: 'number', message: '必须为数字值', trigger: 'blur' }
        ],
        log_level: [
          { required: true, message: '请选择日志等级', trigger: 'change' }
        ],
        cache_size: [
          { required: true, message: '请输入缓存大小', trigger: 'blur' },
          { type: 'number', message: '必须为数字值', trigger: 'blur' }
        ],
        batch_size: [
          { required: true, message: '请输入批处理大小', trigger: 'blur' },
          { type: 'number', message: '必须为数字值', trigger: 'blur' }
        ]
      }
    };
  },
  computed: {
    ...mapState({
      modelList: state => state.training.models || [],
      pluginsList: state => state.app.plugins || []
    }),
    selectedModel() {
      if (!this.formData.model_id) return null
      return this.models.find(model => model.id === this.formData.model_id)
    },
    modelSize() {
      if (!this.selectedModel) return 'medium';
      
      // 根据模型参数量判断大小
      const paramCount = this.getModelParamCount(this.selectedModel);
      if (paramCount < 3) return 'small';
      if (paramCount < 13) return 'medium';
      return 'large';
    },
    hasRecommendations() {
      return !!this.selectedModel;
    },
    pluginsData() {
      return this.plugins.map(plugin => ({
        key: plugin.id,
        label: `${plugin.name} (${plugin.version})`,
        status: plugin.status,
        disabled: plugin.status !== 'active'
      }));
    },
    selectedPlugins() {
      return this.plugins.filter(plugin => this.selectedPluginIds.includes(plugin.id));
    },
    steps() {
      return [
        { title: '基本信息', description: '设置应用名称和选择模型' },
        { title: '配置参数', description: '设置应用的运行参数' },
        { title: '插件选择', description: '选择需要的插件' },
        { title: '确认提交', description: '确认信息并创建应用' }
      ]
    },
    modelSizeRecommendation() {
      if (!this.selectedModel) return null
      
      const paramCount = this.getModelParamCount(this.selectedModel)
      if (paramCount >= 70000000000) {
        return {
          size: '超大型',
          max_concurrency: 1,
          timeout: 300,
          cache_size: 2000,
          batch_size: 1
        }
      } else if (paramCount >= 30000000000) {
        return {
          size: '大型',
          max_concurrency: 2,
          timeout: 180,
          cache_size: 1500,
          batch_size: 2
        }
      } else if (paramCount >= 7000000000) {
        return {
          size: '中型',
          max_concurrency: 4,
          timeout: 120,
          cache_size: 1000,
          batch_size: 4
        }
      } else {
        return {
          size: '小型',
          max_concurrency: 8,
          timeout: 60,
          cache_size: 500,
          batch_size: 8
        }
      }
    }
  },
  created() {
    this.init();
  },
  watch: {
    isEdit: {
      handler(newVal) {
        this.editMode = newVal
      },
      immediate: true
    }
  },
  methods: {
    ...mapActions({
      fetchModels: 'training/fetchModels',
      fetchPlugins: 'app/fetchPlugins',
      createApplication: 'app/createApplication',
      updateApplication: 'app/updateApplication'
    }),
    async init() {
      this.loading = true;
      try {
        await this.fetchModels();
        await this.fetchPlugins();
        
        // 从store获取数据
        this.models = this.modelList;
        this.plugins = this.pluginsList;
        
        if (this.isEdit && this.application) {
          this.initFormData();
        }
      } catch (error) {
        console.error('Failed to initialize wizard:', error);
        this.$message.error('初始化数据失败: ' + (error.message || '未知错误'));
      } finally {
        this.loading = false;
      }
    },
    initFormData() {
      if (!this.application) return;
      
      // 基本信息
      this.formData.name = this.application.name;
      this.formData.model_id = this.application.model_id;
      this.formData.description = this.application.description || '';
      
      // 配置
      if (this.application.config) {
        this.formData.config = {
          max_concurrency: this.application.config.max_concurrency || 5,
          timeout: this.application.config.timeout || 60,
          log_level: this.application.config.log_level || 'INFO',
          cache_size: this.application.config.cache_size || 1000,
          batch_size: this.application.config.batch_size || 4
        };
      }
      
      // 环境变量
      this.formData.env_vars = [];
      if (this.application.env_vars) {
        Object.keys(this.application.env_vars).forEach(key => {
          this.formData.env_vars.push({
            key,
            value: this.application.env_vars[key]
          });
        });
      }
      
      // 插件
      if (this.application.plugins && Array.isArray(this.application.plugins)) {
        this.selectedPluginIds = this.application.plugins.map(plugin => 
          typeof plugin === 'object' ? plugin.id : plugin
        );
      }
    },
    
    getModelSize(model) {
      const paramCount = this.getModelParamCount(model);
      if (paramCount < 1) return '未知';
      return `${paramCount}B 参数`;
    },
    
    getModelParamCount(model) {
      // 从模型名称或描述中提取参数量信息
      const paramRegex = /(\d+)[Bb]|(\d+(\.\d+)?)[Bb]/;
      
      if (model.description) {
        const match = model.description.match(paramRegex);
        if (match) {
          return parseFloat(match[1] || match[2]);
        }
      }
      
      if (model.name) {
        const match = model.name.match(paramRegex);
        if (match) {
          return parseFloat(match[1] || match[2]);
        }
      }
      
      // 默认返回中等大小
      return 7;
    },
    
    getModelStatusType(status) {
      const statusMap = {
        'active': 'success',
        'inactive': 'info',
        'error': 'danger'
      };
      return statusMap[status] || 'info';
    },
    
    getModelStatusText(status) {
      const statusMap = {
        'active': '可用',
        'inactive': '未激活',
        'error': '错误'
      };
      return statusMap[status] || status;
    },
    
    getPluginStatusType(status) {
      const statusMap = {
        'active': 'success',
        'inactive': 'info',
        'error': 'danger'
      };
      return statusMap[status] || 'info';
    },
    
    getPluginStatusText(status) {
      const statusMap = {
        'active': '可用',
        'inactive': '未激活',
        'error': '错误'
      };
      return statusMap[status] || status;
    },
    
    handleModelChange() {
      if (this.selectedModel) {
        // 根据模型大小自动设置推荐配置
        const recommendedConfig = this.modelSizeRecommendation;
        
        this.formData.config = {
          ...this.formData.config,
          ...recommendedConfig
        };
      }
    },
    
    addEnvVar() {
      this.formData.env_vars.push({
        key: '',
        value: ''
      });
    },
    
    removeEnvVar(index) {
      this.formData.env_vars.splice(index, 1);
    },
    
    getRecommendation(field) {
      if (!this.selectedModel) return '-';
      return this.modelSizeRecommendation[field];
    },
    
    getSelectedModelName() {
      if (!this.selectedModel) return '未选择';
      return `${this.selectedModel.name} (${this.selectedModel.version})`;
    },
    
    async nextStep() {
      if (this.currentStep === 1) {
        // 验证基本信息表单
        try {
          await this.$refs.basicForm.validate();
          this.currentStep++;
        } catch (error) {
          // 表单验证失败
          return;
        }
      } else if (this.currentStep === 2) {
        // 验证配置参数表单
        try {
          await this.$refs.configForm.validate();
          this.currentStep++;
        } catch (error) {
          // 表单验证失败
          return;
        }
      } else {
        this.currentStep++;
      }
    },
    
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },
    
    async submitForm() {
      try {
        this.submitting = true;
        
        // 准备提交数据
        const applicationData = {
          name: this.formData.name,
          model_id: this.formData.model_id,
          description: this.formData.description,
          config: this.formData.config,
          plugins: this.selectedPluginIds
        };
        
        // 处理环境变量
        const envVars = {};
        this.formData.env_vars.forEach(env => {
          if (env.key && env.value) {
            envVars[env.key] = env.value;
          }
        });
        applicationData.env_vars = envVars;
        
        // 创建或更新应用
        if (this.isEdit && this.application) {
          await this.updateApplication({
            id: this.application.id,
            data: applicationData
          });
          this.$message.success('应用更新成功');
        } else {
          await this.createApplication(applicationData);
          this.$message.success('应用创建成功');
        }
        
        this.$emit('complete');
      } catch (error) {
        console.error('Failed to submit application:', error);
        this.$message.error(`提交失败: ${error.message || '未知错误'}`);
      } finally {
        this.submitting = false;
      }
    },
    
    cancel() {
      this.$emit('cancel');
    }
  }
};
</script>

<style scoped>
.application-wizard {
  max-width: 1000px;
  margin: 0 auto;
}

.wizard-card {
  margin-bottom: 20px;
}

.wizard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.wizard-steps {
  font-size: 14px;
  color: #606266;
}

.wizard-step-content {
  margin: 20px 0;
  min-height: 300px;
}

.wizard-actions {
  margin-top: 20px;
  text-align: right;
}

.model-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.model-info-card {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #EBEEF5;
  border-radius: 4px;
  background-color: #F5F7FA;
}

.model-info-item {
  margin-bottom: 10px;
}

.model-info-item .label {
  font-weight: bold;
  margin-right: 10px;
}

.config-recommendation {
  margin-bottom: 20px;
}

.param-hint {
  margin-left: 10px;
  color: #909399;
  font-size: 12px;
}

.env-vars-container {
  width: 100%;
}

.env-var-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.env-var-key {
  width: 30%;
  margin-right: 10px;
}

.env-var-value {
  width: 60%;
  margin-right: 10px;
}

.plugin-transfer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-right: 10px;
}

.selected-plugins-info {
  margin-top: 20px;
}

.plugins-hint {
  margin-bottom: 20px;
}

.confirmation-section {
  margin-bottom: 30px;
}

.env-vars-confirmation {
  margin-top: 15px;
}
</style> 