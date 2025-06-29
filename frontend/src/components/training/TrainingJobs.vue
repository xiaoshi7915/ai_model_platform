<template>
  <div class="training-jobs">
    <training-job-list
      @view-model="handleViewModel"
    ></training-job-list>
  </div>
</template>

<script>
import TrainingJobList from './TrainingJobList.vue'

export default {
  name: 'TrainingJobs',
  components: {
    TrainingJobList
  },
  methods: {
    // 处理查看模型
    handleViewModel(modelId) {
      this.$router.push({
        path: '/training-center/models',
        query: { view: 'detail', modelId }
      })
    }
  }
}
</script>

<style scoped>
.training-jobs {
  padding: 20px;
}
</style> 