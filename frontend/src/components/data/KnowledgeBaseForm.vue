<template>
  <div class="knowledge-base-form">
    <el-form 
      ref="form" 
      :model="formData" 
      :rules="rules" 
      label-width="100px"
      size="medium"
    >
      <el-form-item label="知识库名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入知识库名称"></el-input>
      </el-form-item>
      
      <el-form-item label="描述" prop="description">
        <el-input 
          v-model="formData.description" 
          type="textarea" 
          :rows="3" 
          placeholder="请输入知识库描述"
        ></el-input>
      </el-form-item>
      
      <el-form-item label="内容" prop="content">
        <div class="content-actions">
          <el-button 
            type="text" 
            icon="el-icon-upload2" 
            @click="$refs.fileInput.click()"
          >从文件导入</el-button>
          <input 
            ref="fileInput" 
            type="file" 
            style="display: none" 
            accept=".txt,.md,.json"
            @change="handleFileImport"
          />
        </div>
        <el-input 
          v-model="formData.content" 
          type="textarea" 
          :rows="15" 
          placeholder="请输入知识库内容"
        ></el-input>
      </el-form-item>
      
      <el-form-item label="是否公开">
        <el-switch v-model="formData.is_public"></el-switch>
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
  name: 'KnowledgeBaseForm',
  props: {
    // 知识库对象
    knowledgeBase: {
      type: Object,
      default: () => ({
        name: '',
        description: '',
        content: '',
        is_public: false
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
        content: '',
        is_public: false
      },
      loading: false,
      rules: {
        name: [
          { required: true, message: '请输入知识库名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入知识库内容', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    knowledgeBase: {
      handler(newVal) {
        if (newVal) {
          this.formData = JSON.parse(JSON.stringify(newVal))
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
    
    // 处理文件导入
    handleFileImport(event) {
      const file = event.target.files[0]
      if (!file) return
      
      // 检查文件大小，限制为10MB
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        this.$message.error('文件大小不能超过 10MB!')
        return
      }
      
      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          // 尝试解析为JSON
          if (file.name.endsWith('.json')) {
            const jsonObj = JSON.parse(e.target.result)
            this.formData.content = JSON.stringify(jsonObj, null, 2)
          } else {
            // 文本文件直接读取
            this.formData.content = e.target.result
          }
          
          // 如果文件名合适，可以用作知识库名称
          if (!this.formData.name && file.name) {
            // 去掉扩展名作为知识库名称
            const fileName = file.name.split('.').slice(0, -1).join('.')
            if (fileName.length >= 2 && fileName.length <= 50) {
              this.formData.name = fileName
            }
          }
          
          this.$message.success('文件导入成功')
        } catch (error) {
          console.error('文件解析失败:', error)
          this.$message.error('文件解析失败，请检查文件格式')
        }
      }
      
      reader.onerror = () => {
        this.$message.error('文件读取失败')
      }
      
      if (file.name.endsWith('.json')) {
        reader.readAsText(file)
      } else {
        reader.readAsText(file)
      }
      
      // 重置文件输入，以便可以重新选择同一个文件
      event.target.value = ''
    },
    
    // 重置表单
    resetForm() {
      this.$refs.form.resetFields()
      this.formData = {
        id: '',
        name: '',
        description: '',
        content: '',
        is_public: false
      }
    }
  }
}
</script>

<style scoped>
.knowledge-base-form {
  padding: 20px 0;
}

.content-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 5px;
}
</style> 