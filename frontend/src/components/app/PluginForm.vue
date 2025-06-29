<template>
  <div class="plugin-form">
    <el-form
      ref="form"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="form-container"
    >
      <!-- 基本信息 -->
      <h3>基本信息</h3>
      <el-form-item label="插件名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入插件名称"></el-input>
      </el-form-item>
      
      <el-form-item label="版本" prop="version">
        <el-input v-model="formData.version" placeholder="请输入版本号"></el-input>
      </el-form-item>
      
      <el-form-item label="描述" prop="description">
        <el-input
          type="textarea"
          v-model="formData.description"
          :rows="3"
          placeholder="请输入插件描述"
        ></el-input>
      </el-form-item>

      <!-- 兼容性信息 -->
      <h3>兼容性信息</h3>
      <div v-for="(item, index) in compatibilityItems" :key="index" class="compatibility-item">
        <el-form-item :label="item.label" :prop="`compatibility.${item.key}`">
          <el-input v-model="formData.compatibility[item.key]" :placeholder="`请输入${item.label}`"></el-input>
        </el-form-item>
      </div>
      
      <el-form-item>
        <el-button type="primary" size="small" @click="addCustomCompatibility">添加自定义兼容性</el-button>
      </el-form-item>
      
      <div v-for="(item, index) in customCompatibilityItems" :key="`custom-${index}`" class="compatibility-item">
        <el-row :gutter="10">
          <el-col :span="8">
            <el-form-item label="名称">
              <el-input v-model="item.key" placeholder="请输入名称"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="14">
            <el-form-item label="值">
              <el-input v-model="item.value" placeholder="请输入值"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2">
            <el-button
              type="danger"
              icon="el-icon-delete"
              circle
              size="mini"
              @click="removeCustomCompatibility(index)"
              style="margin-top: 10px;"
            ></el-button>
          </el-col>
        </el-row>
      </div>

      <!-- 插件文件 -->
      <h3>插件文件</h3>
      <el-form-item label="插件文件" prop="file">
        <el-upload
          class="upload-container"
          action="#"
          :http-request="handleFileUpload"
          :before-upload="beforeUpload"
          :limit="1"
          :file-list="fileList"
        >
          <el-button type="primary">选择文件</el-button>
          <div slot="tip" class="el-upload__tip">支持上传zip、js、py等格式的插件文件</div>
        </el-upload>
      </el-form-item>

      <!-- 表单按钮 -->
      <div class="form-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '保存' : '上传' }}
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'PluginForm',
  props: {
    // 如果是编辑模式，传入现有的插件数据
    pluginData: {
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
      fileList: [],
      // 表单数据
      formData: {
        name: '',
        version: '',
        description: '',
        compatibility: {
          framework: '',
          model_type: '',
          min_version: '',
          max_version: ''
        },
        file: null
      },
      // 自定义兼容性项
      customCompatibilityItems: [],
      // 表单验证规则
      rules: {
        name: [
          { required: true, message: '请输入插件名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入版本号', trigger: 'blur' },
          { pattern: /^\d+\.\d+\.\d+$/, message: '版本号格式为 x.y.z', trigger: 'blur' }
        ],
        description: [
          { max: 200, message: '描述不能超过200个字符', trigger: 'blur' }
        ],
        file: [
          { required: true, message: '请上传插件文件', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    // 预定义的兼容性项
    compatibilityItems() {
      return [
        { key: 'framework', label: '框架' },
        { key: 'model_type', label: '模型类型' },
        { key: 'min_version', label: '最低版本' },
        { key: 'max_version', label: '最高版本' }
      ]
    }
  },
  methods: {
    // 添加自定义兼容性项
    addCustomCompatibility() {
      this.customCompatibilityItems.push({ key: '', value: '' })
    },
    
    // 移除自定义兼容性项
    removeCustomCompatibility(index) {
      this.customCompatibilityItems.splice(index, 1)
    },
    
    // 处理文件上传前的验证
    beforeUpload(file) {
      const validExtensions = ['.zip', '.js', '.py', '.json', '.yaml', '.yml']
      const isValidType = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
      const isLt10M = file.size / 1024 / 1024 < 10

      if (!isValidType) {
        this.$message.error('不支持的文件类型!')
      }
      
      if (!isLt10M) {
        this.$message.error('文件大小不能超过10MB!')
      }
      
      return isValidType && isLt10M
    },
    
    // 处理文件上传
    handleFileUpload(options) {
      this.formData.file = options.file
      this.fileList = [{ name: options.file.name, url: '' }]
    },
    
    // 处理表单提交
    handleSubmit() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.submitting = true
          
          // 处理自定义兼容性项
          const compatibility = { ...this.formData.compatibility }
          this.customCompatibilityItems.forEach(item => {
            if (item.key && item.value) {
              compatibility[item.key] = String(item.value)
            }
          })
          
          // 构建提交数据
          const formData = new FormData()
          
          // 添加基本信息
          formData.append('name', this.formData.name)
          formData.append('version', this.formData.version)
          formData.append('description', this.formData.description)
          formData.append('compatibility', JSON.stringify(compatibility))
          
          // 添加文件（如果有）
          if (this.formData.file && !this.isEdit) {
            formData.append('file', this.formData.file)
          }
          
          // 触发提交事件
          this.$emit('submit', formData)
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
      this.fileList = []
      this.customCompatibilityItems = []
      this.submitting = false
    }
  },
  created() {
    // 如果是编辑模式，初始化表单数据
    if (this.isEdit && this.pluginData) {
      // 基本信息
      this.formData.name = this.pluginData.name || ''
      this.formData.version = this.pluginData.version || ''
      this.formData.description = this.pluginData.description || ''
      
      // 兼容性信息
      if (this.pluginData.compatibility) {
        // 预定义的兼容性项
        const predefinedKeys = this.compatibilityItems.map(item => item.key)
        
        // 确保兼容性对象中的所有值都是字符串
        const compatibility = { ...this.pluginData.compatibility }
        predefinedKeys.forEach(key => {
          this.formData.compatibility[key] = compatibility[key] ? String(compatibility[key]) : ''
        })
        
        // 处理自定义兼容性项
        Object.keys(compatibility).forEach(key => {
          if (!predefinedKeys.includes(key)) {
            this.customCompatibilityItems.push({
              key: key,
              value: compatibility[key] ? String(compatibility[key]) : ''
            })
          }
        })
      }
      
      // 如果有文件信息，添加到文件列表
      if (this.pluginData.file_name) {
        this.fileList = [{ name: this.pluginData.file_name, url: '' }]
      }
    }
  }
}
</script>

<style scoped>
.plugin-form {
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

.compatibility-item {
  margin-bottom: 10px;
}

.upload-container {
  width: 100%;
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