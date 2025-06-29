<template>
  <div class="training-center-container">
    <training-center-view />
  </div>
</template>

<script>
import TrainingCenterView from './training/TrainingCenter.vue'

export default {
  name: 'TrainingCenter',
  components: {
    TrainingCenterView
  }
}
</script>

<style scoped>
.training-center-container {
  height: 100%;
}
</style> 