# 评测中心组件

本目录包含评测中心相关的所有组件，用于实现模型评测和比较功能。

## 组件结构

```
evaluation/
├── EvaluationCenter.vue       # 评测中心主组件
├── EvaluationTaskList.vue     # 评测任务列表组件
├── EvaluationTaskForm.vue     # 评测任务表单组件
├── EvaluationTaskCreate.vue   # 创建评测任务组件
├── EvaluationTaskDetail.vue   # 评测任务详情组件
├── EvaluationReport.vue       # 评测报告组件
├── ModelComparison.vue        # 模型比较组件
├── README.md                  # 组件说明文档
└── CHANGELOG.md               # 变更日志
```

## 组件说明

### EvaluationCenter.vue

评测中心主组件，包含评测任务列表和创建评测任务的功能。

**功能特点：**
- 显示评测任务列表
- 支持任务筛选和搜索
- 提供创建新评测任务的入口
- 显示任务状态和进度

### EvaluationTaskList.vue

评测任务列表组件，用于展示所有评测任务。

**功能特点：**
- 分页显示评测任务
- 支持按状态、模型类型等筛选
- 提供任务操作（查看、删除、取消等）
- 显示任务进度和状态

### EvaluationTaskForm.vue

评测任务表单组件，用于创建和编辑评测任务。

**功能特点：**
- 选择评测模型
- 配置评测参数
- 选择评测数据集
- 设置评测指标

### EvaluationTaskCreate.vue

创建评测任务的组件，集成了表单和提交逻辑。

**功能特点：**
- 集成评测任务表单
- 提供表单验证
- 处理任务提交逻辑
- 显示提交结果反馈

### EvaluationTaskDetail.vue

评测任务详情组件，显示任务的详细信息和进度。

**功能特点：**
- 显示任务基本信息
- 实时更新任务进度
- 提供任务操作（取消、重试等）
- 显示评测结果预览

### EvaluationReport.vue

评测报告组件，用于展示评测结果和分析。

**功能特点：**
- 显示评测指标和得分
- 提供图表可视化
- 支持报告导出
- 显示详细的评测数据

### ModelComparison.vue

模型比较组件，用于比较多个模型的评测结果。

**功能特点：**
- 选择多个模型进行比较
- 提供多维度比较视图
- 支持雷达图、柱状图等可视化
- 显示模型优劣势分析

## 使用方法

### 评测任务列表

```vue
<template>
  <evaluation-task-list 
    :loading="loading"
    :tasks="tasks"
    @view="handleViewTask"
    @delete="handleDeleteTask"
  />
</template>

<script>
import EvaluationTaskList from '@/components/evaluation/EvaluationTaskList.vue'
import evaluationCenterApi from '@/api/evaluationCenter'

export default {
  components: {
    EvaluationTaskList
  },
  data() {
    return {
      loading: false,
      tasks: []
    }
  },
  methods: {
    async fetchTasks() {
      this.loading = true
      try {
        const response = await evaluationCenterApi.getEvaluationTasks()
        this.tasks = response.data
      } catch (error) {
        console.error('获取评测任务失败', error)
      } finally {
        this.loading = false
      }
    },
    handleViewTask(taskId) {
      this.$router.push(`/evaluation/task/${taskId}`)
    },
    handleDeleteTask(taskId) {
      // 删除任务逻辑
    }
  },
  created() {
    this.fetchTasks()
  }
}
</script>
```

### 创建评测任务

```vue
<template>
  <evaluation-task-create @submit="handleSubmit" @cancel="handleCancel" />
</template>

<script>
import EvaluationTaskCreate from '@/components/evaluation/EvaluationTaskCreate.vue'
import evaluationCenterApi from '@/api/evaluationCenter'

export default {
  components: {
    EvaluationTaskCreate
  },
  methods: {
    async handleSubmit(taskData) {
      try {
        await evaluationCenterApi.createEvaluationTask(taskData)
        this.$message.success('评测任务创建成功')
        this.$router.push('/evaluation/tasks')
      } catch (error) {
        this.$message.error('评测任务创建失败')
        console.error(error)
      }
    },
    handleCancel() {
      this.$router.push('/evaluation/tasks')
    }
  }
}
</script>
```

### 查看评测报告

```vue
<template>
  <evaluation-report :report-id="reportId" />
</template>

<script>
import EvaluationReport from '@/components/evaluation/EvaluationReport.vue'

export default {
  components: {
    EvaluationReport
  },
  props: {
    reportId: {
      type: [Number, String],
      required: true
    }
  }
}
</script>
```

## API 接口

评测中心组件使用 `@/api/evaluationCenter.js` 中定义的API接口与后端交互。主要接口包括：

- `getEvaluationTasks` - 获取评测任务列表
- `getEvaluationTaskDetail` - 获取评测任务详情
- `createEvaluationTask` - 创建评测任务
- `deleteEvaluationTask` - 删除评测任务
- `startEvaluationTask` - 开始评测任务
- `cancelEvaluationTask` - 取消评测任务
- `getEvaluationTaskReport` - 获取评测任务报告
- `getEvaluationTaskProgress` - 获取评测任务进度
- `getModelComparisons` - 获取模型比较列表
- `createModelComparison` - 创建模型比较

## 注意事项

1. 评测任务可能需要较长时间，请确保实现了任务进度的实时更新
2. 评测报告包含大量数据，建议实现懒加载和分页显示
3. 图表组件使用 ECharts，确保正确配置图表选项
4. 模型比较功能需要选择至少两个模型才能进行

## 更新日志

### 2024-03-12

- 优化评测中心组件结构，将视图组件移至views目录
- 改进路由配置，优化页面加载性能
- 添加模型对比功能，支持多模型性能对比

### 2024-03-11

- 完善评测报告组件，添加更多可视化图表
- 优化评测任务列表，添加搜索和状态筛选功能
- 改进评测任务详情页面，显示更多任务信息 