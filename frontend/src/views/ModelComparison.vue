<template>
  <div class="model-comparison-view">
    <model-comparison />
  </div>
</template>

<script>
import ModelComparison from '@/components/evaluation/ModelComparison.vue'

export default {
  name: 'ModelComparisonView',
  components: {
    ModelComparison
  }
}
</script>

<style scoped>
.model-comparison-view {
  height: 100%;
}
</style> 