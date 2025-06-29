<template>
  <div class="evaluation-center-container">
    <!-- 路由视图容器 -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'EvaluationCenterContainer',
  data() {
    return {}
  }
}
</script>

<style scoped>
.evaluation-center-container {
  height: 100%;
  width: 100%;
}
</style> 