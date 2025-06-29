<template>
  <div class="api-usage-logs">
    <api-logs-viewer />
  </div>
</template>

<script>
import ApiLogsViewer from './ApiLogsViewer.vue'

export default {
  name: 'ApiUsageLogs',
  components: {
    ApiLogsViewer
  }
}
</script>

<style scoped>
.api-usage-logs {
  width: 100%;
}
</style> 