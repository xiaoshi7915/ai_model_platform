<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="login-header">
        <img src="../assets/logo.png" alt="Logo" class="login-logo">
        <h2 class="login-title">大模型构建管理平台</h2>
      </div>
      
      <el-form ref="loginForm" :model="loginForm" :rules="loginRules" label-width="0" class="login-form">
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            prefix-icon="el-icon-user" 
            placeholder="用户名"
            @keyup.enter.native="handleLogin"
          ></el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            prefix-icon="el-icon-lock" 
            placeholder="密码" 
            show-password
            @keyup.enter.native="handleLogin"
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" :loading="loading" class="login-button" @click="handleLogin">登录</el-button>
        </el-form-item>
        
        <div class="login-options">
          <router-link to="/register" class="register-link">注册账号</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: 'admin',
        password: 'admin123456@'
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    ...mapActions('user', ['login']),
    handleLogin() {
      this.$refs.loginForm.validate(async valid => {
        if (valid) {
          this.loading = true;
          try {
            console.log('登录表单数据:', this.loginForm);
            
            // 使用Vuex store的login action
            const response = await this.$store.dispatch('user/login', this.loginForm);
            console.log('登录响应:', response);
            
            // 获取用户信息
            await this.$store.dispatch('user/getUserInfo');
            
            this.$message.success('登录成功');
            this.$router.push('/');
          } catch (error) {
            console.error('登录失败:', error);
            // 不显示密码错误提示，只在控制台记录
            if (error.response && error.response.status === 401) {
              console.log('用户名或密码不正确');
            } else {
              this.$message.error('登录失败，请稍后再试');
            }
          } finally {
            this.loading = false;
          }
        } else {
          return false;
        }
      });
    },
    handleTempLogin() {
      // 实现临时登录逻辑
      console.log('临时登录');
      
      // 设置一个临时token
      const tempToken = 'temp_token_for_development_' + Date.now();
      localStorage.setItem('token', tempToken);
      
      // 设置临时用户信息
      const tempUserInfo = {
        id: 1,
        username: 'admin',
        email: 'admin@example.com',
        is_staff: true,
        is_superuser: true
      };
      localStorage.setItem('userInfo', JSON.stringify(tempUserInfo));
      
      this.$message.success('临时登录成功（仅用于开发测试）');
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
}

.login-card {
  width: 400px;
  padding: 20px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-logo {
  height: 60px;
  margin-bottom: 15px;
}

.login-title {
  font-size: 22px;
  color: #303133;
  margin: 0;
}

.login-form {
  margin-top: 20px;
}

.login-button {
  width: 100%;
}

.login-options {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
  font-size: 14px;
}

.register-link {
  color: #409EFF;
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}
</style> 