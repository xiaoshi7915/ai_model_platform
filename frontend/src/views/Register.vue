<template>
  <div class="register-container">
    <el-card class="register-card">
      <div class="register-header">
        <img src="../assets/logo.png" alt="Logo" class="register-logo">
        <h2 class="register-title">注册账号</h2>
      </div>
      
      <el-form ref="registerForm" :model="registerForm" :rules="registerRules" label-width="0" class="register-form">
        <el-form-item prop="username">
          <el-input 
            v-model="registerForm.username" 
            prefix-icon="el-icon-user" 
            placeholder="用户名"
          ></el-input>
        </el-form-item>
        
        <el-form-item prop="email">
          <el-input 
            v-model="registerForm.email" 
            prefix-icon="el-icon-message" 
            placeholder="邮箱"
          ></el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="registerForm.password" 
            prefix-icon="el-icon-lock" 
            placeholder="密码" 
            show-password
          ></el-input>
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input 
            v-model="registerForm.confirmPassword" 
            prefix-icon="el-icon-lock" 
            placeholder="确认密码" 
            show-password
          ></el-input>
        </el-form-item>
        
        <el-form-item prop="agreement">
          <el-checkbox v-model="registerForm.agreement">
            我已阅读并同意
            <el-button type="text" @click="showTerms">《服务条款》</el-button>
          </el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" :loading="loading" class="register-button" @click="handleRegister">注册</el-button>
        </el-form-item>
        
        <div class="register-options">
          <span>已有账号？</span>
          <router-link to="/login" class="login-link">立即登录</router-link>
        </div>
      </el-form>
    </el-card>

    <!-- 服务条款对话框 -->
    <el-dialog
      title="服务条款"
      :visible.sync="termsDialogVisible"
      width="50%"
      class="terms-dialog"
    >
      <div class="terms-content">
        <h3>用户服务协议</h3>
        <p>欢迎使用大型模型构建管理平台！</p>
        
        <h4>1. 服务内容</h4>
        <p>本平台提供模型训练、评测和部署等相关服务。用户可以通过本平台进行数据管理、模型训练、应用部署等操作。</p>
        
        <h4>2. 用户义务</h4>
        <p>2.1 用户应当遵守中华人民共和国相关法律法规。</p>
        <p>2.2 用户应当妥善保管账号密码，对账号下的所有行为负责。</p>
        <p>2.3 用户应当合理使用平台资源，不得进行任何破坏平台正常运行的行为。</p>
        
        <h4>3. 知识产权</h4>
        <p>3.1 用户在平台上传的数据归用户所有。</p>
        <p>3.2 平台提供的软件、界面、文档等归平台所有。</p>
        
        <h4>4. 免责声明</h4>
        <p>4.1 平台不对用户的模型训练结果做任何保证。</p>
        <p>4.2 因不可抗力导致的服务中断，平台不承担责任。</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="termsDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="agreeTerms">同意</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Register',
  data() {
    // 密码确认验证
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    
    return {
      registerForm: {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        agreement: false
      },
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        email: [
          { required: false, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ],
        agreement: [
          { 
            validator: (rule, value, callback) => {
              if (!value) {
                callback(new Error('请阅读并同意服务条款'))
              } else {
                callback()
              }
            }, 
            trigger: 'change' 
          }
        ]
      },
      loading: false,
      termsDialogVisible: false
    }
  },
  methods: {
    ...mapActions('user', ['register']),
    
    // 显示服务条款
    showTerms() {
      this.termsDialogVisible = true
    },
    
    // 同意服务条款
    agreeTerms() {
      this.registerForm.agreement = true
      this.termsDialogVisible = false
    },
    
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          if (!this.registerForm.agreement) {
            this.$message.warning('请阅读并同意服务条款')
            return
          }
          
          // 验证两次密码是否一致
          if (this.registerForm.password !== this.registerForm.confirmPassword) {
            this.$message.error('两次输入的密码不一致')
            return
          }
          
          this.loading = true
          // 创建注册数据对象，移除确认密码字段
          const registerData = {
            username: this.registerForm.username,
            email: this.registerForm.email,
            password: this.registerForm.password
          }
          
          this.register(registerData)
            .then(async (response) => {
              // 注册成功后直接获取用户信息并导航到首页
              await this.$store.dispatch('user/getUserInfo');
              this.$message.success('注册成功');
              this.$router.push('/');
            })
            .catch(error => {
              this.$message.error(error.message || '注册失败')
            })
            .finally(() => {
              this.loading = false
            })
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
}

.register-card {
  width: 400px;
  padding: 20px;
}

.register-header {
  text-align: center;
  margin-bottom: 20px;
}

.register-logo {
  height: 60px;
  margin-bottom: 15px;
}

.register-title {
  font-size: 22px;
  color: #303133;
  margin: 0;
}

.register-form {
  margin-top: 20px;
}

.register-button {
  width: 100%;
}

.register-options {
  display: flex;
  justify-content: center;
  margin-top: 10px;
  font-size: 14px;
}

.login-link {
  color: #409EFF;
  text-decoration: none;
  margin-left: 5px;
}

.login-link:hover {
  text-decoration: underline;
}

/* 服务条款样式 */
.terms-content {
  max-height: 400px;
  overflow-y: auto;
  padding: 0 20px;
}

.terms-content h3 {
  text-align: center;
  margin-bottom: 20px;
}

.terms-content h4 {
  margin: 15px 0 10px;
  color: #303133;
}

.terms-content p {
  margin: 10px 0;
  line-height: 1.6;
  color: #606266;
}

.terms-dialog >>> .el-dialog__body {
  padding: 10px 20px;
}
</style> 