<template>
  <div class="model-form">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      label-width="120px"
      size="medium"
    >
      <!-- 基本信息 -->
      <h3>基本信息</h3>
      <el-form-item label="模型名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入模型名称"></el-input>
      </el-form-item>
      
      <el-form-item label="版本" prop="version">
        <el-input v-model="form.version" placeholder="请输入版本号"></el-input>
      </el-form-item>
      
      <el-form-item label="描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入模型描述"
        ></el-input>
      </el-form-item>
      
      <el-form-item label="训练数据集" prop="dataset">
        <el-select v-model="form.dataset" placeholder="请选择训练数据集" style="width: 100%">
          <el-option
            v-for="dataset in datasets"
            :key="dataset.id"
            :label="dataset.name"
            :value="dataset.id"
          ></el-option>
        </el-select>
      </el-form-item>
      
      <el-form-item label="训练参数" prop="parameters">
        <el-input
          v-model="form.parametersStr"
          type="textarea"
          :rows="8"
          placeholder="请输入训练参数（JSON格式）"
        ></el-input>
        <div class="form-tip">训练参数应为有效的JSON格式，例如：{"learning_rate": 0.001, "batch_size": 32, "epochs": 10}</div>
      </el-form-item>

      <!-- 表单按钮 -->
      <div class="form-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="loading">保存</el-button>
      </div>
    </el-form>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'ModelForm',
  props: {
    model: {
      type: Object,
      default: () => ({
        id: null,
        name: '',
        description: '',
        version: '',
        parameters: {},
        dataset: null
      })
    },
    type: {
      type: String,
      default: 'create'
    }
  },
  data() {
    // 验证JSON格式
    const validateParameters = (rule, value, callback) => {
      if (!value) {
        callback()
        return
      }
      
      try {
        JSON.parse(value)
        callback()
      } catch (error) {
        callback(new Error('请输入有效的JSON格式'))
      }
    }
    
    return {
      loading: false,
      form: {
        id: this.model?.id || null,
        name: this.model?.name || '',
        description: this.model?.description || '',
        version: this.model?.version || '',
        parameters: this.model?.parameters || {},
        dataset: this.model?.dataset || null,
        parametersStr: '{}'
      },
      rules: {
        name: [
          { required: true, message: '请输入模型名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9\u4e00-\u9fa5_-]+$/, message: '模型名称只能包含字母、数字、中文、下划线和短横线', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入版本号', trigger: 'blur' },
          { pattern: /^[0-9]+\.[0-9]+\.[0-9]+$/, message: '版本号格式应为 x.y.z', trigger: 'blur' }
        ],
        dataset: [
          { required: true, message: '请选择训练数据集', trigger: 'change' }
        ],
        parametersStr: [
          { validator: validateParameters, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapState({
      datasets: state => state.dataCenter.datasets
    })
  },
  watch: {
    model: {
      handler(newVal) {
        if (newVal) {
          // 深拷贝避免直接修改props
          const modelCopy = JSON.parse(JSON.stringify(newVal))
          
          // 将parameters对象转为字符串
          const parametersStr = modelCopy.parameters ? 
            JSON.stringify(modelCopy.parameters, null, 2) : 
            '{}'
          
          this.form = {
            ...modelCopy,
            parametersStr
          }
        }
      },
      immediate: true,
      deep: true
    }
  },
  methods: {
    // 提交表单
    submitForm() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.loading = true
          
          try {
            // 将参数字符串转为对象
            const parameters = this.form.parametersStr ? 
              JSON.parse(this.form.parametersStr) : 
              {}
            
            // 构建提交数据
            const submitData = {
              ...this.form,
              parameters
            }
            
            delete submitData.parametersStr // 删除临时字段
            
            // 发送表单数据到父组件
            this.$emit('submit', submitData)
            
            // 模拟异步操作
            setTimeout(() => {
              this.loading = false
            }, 500)
          } catch (error) {
            this.$message.error('训练参数格式不正确，请输入有效的JSON格式')
            this.loading = false
          }
        } else {
          return false
        }
      })
    },
    
    // 取消操作
    handleCancel() {
      this.$emit('cancel')
    },
    
    // 重置表单
    resetForm() {
      this.form = {
        id: null,
        name: '',
        description: '',
        version: '',
        parameters: {},
        dataset: null,
        parametersStr: '{}'
      }
      if (this.$refs.form) {
        this.$refs.form.resetFields()
      }
    }
  },
  created() {
    // 获取数据集列表
    if (this.datasets.length === 0) {
      this.$store.dispatch('dataCenter/fetchDatasets')
    }
  }
}
</script>

<style scoped>
.model-form {
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

.form-actions {
  margin-top: 40px;
  text-align: center;
}

.form-actions button {
  min-width: 120px;
  margin: 0 10px;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
  margin-top: 5px;
}
</style> 