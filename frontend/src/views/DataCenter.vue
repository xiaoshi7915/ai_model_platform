<template>
  <div class="data-center">
    <el-tabs v-model="activeTab" type="card" @tab-click="handleTabClick">
      <el-tab-pane label="数据集管理" name="datasets">
        <dataset-management></dataset-management>
      </el-tab-pane>
      
      <el-tab-pane label="知识库管理" name="knowledge">
        <knowledge-base-management></knowledge-base-management>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import DatasetManagement from '@/components/data/DatasetManagement.vue'
import KnowledgeBaseManagement from '@/components/data/KnowledgeBaseManagement.vue'

export default {
  name: 'DataCenter',
  components: {
    DatasetManagement,
    KnowledgeBaseManagement
  },
  data() {
    return {
      activeTab: 'datasets'
    }
  },
  created() {
    // 根据路由路径设置当前活动标签
    const path = this.$route.path
    if (path.includes('/data-center/knowledge')) {
      this.activeTab = 'knowledge'
    } else {
      this.activeTab = 'datasets'
    }
  },
  methods: {
    handleTabClick(tab) {
      let path = '/data-center'
      if (tab.name === 'knowledge') {
        path = '/data-center/knowledge'
      } else {
        path = '/data-center/datasets'
      }
      
      if (this.$route.path !== path) {
        this.$router.push(path)
      }
    }
  },
  watch: {
    // 监听路由变化，更新当前标签
    '$route.path'(newPath) {
      if (newPath.includes('/data-center/knowledge')) {
        this.activeTab = 'knowledge'
      } else if (newPath.includes('/data-center/datasets')) {
        this.activeTab = 'datasets'
      }
    }
  }
}
</script>

<style scoped>
.data-center {
  padding: 20px;
  min-height: calc(100vh - 84px);
  background-color: #f5f7fa;
}

.el-tabs {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-tabs >>> .el-tabs__header {
  margin-bottom: 0;
  padding: 0 20px;
}

.el-tabs >>> .el-tabs__content {
  padding: 0;
}

.el-tab-pane {
  padding: 0;
}
</style> 