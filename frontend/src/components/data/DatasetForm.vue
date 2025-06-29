<template>
  <div class="dataset-form">
    <el-form 
      ref="form" 
      :model="formData" 
      :rules="rules" 
      label-width="100px"
      size="medium"
    >
      <el-form-item label="数据集名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入数据集名称"></el-input>
      </el-form-item>
      
      <el-form-item label="描述" prop="description">
        <el-input 
          v-model="formData.description" 
          type="textarea" 
          :rows="4" 
          placeholder="请输入数据集描述"
        ></el-input>
      </el-form-item>
      
      <el-form-item v-if="type === 'create'" label="数据集文件" prop="file">
        <el-upload
          class="upload-demo"
          drag
          action="#"
          :http-request="handleFileUpload"
          :limit="1"
          :file-list="fileList"
          :before-upload="beforeUpload"
          :on-remove="handleRemove"
          :on-exceed="handleExceed"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">支持CSV、JSON、TXT等格式文件，大小不超过100MB</div>
        </el-upload>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="loading">保存</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'DatasetForm',
  props: {
    // 数据集对象
    dataset: {
      type: Object,
      default: () => ({
        name: '',
        description: '',
        file: null
      })
    },
    // 表单类型：create 或 edit
    type: {
      type: String,
      default: 'create',
      validator: value => ['create', 'edit'].includes(value)
    }
  },
  data() {
    return {
      formData: {
        id: '',
        name: '',
        description: '',
        file: null
      },
      fileList: [],
      loading: false,
      rules: {
        name: [
          { required: true, message: '请输入数据集名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        file: [
          { required: this.type === 'create', message: '请上传数据集文件', trigger: 'change' }
        ]
      }
    }
  },
  watch: {
    dataset: {
      handler(newVal) {
        if (newVal) {
          this.formData = JSON.parse(JSON.stringify(newVal))
          
          // 如果有文件，添加到文件列表
          if (this.formData.file && typeof this.formData.file === 'object') {
            this.fileList = [this.formData.file]
          } else {
            this.fileList = []
          }
        }
      },
      immediate: true,
      deep: true
    },
    type: {
      handler(newVal) {
        // 根据表单类型更新文件验证规则
        this.rules.file[0].required = newVal === 'create'
      },
      immediate: true
    }
  },
  methods: {
    // 提交表单
    submitForm() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.loading = true
          
          // 发送表单数据到父组件
          this.$emit('submit', this.formData)
          
          // 模拟异步操作
          setTimeout(() => {
            this.loading = false
          }, 500)
        } else {
          return false
        }
      })
    },
    
    // 取消操作
    handleCancel() {
      this.$emit('cancel')
    },
    
    // 处理文件上传
    handleFileUpload(options) {
      this.formData.file = options.file
      this.fileList = [options.file]
    },
    
    // 上传前检查
    beforeUpload(file) {
      // 检查文件大小，限制为100MB
      const isLt100M = file.size / 1024 / 1024 < 100
      if (!isLt100M) {
        this.$message.error('上传文件大小不能超过 100MB!')
        return false
      }
      return true
    },
    
    // 处理文件移除
    handleRemove() {
      this.formData.file = null
      this.fileList = []
    },
    
    // 处理超出文件数量限制
    handleExceed() {
      this.$message.warning('只能上传一个文件')
    },
    
    // 重置表单
    resetForm() {
      this.$refs.form.resetFields()
      this.formData = {
        id: '',
        name: '',
        description: '',
        file: null
      }
      this.fileList = []
    }
  }
}
</script>

<style scoped>
.dataset-form {
  padding: 20px 0;
}

.upload-demo {
  width: 100%;
}
</style> 