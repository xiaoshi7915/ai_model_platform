<template>
  <div class="docker-image-form">
    <el-form
      ref="form"
      :model="formData"
      :rules="rules"
      label-width="120px"
      class="form-container"
    >
      <!-- 基本信息 -->
      <h3>基本信息</h3>
      <el-form-item label="镜像名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入镜像名称"></el-input>
      </el-form-item>
      
      <el-form-item label="标签" prop="tag">
        <el-input v-model="formData.tag" placeholder="请输入标签"></el-input>
      </el-form-item>
      
      <el-form-item label="仓库" prop="registry">
        <el-input v-model="formData.registry" placeholder="请输入仓库地址">
          <template slot="prepend">https://</template>
        </el-input>
      </el-form-item>
      
      <el-form-item label="描述" prop="description">
        <el-input
          type="textarea"
          v-model="formData.description"
          :rows="3"
          placeholder="请输入镜像描述"
        ></el-input>
      </el-form-item>

      <!-- 上传方式选择 -->
      <h3>上传方式</h3>
      <el-form-item label="上传方式" prop="upload_type">
        <el-radio-group v-model="formData.upload_type">
          <el-radio label="file">本地文件上传</el-radio>
          <el-radio label="pull">从远程仓库拉取</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <!-- 本地文件上传 -->
      <div v-if="formData.upload_type === 'file'">
        <el-form-item label="镜像文件" prop="file">
          <el-upload
            class="upload-container"
            action="#"
            :http-request="handleFileUpload"
            :before-upload="beforeUpload"
            :limit="1"
            :file-list="fileList"
          >
            <el-button type="primary">选择文件</el-button>
            <div slot="tip" class="el-upload__tip">只能上传tar格式的Docker镜像文件，且不超过500MB</div>
          </el-upload>
        </el-form-item>
        
        <el-form-item label="镜像大小" prop="size">
          <el-input-number
            v-model="formData.size"
            :min="1"
            :max="10000"
            label="镜像大小(MB)"
          ></el-input-number>
        </el-form-item>
      </div>
      
      <!-- 远程仓库拉取 -->
      <div v-if="formData.upload_type === 'pull'">
        <el-form-item label="完整镜像名称" prop="full_name">
          <el-input 
            v-model="formData.full_name" 
            placeholder="例如: docker.io/library/ubuntu:20.04"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="认证信息">
          <el-switch
            v-model="formData.need_auth"
            active-text="需要认证"
            inactive-text="无需认证"
          ></el-switch>
        </el-form-item>
        
        <div v-if="formData.need_auth">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="formData.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input 
              v-model="formData.password" 
              type="password" 
              placeholder="请输入密码"
              show-password
            ></el-input>
          </el-form-item>
        </div>
      </div>

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
  name: 'DockerImageForm',
  props: {
    // 如果是编辑模式，传入现有的镜像数据
    imageData: {
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
        tag: 'latest',
        registry: 'docker.io',
        description: '',
        size: 100,
        upload_type: 'pull',
        full_name: '',
        need_auth: false,
        username: '',
        password: '',
        file: null
      },
      // 表单验证规则
      rules: {
        name: [
          { required: true, message: '请输入镜像名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        tag: [
          { required: true, message: '请输入标签', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9_.-]+$/, message: '标签格式不正确', trigger: 'blur' }
        ],
        registry: [
          { required: true, message: '请输入仓库地址', trigger: 'blur' }
        ],
        description: [
          { max: 200, message: '描述不能超过200个字符', trigger: 'blur' }
        ],
        full_name: [
          { required: true, message: '请输入完整镜像名称', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    // 如果是编辑模式，初始化表单数据
    if (this.isEdit && this.imageData) {
      Object.keys(this.formData).forEach(key => {
        if (this.imageData[key] !== undefined) {
          this.formData[key] = this.imageData[key]
        }
      })
    }
  },
  methods: {
    // 处理文件上传前的验证
    beforeUpload(file) {
      const isTar = file.type === 'application/x-tar' || file.name.endsWith('.tar')
      const isLt500M = file.size / 1024 / 1024 < 500

      if (!isTar) {
        this.$message.error('只能上传tar格式的Docker镜像文件!')
      }
      
      if (!isLt500M) {
        this.$message.error('镜像文件大小不能超过500MB!')
      }
      
      return isTar && isLt500M
    },
    
    // 处理文件上传
    handleFileUpload(options) {
      this.formData.file = options.file
      this.fileList = [{ name: options.file.name, url: '' }]
      // 自动计算文件大小（MB）
      this.formData.size = Math.ceil(options.file.size / 1024 / 1024)
    },
    
    // 处理表单提交
    handleSubmit() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.submitting = true
          
          // 构建提交数据
          const submitData = { ...this.formData }
          
          // 根据上传方式处理数据
          if (submitData.upload_type === 'pull') {
            // 如果不需要认证，删除认证信息
            if (!submitData.need_auth) {
              delete submitData.username
              delete submitData.password
            }
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
      this.fileList = []
      this.submitting = false
    }
  }
}
</script>

<style scoped>
.docker-image-form {
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