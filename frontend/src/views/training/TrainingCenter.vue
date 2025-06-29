<template>
  <div class="training-center-view">
    <el-card class="page-header">
      <div class="page-title">
        <h2>模型训练中心</h2>
        <div class="page-description">
          管理模型训练、模型管理和Docker镜像管理
        </div>
      </div>
    </el-card>

    <el-tabs v-model="activeTab" type="card" class="main-tabs" @tab-click="handleTabClick">
      <el-tab-pane label="模型管理" name="models">
        <model-management></model-management>
      </el-tab-pane>
      
      <el-tab-pane label="训练任务" name="jobs">
        <training-jobs></training-jobs>
      </el-tab-pane>
      
      <el-tab-pane label="镜像管理" name="images">
        <docker-image-management></docker-image-management>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import ModelManagement from '@/components/training/ModelManagement.vue'
import TrainingJobs from '@/components/training/TrainingJobs.vue'
import DockerImageManagement from '@/components/training/DockerImageManagement.vue'

export default {
  name: 'TrainingCenterView',
  components: {
    ModelManagement,
    TrainingJobs,
    DockerImageManagement
  },
  data() {
    return {
      activeTab: 'models'
    }
  },
  created() {
    // 根据路由路径设置当前活动标签
    const path = this.$route.path
    if (path.includes('/training-center/jobs')) {
      this.activeTab = 'jobs'
    } else if (path.includes('/training-center/docker-images')) {
      this.activeTab = 'images'
    } else {
      this.activeTab = 'models'
    }
  },
  methods: {
    handleTabClick(tab) {
      let path = '/training-center/models'
      if (tab.name === 'jobs') {
        path = '/training-center/jobs'
      } else if (tab.name === 'images') {
        path = '/training-center/docker-images'
      } else {
        path = '/training-center/models'
      }
      
      if (this.$route.path !== path) {
        this.$router.push(path)
      }
    }
  },
  watch: {
    // 监听路由变化，更新当前标签
    '$route.path'(newPath) {
      if (newPath.includes('/training-center/jobs')) {
        this.activeTab = 'jobs'
      } else if (newPath.includes('/training-center/docker-images')) {
        this.activeTab = 'images'
      } else if (newPath.includes('/training-center/models')) {
        this.activeTab = 'models'
      }
    }
  }
}
</script>

<style scoped>
.training-center-view {
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