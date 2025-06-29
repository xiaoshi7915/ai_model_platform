<template>
  <div class="app-center-container">
    <!-- 路由视图容器 -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'AppCenterContainer',
  data() {
    return {}
  }
}
</script>

<style scoped>
.app-center-container {
  height: 100%;
  width: 100%;
}
</style> 