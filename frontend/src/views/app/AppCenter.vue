<template>
  <div class="app-center-view">
    <el-card class="page-header">
      <div class="page-title">
        <h2>应用中心</h2>
        <div class="page-description">
          管理应用部署和插件，实现模型能力的快速应用
        </div>
      </div>
    </el-card>

    <el-tabs v-model="activeTab" type="card" class="main-tabs" @tab-click="handleTabClick">
      <el-tab-pane label="应用管理" name="applications">
        <application-management />
      </el-tab-pane>
      
      <el-tab-pane label="插件管理" name="plugins">
        <plugin-management />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import ApplicationManagement from '@/components/app/ApplicationManagement.vue'
import PluginManagement from '@/components/app/PluginManagement.vue'

export default {
  name: 'AppCenterView',
  components: {
    ApplicationManagement,
    PluginManagement
  },
  data() {
    return {
      activeTab: 'applications'
    }
  },
  created() {
    // 根据路由路径设置当前活动标签
    const path = this.$route.path
    if (path.includes('/app-center/plugins')) {
      this.activeTab = 'plugins'
    } else {
      this.activeTab = 'applications'
    }
  },
  methods: {
    handleTabClick() {
      let path = '/app-center'
      if (this.activeTab === 'plugins') {
        path = '/app-center/plugins'
      } else {
        path = '/app-center/applications'
      }
      
      if (this.$route.path !== path) {
        this.$router.push(path)
      }
    }
  },
  watch: {
    // 监听路由变化，更新当前标签
    '$route.path'(newPath) {
      if (newPath.includes('/app-center/plugins')) {
        this.activeTab = 'plugins'
      } else if (newPath.includes('/app-center/applications')) {
        this.activeTab = 'applications'
      }
    }
  }
}
</script>

<style scoped>
.app-center-view {
  padding: 20px;
  min-height: calc(100vh - 84px);
  background-color: #f5f7fa;
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

.main-tabs {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.main-tabs >>> .el-tabs__header {
  margin-bottom: 0;
  padding: 0 20px;
}

.main-tabs >>> .el-tabs__content {
  padding: 20px;
}
</style> 