<template>
  <div class="evaluation-task-form">
    <el-form
      ref="form"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="form-container"
    >
      <!-- 基本信息 -->
      <h3>基本信息</h3>
      <el-form-item label="任务名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入任务名称"></el-input>
      </el-form-item>
      
      <el-form-item label="评测模型" prop="model_id">
        <el-select
          v-model="formData.model_id"
          placeholder="请选择模型"
          style="width: 100%"
          @change="handleModelChange"
        >
          <el-option
            v-for="model in completedModels"
            :key="model.id"
            :label="`${model.name} (${model.version})`"
            :value="model.id"
          ></el-option>
        </el-select>
      </el-form-item>
      
      <el-form-item label="评测数据集" prop="dataset_id">
        <el-select
          v-model="formData.dataset_id"
          placeholder="请选择数据集"
          style="width: 100%"
        >
          <el-option
            v-for="dataset in datasets"
            :key="dataset.id"
            :label="dataset.name"
            :value="dataset.id"
          ></el-option>
        </el-select>
      </el-form-item>
      
      <el-form-item label="描述" prop="description">
        <el-input
          type="textarea"
          v-model="formData.description"
          :rows="3"
          placeholder="请输入任务描述"
        ></el-input>
      </el-form-item>

      <!-- 评测参数 -->
      <h3>评测参数</h3>
      <el-form-item label="批次大小" prop="parameters.batch_size">
        <el-input-number
          v-model="formData.parameters.batch_size"
          :min="1"
          :max="128"
        ></el-input-number>
      </el-form-item>
      
      <el-form-item label="最大样本数" prop="parameters.max_samples">
        <el-input-number
          v-model="formData.parameters.max_samples"
          :min="1"
          :max="10000"
        ></el-input-number>
      </el-form-item>
      
      <el-form-item label="评估指标" prop="parameters.metrics">
        <el-select
          v-model="formData.parameters.metrics"
          multiple
          placeholder="请选择评估指标"
          style="width: 100%"
        >
          <el-option label="准确率 (Accuracy)" value="accuracy"></el-option>
          <el-option label="精确率 (Precision)" value="precision"></el-option>
          <el-option label="召回率 (Recall)" value="recall"></el-option>
          <el-option label="F1分数 (F1 Score)" value="f1_score"></el-option>
          <el-option label="BLEU分数 (BLEU Score)" value="bleu_score"></el-option>
          <el-option label="ROUGE分数 (ROUGE Score)" value="rouge_score"></el-option>
        </el-select>
      </el-form-item>

      <!-- 高级参数 -->
      <div class="advanced-settings">
        <el-collapse v-model="activeCollapse">
          <el-collapse-item title="高级参数" name="advanced">
            <el-form-item label="阈值" prop="parameters.threshold">
              <el-input-number
                v-model="formData.parameters.threshold"
                :precision="2"
                :step="0.01"
                :min="0"
                :max="1"
              ></el-input-number>
            </el-form-item>
            
            <el-form-item label="温度" prop="parameters.temperature">
              <el-input-number
                v-model="formData.parameters.temperature"
                :precision="2"
                :step="0.01"
                :min="0.01"
                :max="2"
              ></el-input-number>
            </el-form-item>
            
            <el-form-item label="Top K" prop="parameters.top_k">
              <el-input-number
                v-model="formData.parameters.top_k"
                :min="0"
                :max="100"
              ></el-input-number>
            </el-form-item>
            
            <el-form-item label="Top P" prop="parameters.top_p">
              <el-input-number
                v-model="formData.parameters.top_p"
                :precision="2"
                :step="0.01"
                :min="0"
                :max="1"
              ></el-input-number>
            </el-form-item>
            
            <el-form-item label="自定义参数">
              <div v-for="(param, index) in customParams" :key="index" class="custom-param-item">
                <el-row :gutter="10">
                  <el-col :span="8">
                    <el-input v-model="param.key" placeholder="参数名"></el-input>
                  </el-col>
                  <el-col :span="14">
                    <el-input v-model="param.value" placeholder="参数值"></el-input>
                  </el-col>
                  <el-col :span="2">
                    <el-button
                      type="danger"
                      icon="el-icon-delete"
                      circle
                      size="mini"
                      @click="removeCustomParam(index)"
                    ></el-button>
                  </el-col>
                </el-row>
              </div>
              <el-button type="primary" size="small" @click="addCustomParam">添加自定义参数</el-button>
            </el-form-item>
          </el-collapse-item>
        </el-collapse>
      </div>

      <!-- 表单按钮 -->
      <div class="form-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">创建</el-button>
      </div>
    </el-form>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'EvaluationTaskForm',
  data() {
    return {
      submitting: false,
      activeCollapse: [],
      customParams: [],
      // 表单数据
      formData: {
        name: '',
        model_id: '',
        dataset_id: '',
        description: '',
        parameters: {
          batch_size: 32,
          max_samples: 1000,
          metrics: ['accuracy', 'f1_score'],
          threshold: 0.5,
          temperature: 1.0,
          top_k: 50,
          top_p: 0.9
        }
      },
      // 表单验证规则
      rules: {
        name: [
          { required: true, message: '请输入任务名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        model_id: [
          { required: true, message: '请选择评测模型', trigger: 'change' }
        ],
        dataset_id: [
          { required: true, message: '请选择评测数据集', trigger: 'change' }
        ],
        description: [
          { max: 200, message: '描述不能超过200个字符', trigger: 'blur' }
        ],
        'parameters.metrics': [
          { required: true, type: 'array', message: '请至少选择一个评估指标', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    ...mapState({
      models: state => state.models || [],
      datasets: state => state.datasets || []
    }),
    
    // 已完成训练的模型列表
    completedModels() {
      return this.models.filter(model => model.status === 'completed')
    }
  },
  methods: {
    ...mapActions(['fetchModels', 'fetchDatasets']),
    
    // 处理模型变更
    handleModelChange(modelId) {
      // 可以在这里根据选择的模型自动设置一些参数
      const selectedModel = this.models.find(model => model.id === modelId)
      if (selectedModel) {
        // 例如，根据模型类型调整评估指标
        if (selectedModel.type === 'text-generation') {
          this.formData.parameters.metrics = ['bleu_score', 'rouge_score']
        } else if (selectedModel.type === 'classification') {
          this.formData.parameters.metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        }
      }
    },
    
    // 添加自定义参数
    addCustomParam() {
      this.customParams.push({ key: '', value: '' })
    },
    
    // 移除自定义参数
    removeCustomParam(index) {
      this.customParams.splice(index, 1)
    },
    
    // 处理表单提交
    handleSubmit() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.submitting = true
          
          // 处理自定义参数
          const parameters = { ...this.formData.parameters }
          this.customParams.forEach(param => {
            if (param.key && param.value) {
              parameters[param.key] = param.value
            }
          })
          
          // 构建提交数据
          const submitData = {
            ...this.formData,
            parameters
          }
          
          // 触发提交事件
          this.$emit('submit', submitData)
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
      this.customParams = []
      this.submitting = false
    }
  },
  created() {
    // 获取模型和数据集列表
    this.fetchModels()
    this.fetchDatasets()
  }
}
</script>

<style scoped>
.evaluation-task-form {
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

.custom-param-item {
  margin-bottom: 10px;
}

.form-actions {
  margin-top: 40px;
  text-align: center;
}

.form-actions button {
  min-width: 120px;
  margin: 0 10px;
}
</style> 