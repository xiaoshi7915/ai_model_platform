<template>
  <div class="models-container">
    <model-management />
  </div>
</template>

<script>
import ModelManagement from './ModelManagement.vue'

export default {
  name: 'Models',
  components: {
    ModelManagement
  }
}
</script>

<style scoped>
.models-container {
  padding: 20px;
}
</style> 