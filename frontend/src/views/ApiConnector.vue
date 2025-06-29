<template>
  <div class="api-connector-container">
    <h1 class="page-title">API连接服务</h1>
    <p class="page-description">管理各类外部API的连接和调用</p>
    
    <el-tabs v-model="activeTab" type="card">
      <el-tab-pane label="API配置" name="connections">
        <api-connections-manager />
      </el-tab-pane>
      <el-tab-pane label="API提供商" name="providers">
        <api-providers-manager />
      </el-tab-pane>
      <el-tab-pane label="使用统计" name="statistics">
        <api-usage-statistics />
      </el-tab-pane>
      <el-tab-pane label="使用日志" name="logs">
        <api-usage-logs />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import ApiConnectionsManager from '@/components/api_connector/ApiConnectionsManager.vue'
import ApiProvidersManager from '@/components/api_connector/ApiProvidersManager.vue'
import ApiUsageStatistics from '@/components/api_connector/ApiUsageStatistics.vue'
import ApiUsageLogs from '@/components/api_connector/ApiUsageLogs.vue'

export default {
  name: 'ApiConnector',
  components: {
    ApiConnectionsManager,
    ApiProvidersManager,
    ApiUsageStatistics,
    ApiUsageLogs
  },
  data() {
    return {
      activeTab: 'connections'
    }
  }
}
</script>

<style scoped>
.api-connector-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 8px;
  color: #303133;
}

.page-description {
  font-size: 14px;
  color: #606266;
  margin-bottom: 20px;
}
</style> 