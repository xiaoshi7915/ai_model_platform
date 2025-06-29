<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="sidebarWidth" class="sidebar">
      <div class="logo-container">
        <img src="../assets/logo.png" alt="Logo" class="logo" v-if="!sidebarCollapsed">
        <img src="../assets/logo-small.png" alt="Logo" class="logo-small" v-else>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        :collapse="sidebarCollapsed"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <el-menu-item index="/">
          <i class="el-icon-s-home"></i>
          <span slot="title">仪表盘</span>
        </el-menu-item>
        
        <!-- 数据中心 -->
        <el-submenu index="/data-center">
          <template slot="title">
            <i class="el-icon-folder"></i>
            <span>数据中心</span>
          </template>
          <el-menu-item index="/data-center/datasets">数据集管理</el-menu-item>
          <el-menu-item index="/data-center/knowledge">知识库管理</el-menu-item>
        </el-submenu>
        
        <!-- 训练中心 -->
        <el-submenu index="/training-center">
          <template slot="title">
            <i class="el-icon-cpu"></i>
            <span>训练中心</span>
          </template>
          <el-menu-item index="/training-center/models">模型管理</el-menu-item>
          <el-menu-item index="/training-center/jobs">训练任务管理</el-menu-item>
          <el-menu-item index="/training-center/docker-images">镜像管理</el-menu-item>
        </el-submenu>
        
        <!-- 应用中心 -->
        <el-submenu index="/app-center">
          <template slot="title">
            <i class="el-icon-s-platform"></i>
            <span>应用中心</span>
          </template>
          <el-menu-item index="/app-center/applications">应用管理</el-menu-item>
          <el-menu-item index="/app-center/plugins">插件管理</el-menu-item>
        </el-submenu>
        
        <!-- 评测中心 -->
        <el-submenu index="/evaluation-center">
          <template slot="title">
            <i class="el-icon-data-analysis"></i>
            <span>评测中心</span>
          </template>
          <el-menu-item index="/evaluation-center/tasks">评测任务管理</el-menu-item>
          <el-menu-item index="/evaluation-center/comparison">模型对比</el-menu-item>
          <el-menu-item index="/evaluation-center/reports">评测报告</el-menu-item>
        </el-submenu>
        
        <!-- API连接服务 -->
        <el-menu-item index="/api-connector">
          <i class="el-icon-connection"></i>
          <span slot="title">API连接服务</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <!-- 主体区域 -->
    <el-container>
      <!-- 头部 -->
      <el-header class="header">
        <div class="header-left">
          <i 
            :class="sidebarCollapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'" 
            class="toggle-sidebar"
            @click="toggleSidebar"
          ></i>
          <breadcrumb />
        </div>
        
        <div class="header-right">
          <el-dropdown trigger="click" @command="handleCommand">
            <span class="user-dropdown">
              {{ currentUser ? currentUser.username : '用户' }}
              <i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="profile">个人资料</el-dropdown-item>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      
      <!-- 内容区域 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
      
      <!-- 底部 -->
      <el-footer class="footer">
        <div>大模型构建管理平台 &copy; {{ currentYear }}</div>
      </el-footer>
    </el-container>
  </el-container>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import Breadcrumb from '../components/Breadcrumb.vue'

export default {
  name: 'Layout',
  components: {
    Breadcrumb
  },
  computed: {
    ...mapState({
      sidebarCollapsed: state => state.app.sidebarCollapsed,
      currentUser: state => state.user.userInfo
    }),
    sidebarWidth() {
      return this.sidebarCollapsed ? '64px' : '200px'
    },
    activeMenu() {
      return this.$route.path
    },
    currentYear() {
      return new Date().getFullYear()
    }
  },
  methods: {
    ...mapActions('app', ['toggleSidebar']),
    ...mapActions('user', ['logout']),
    async handleCommand(command) {
      if (command === 'logout') {
        try {
          await this.logout()
          this.$message.success('退出登录成功')
          this.$router.push('/login')
        } catch (error) {
          this.$message.error('退出登录失败')
        }
      } else if (command === 'profile') {
        // 跳转到个人资料页面
        this.$message.info('个人资料功能将在后续版本中实现')
      }
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  transition: width 0.3s;
  overflow-x: hidden;
}

.logo-container {
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #263445;
}

.logo {
  height: 40px;
}

.logo-small {
  height: 30px;
}

.sidebar-menu {
  border-right: none;
}

.header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.toggle-sidebar {
  font-size: 20px;
  cursor: pointer;
  margin-right: 15px;
}

.user-dropdown {
  cursor: pointer;
  color: #606266;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}

.footer {
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #606266;
  font-size: 14px;
}
</style> 