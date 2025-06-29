<template>
  <div class="model-comparison-create">
    <div class="page-header">
      <div class="page-title">
        <h2>创建模型对比</h2>
        <span class="page-description">选择要对比的模型和评测指标</span>
      </div>
    </div>

    <el-card class="form-card">
      <el-form ref="comparisonForm" :model="comparisonForm" :rules="rules" label-width="120px">
        <!-- 基本信息 -->
        <h3>基本信息</h3>
        <el-form-item label="对比名称" prop="name">
          <el-input v-model="comparisonForm.name" placeholder="请输入对比名称"></el-input>
        </el-form-item>
        
        <el-form-item label="对比描述" prop="description">
          <el-input
            type="textarea"
            v-model="comparisonForm.description"
            :rows="3"
            placeholder="请输入对比描述"
          ></el-input>
        </el-form-item>

        <!-- 对比模型 -->
        <h3>对比模型</h3>
        <el-form-item label="基准模型" prop="baseModelId">
          <el-select 
            v-model="comparisonForm.baseModelId" 
            placeholder="请选择基准模型"
            style="width: 100%"
          >
            <el-option
              v-for="model in models"
              :key="model.id"
              :label="model.name"
              :value="model.id"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="对比模型" prop="compareModelIds">
          <el-select 
            v-model="comparisonForm.compareModelIds" 
            multiple
            placeholder="请选择要对比的模型"
            style="width: 100%"
          >
            <el-option
              v-for="model in compareModels"
              :key="model.id"
              :label="model.name"
              :value="model.id"
            ></el-option>
          </el-select>
        </el-form-item>

        <!-- 对比配置 -->
        <h3>对比配置</h3>
        <el-form-item label="评测数据集" prop="datasetId">
          <el-select 
            v-model="comparisonForm.datasetId" 
            placeholder="请选择评测数据集"
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

        <el-form-item label="对比指标" prop="metrics">
          <el-checkbox-group v-model="comparisonForm.metrics">
            <el-checkbox label="accuracy">准确率</el-checkbox>
            <el-checkbox label="precision">精确率</el-checkbox>
            <el-checkbox label="recall">召回率</el-checkbox>
            <el-checkbox label="f1">F1分数</el-checkbox>
            <el-checkbox label="latency">延迟</el-checkbox>
            <el-checkbox label="throughput">吞吐量</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="高级参数" prop="parameters">
          <el-input
            type="textarea"
            v-model="comparisonForm.parameters"
            :rows="4"
            placeholder="请输入JSON格式的高级参数配置"
          ></el-input>
          <div class="parameter-help">
            <i class="el-icon-info"></i>
            参数示例：{"batch_size": 32, "max_length": 512}
          </div>
        </el-form-item>

        <!-- 提交按钮 -->
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">创建对比</el-button>
          <el-button @click="handleCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'ModelComparisonCreate',
  
  data() {
    return {
      submitting: false,
      comparisonForm: {
        name: '',
        description: '',
        baseModelId: '',
        compareModelIds: [],
        datasetId: '',
        metrics: [],
        parameters: '{}'
      },
      rules: {
        name: [
          { required: true, message: '请输入对比名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        baseModelId: [
          { required: true, message: '请选择基准模型', trigger: 'change' }
        ],
        compareModelIds: [
          { type: 'array', required: true, message: '请至少选择一个对比模型', trigger: 'change' }
        ],
        datasetId: [
          { required: true, message: '请选择评测数据集', trigger: 'change' }
        ],
        metrics: [
          { type: 'array', required: true, message: '请至少选择一个对比指标', trigger: 'change' }
        ],
        parameters: [
          { 
            validator: (rule, value, callback) => {
              try {
                if (value) {
                  JSON.parse(value)
                }
                callback()
              } catch (error) {
                callback(new Error('请输入有效的JSON格式'))
              }
            },
            trigger: 'blur'
          }
        ]
      }
    }
  },
  
  computed: {
    ...mapState('evaluationCenter', [
      'models',
      'datasets'
    ]),
    
    // 过滤掉基准模型，避免重复选择
    compareModels() {
      return this.models.filter(model => model.id !== this.comparisonForm.baseModelId)
    }
  },
  
  created() {
    this.initialize()
  },
  
  methods: {
    ...mapActions('evaluationCenter', [
      'fetchAllModels',
      'fetchAllDatasets',
      'createModelComparison'
    ]),
    
    // 初始化数据
    async initialize() {
      try {
        await Promise.all([
          this.fetchAllModels(),
          this.fetchAllDatasets()
        ])
      } catch (error) {
        console.error('初始化数据失败:', error)
        this.$message.error('加载数据失败，请刷新页面重试')
      }
    },
    
    // 处理表单提交
    handleSubmit() {
      this.$refs.comparisonForm.validate(async valid => {
        if (!valid) return
        
        this.submitting = true
        try {
          await this.createModelComparison(this.comparisonForm)
          this.$message.success('创建模型对比成功')
          this.$router.push('/evaluation-center/comparison')
        } catch (error) {
          console.error('创建模型对比失败:', error)
          this.$message.error('创建模型对比失败：' + (error.message || '未知错误'))
        } finally {
          this.submitting = false
        }
      })
    },
    
    // 处理取消
    handleCancel() {
      this.$router.push('/evaluation-center/comparison')
    }
  }
}
</script>

<style scoped>
.model-comparison-create {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-title {
  display: flex;
  flex-direction: column;
}

.page-title h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.page-description {
  margin-top: 8px;
  font-size: 14px;
  color: #606266;
}

.form-card {
  background-color: #fff;
  border-radius: 4px;
}

.form-card >>> .el-card__body {
  padding: 20px;
}

h3 {
  margin: 0 0 20px;
  padding-bottom: 10px;
  font-size: 18px;
  color: #303133;
  border-bottom: 1px solid #EBEEF5;
}

.parameter-help {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}

.parameter-help .el-icon-info {
  margin-right: 5px;
}

.el-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
</style> 