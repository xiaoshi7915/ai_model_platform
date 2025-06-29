<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="index" :to="item.path">
      {{ item.meta.title || item.name }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script>
export default {
  name: 'Breadcrumb',
  data() {
    return {
      breadcrumbs: []
    }
  },
  watch: {
    $route: {
      immediate: true,
      handler(route) {
        this.getBreadcrumbs(route)
      }
    }
  },
  methods: {
    getBreadcrumbs(route) {
      // 过滤掉没有meta.title的路由
      let matched = route.matched.filter(item => item.meta && item.meta.title)
      
      // 添加首页
      if (matched.length > 0 && matched[0].path !== '/') {
        matched = [{ path: '/', meta: { title: '首页' } }].concat(matched)
      }
      
      this.breadcrumbs = matched
    }
  }
}
</script>

<style scoped>
.el-breadcrumb {
  font-size: 14px;
  line-height: 60px;
}
</style> 