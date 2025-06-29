<template>
  <div class="evaluation-center-view">
    <el-card class="page-header">
      <div class="page-title">
        <h2>模型评测中心</h2>
        <div class="page-description">
          对模型进行全面评测，获取详细的性能报告和优化建议
        </div>
      </div>
    </el-card>

    <el-tabs v-model="activeTab" type="card" class="main-tabs" @tab-click="handleTabClick">
      <el-tab-pane label="模型评测" name="tasks">
        <evaluation-task-list v-if="activeTab === 'tasks'" />
      </el-tab-pane>
      
      <el-tab-pane label="模型对比" name="comparison">
        <model-comparison v-if="activeTab === 'comparison'" />
      </el-tab-pane>
      
      <el-tab-pane label="评测报告" name="reports">
        <evaluation-report-list v-if="activeTab === 'reports'" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import EvaluationTaskList from '@/components/evaluation/EvaluationTaskList.vue'
import ModelComparison from '@/components/evaluation/ModelComparison.vue'
import EvaluationReportList from '@/components/evaluation/EvaluationReportList.vue'

export default {
  name: 'EvaluationCenterView',
  components: {
    EvaluationTaskList,
    ModelComparison,
    EvaluationReportList
  },
  data() {
    return {
      activeTab: 'tasks'
    }
  },
  created() {
    // 根据路由路径设置当前活动标签
    this.updateActiveTabFromRoute();
  },
  methods: {
    updateActiveTabFromRoute() {
      const path = this.$route.path;
      // 检查当前URL路径中是否包含特定部分
      if (path.includes('/comparison')) {
        this.activeTab = 'comparison';
      } else if (path.includes('/reports')) {
        this.activeTab = 'reports';
      } else {
        this.activeTab = 'tasks';
      }
    },
    handleTabClick(tab) {
      // 根据标签名导航到相应的路由
      let path;
      switch (tab.name) {
        case 'comparison':
          path = '/evaluation-center/comparison';
          break;
        case 'reports':
          path = '/evaluation-center/reports';
          break;
        default:
          path = '/evaluation-center/tasks';
      }
      
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    }
  },
  watch: {
    // 监听路由变化，更新当前标签
    '$route.path'() {
      this.updateActiveTabFromRoute();
    }
  }
}
</script>

<style scoped>
.evaluation-center-view {
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