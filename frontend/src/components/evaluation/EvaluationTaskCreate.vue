<template>
  <div class="evaluation-task-create">
    <el-card>
      <div slot="header" class="card-header">
        <span>创建评测任务</span>
      </div>
      
      <el-form 
        ref="taskForm" 
        :model="taskForm" 
        :rules="rules" 
        label-width="120px"
        label-position="right"
      >
        <!-- 基本信息 -->
        <h3 class="form-section-title">基本信息</h3>
        
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="请输入评测任务名称"></el-input>
        </el-form-item>
        
        <el-form-item label="任务描述" prop="description">
          <el-input 
            v-model="taskForm.description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入评测任务描述（可选）"
          ></el-input>
        </el-form-item>
        
        <!-- 模型选择 -->
        <h3 class="form-section-title">模型选择</h3>
        
        <el-form-item label="评测模型" prop="model_id">
          <el-select 
            v-model="taskForm.model_id" 
            placeholder="请选择评测模型"
            filterable
            @change="handleModelChange"
          >
            <el-option
              v-for="model in modelOptions"
              :key="model.id"
              :label="model.name + ' (' + model.version + ')'"
              :value="model.id"
            ></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="模型信息" v-if="selectedModel">
          <el-descriptions :column="1" border size="small">
            <el-descriptions-item label="模型名称">{{ selectedModel.name }}</el-descriptions-item>
            <el-descriptions-item label="模型版本">{{ selectedModel.version }}</el-descriptions-item>
            <el-descriptions-item label="模型类型">{{ selectedModel.type }}</el-descriptions-item>
          </el-descriptions>
        </el-form-item>
        
        <!-- 数据集选择 -->
        <h3 class="form-section-title">数据集选择</h3>
        
        <el-form-item label="评测数据集" prop="dataset_id">
          <el-select 
            v-model="taskForm.dataset_id" 
            placeholder="请选择评测数据集"
            filterable
            @change="handleDatasetChange"
          >
            <el-option
              v-for="dataset in datasetOptions"
              :key="dataset.id"
              :label="dataset.name"
              :value="dataset.id"
            ></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="数据集信息" v-if="selectedDataset">
          <el-descriptions :column="1" border size="small">
            <el-descriptions-item label="数据集名称">{{ selectedDataset.name }}</el-descriptions-item>
            <el-descriptions-item label="数据集大小">{{ selectedDataset.size || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="数据集类型">{{ selectedDataset.type }}</el-descriptions-item>
          </el-descriptions>
        </el-form-item>
        
        <!-- 评测配置 -->
        <h3 class="form-section-title">评测配置</h3>
        
        <el-form-item label="评测指标" prop="metrics">
          <el-checkbox-group v-model="taskForm.metrics">
            <el-checkbox 
              v-for="metric in availableMetrics" 
              :key="metric.value" 
              :label="metric.value"
            >
              {{ metric.label }}
              <el-tooltip :content="metric.description" placement="top">
                <i class="el-icon-question"></i>
              </el-tooltip>
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        
        <el-form-item label="高级参数">
          <el-collapse>
            <el-collapse-item title="高级参数配置" name="1">
              <el-form-item label="温度" prop="parameters.temperature">
                <el-slider 
                  v-model="taskForm.parameters.temperature" 
                  :min="0" 
                  :max="1" 
                  :step="0.01"
                  show-input
                ></el-slider>
              </el-form-item>
              
              <el-form-item label="最大长度" prop="parameters.max_length">
                <el-input-number 
                  v-model="taskForm.parameters.max_length" 
                  :min="1" 
                  :max="4096"
                ></el-input-number>
              </el-form-item>
              
              <el-form-item label="批处理大小" prop="parameters.batch_size">
                <el-input-number 
                  v-model="taskForm.parameters.batch_size" 
                  :min="1" 
                  :max="64"
                ></el-input-number>
              </el-form-item>
            </el-collapse-item>
          </el-collapse>
        </el-form-item>
        
        <!-- 提交按钮 -->
        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitting">创建评测任务</el-button>
          <el-button @click="resetForm">重置</el-button>
          <el-button @click="handleCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'EvaluationTaskCreate',
  data() {
    return {
      submitting: false,
      taskForm: {
        name: '',
        description: '',
        model_id: '',
        dataset_id: '',
        metrics: [],
        parameters: {
          temperature: 0.7,
          max_length: 1024,
          batch_size: 16
        }
      },
      rules: {
        name: [
          { required: true, message: '请输入评测任务名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        model_id: [
          { required: true, message: '请选择评测模型', trigger: 'change' }
        ],
        dataset_id: [
          { required: true, message: '请选择评测数据集', trigger: 'change' }
        ],
        metrics: [
          { type: 'array', required: true, message: '请至少选择一个评测指标', trigger: 'change' }
        ]
      },
      modelOptions: [],
      datasetOptions: [],
      selectedModel: null,
      selectedDataset: null,
      availableMetrics: [
        { value: 'accuracy', label: '准确率', description: '模型预测正确的比例' },
        { value: 'precision', label: '精确率', description: '模型预测为正例中实际为正例的比例' },
        { value: 'recall', label: '召回率', description: '实际为正例中被模型预测为正例的比例' },
        { value: 'f1', label: 'F1分数', description: '精确率和召回率的调和平均值' },
        { value: 'bleu', label: 'BLEU', description: '评估生成文本与参考文本的相似度' },
        { value: 'rouge', label: 'ROUGE', description: '评估生成摘要与参考摘要的相似度' },
        { value: 'perplexity', label: '困惑度', description: '评估语言模型预测下一个词的能力' }
      ]
    }
  },
  methods: {
    // 获取模型列表
    fetchModels() {
      return this.$store.dispatch('evaluationCenter/fetchAllModels')
        .then(models => {
          this.modelOptions = models || []
          return models
        })
        .catch(error => {
          console.error('获取模型列表失败:', error)
          this.$message.error('获取模型列表失败')
          this.modelOptions = []
          return []
        })
    },
    
    // 获取数据集列表
    fetchDatasets() {
      return this.$store.dispatch('evaluationCenter/fetchAllDatasets')
        .then(datasets => {
          this.datasetOptions = datasets || []
          return datasets
        })
        .catch(error => {
          console.error('获取数据集列表失败:', error)
          this.$message.error('获取数据集列表失败')
          this.datasetOptions = []
          return []
        })
    },
    
    // 处理模型变更
    handleModelChange(modelId) {
      this.selectedModel = this.modelOptions.find(model => model.id === modelId)
    },
    
    // 处理数据集变更
    handleDatasetChange(datasetId) {
      this.selectedDataset = this.datasetOptions.find(dataset => dataset.id === datasetId)
      
      // 根据数据集类型自动选择适合的评测指标
      if (this.selectedDataset) {
        this.taskForm.metrics = []
        
        switch (this.selectedDataset.type) {
          case 'classification':
            this.taskForm.metrics = ['accuracy', 'precision', 'recall', 'f1']
            break
          case 'generation':
            this.taskForm.metrics = ['bleu', 'rouge']
            break
          case 'language_modeling':
            this.taskForm.metrics = ['perplexity']
            break
          default:
            break
        }
      }
    },
    
    // 提交表单
    submitForm() {
      this.$refs.taskForm.validate(valid => {
        if (valid) {
          this.submitting = true
          
          // 构建评测任务数据
          const taskData = {
            name: this.taskForm.name,
            description: this.taskForm.description,
            model_id: this.taskForm.model_id,
            dataset_id: this.taskForm.dataset_id,
            metrics: this.taskForm.metrics,
            parameters: this.taskForm.parameters
          }
          
          // 创建评测任务
          this.$store.dispatch('evaluationCenter/createEvaluationTask', taskData)
            .then(success => {
              this.submitting = false
              if (success) {
                this.$message.success('创建评测任务成功')
                this.$emit('created')
              } else {
                this.$message.error('创建评测任务失败')
              }
            })
            .catch(error => {
              console.error('创建评测任务失败:', error)
              this.$message.error('创建评测任务失败: ' + (error.message || '未知错误'))
              this.submitting = false
            })
        } else {
          this.$message.warning('请完善表单信息')
          return false
        }
      })
    },
    
    // 重置表单
    resetForm() {
      this.$refs.taskForm.resetFields()
      this.selectedModel = null
      this.selectedDataset = null
    },
    
    // 取消创建
    handleCancel() {
      this.$emit('cancel')
    }
  },
  created() {
    this.fetchModels()
    this.fetchDatasets()
  }
}
</script>

<style scoped>
.evaluation-task-create {
  padding: 20px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.form-section-title {
  margin: 20px 0 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
  color: #303133;
}
</style> 