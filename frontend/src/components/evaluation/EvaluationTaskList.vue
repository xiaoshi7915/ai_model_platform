<template>
  <div class="evaluation-task-list">
    <!-- 搜索和过滤区域 -->
    <div class="table-actions">
      <el-input
        v-model="searchQuery"
        placeholder="搜索任务名称"
        class="search-input"
        clearable
        @clear="handleSearch"
        @input="handleSearch"
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      
      <el-select v-model="statusFilter" placeholder="状态过滤" @change="handleFilter" clearable>
        <el-option
          v-for="item in statusOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
      
      <el-button type="primary" @click="handleCreate">
        <i class="el-icon-plus"></i> 创建评测任务
      </el-button>
    </div>

    <!-- 评测任务列表表格 -->
    <el-table
      v-loading="loading"
      :data="filteredTasks"
      border
      style="width: 100%"
    >
      <el-table-column prop="name" label="任务名称" min-width="150">
        <template slot-scope="scope">
          <el-link type="primary" @click="handleDetail(scope.row)">{{ scope.row.name }}</el-link>
        </template>
      </el-table-column>
      
      <el-table-column prop="model_name" label="评测模型" min-width="150">
        <template slot-scope="scope">
          {{ scope.row.model_name }} ({{ scope.row.model_version }})
        </template>
      </el-table-column>
      
      <el-table-column prop="dataset_name" label="评测数据集" min-width="150"></el-table-column>
      
      <el-table-column prop="status" label="状态" width="100">
        <template slot-scope="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="250" fixed="right">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            @click="handleStart(scope.row)"
            v-if="scope.row.status === 'pending'"
          >开始评测</el-button>
          
          <el-button
            size="mini"
            type="warning"
            @click="handleCancel(scope.row)"
            v-if="scope.row.status === 'running'"
          >取消评测</el-button>
          
          <el-button
            size="mini"
            type="success"
            @click="handleViewReport(scope.row)"
            v-if="scope.row.status === 'completed'"
          >查看报告</el-button>
          
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.row)"
            :disabled="scope.row.status === 'running'"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页器 -->
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalTasks"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import moment from 'moment'

export default {
  name: 'EvaluationTaskList',
  data() {
    return {
      searchQuery: '',
      statusFilter: '',
      currentPage: 1,
      pageSize: 10,
      selectedTask: null,
      deleteDialogVisible: false,
      statusOptions: [
        { value: 'pending', label: '等待中' },
        { value: 'running', label: '运行中' },
        { value: 'completed', label: '已完成' },
        { value: 'failed', label: '失败' },
        { value: 'cancelled', label: '已取消' }
      ]
    }
  },
  computed: {
    ...mapState('evaluationCenter', [
      'evaluationTasks',
      'loading'
    ]),
    
    filteredTasks() {
      let result = [...this.evaluationTasks]
      
      // 搜索过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(task => 
          task.name.toLowerCase().includes(query) ||
          task.description.toLowerCase().includes(query)
        )
      }
      
      // 状态过滤
      if (this.statusFilter) {
        result = result.filter(task => task.status === this.statusFilter)
      }
      
      return result
    },
    
    totalTasks() {
      return this.$store.state.evaluationCenter.pagination.total || 0
    }
  },
  methods: {
    ...mapActions('evaluationCenter', [
      'fetchEvaluationTasks',
      'startEvaluationTask',
      'cancelEvaluationTask',
      'deleteEvaluationTask',
      'setPagination'
    ]),
    
    async fetchTasks() {
      try {
        await this.fetchEvaluationTasks({
          page: this.currentPage,
          pageSize: this.pageSize,
          search: this.searchQuery,
          status: this.statusFilter
        })
      } catch (error) {
        this.$message.error('获取评测任务列表失败')
        console.error(error)
      }
    },
    
    // 处理搜索
    handleSearch() {
      this.currentPage = 1
      this.fetchTasks()
    },
    
    // 处理过滤
    handleFilter() {
      this.currentPage = 1
      this.fetchTasks()
    },
    
    // 处理页码变化
    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchTasks()
    },
    
    // 处理每页数量变化
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
      this.fetchTasks()
    },
    
    // 处理开始评测任务
    async handleStartEvaluationTask(task) {
      try {
        await this.startEvaluationTask(task.id)
        this.$message.success('开始评测任务成功')
        this.fetchTasks()
      } catch (error) {
        this.$message.error('开始评测任务失败')
        console.error(error)
      }
    },
    
    // 处理取消评测任务
    async handleCancelEvaluationTask(task) {
      try {
        await this.cancelEvaluationTask(task.id)
        this.$message.success('取消评测任务成功')
        this.fetchTasks()
      } catch (error) {
        this.$message.error('取消评测任务失败')
        console.error(error)
      }
    },
    
    // 处理删除评测任务
    async handleDeleteEvaluationTask(task) {
      try {
        await this.deleteEvaluationTask(task.id)
        this.$message.success('删除评测任务成功')
        this.fetchTasks()
      } catch (error) {
        this.$message.error('删除评测任务失败')
        console.error(error)
      }
    },
    
    // 处理查看评测报告
    handleViewEvaluationReport(task) {
      if (task.report_id) {
        this.$router.push(`/evaluation-center/reports/${task.report_id}`)
      }
    },
    
    // 获取状态类型
    getStatusType(status) {
      const types = {
        pending: 'info',
        running: 'warning',
        completed: 'success',
        failed: 'danger',
        cancelled: 'info'
      }
      return types[status] || 'info'
    },
    
    // 获取状态文本
    getStatusText(status) {
      const texts = {
        pending: '等待中',
        running: '运行中',
        completed: '已完成',
        failed: '失败',
        cancelled: '已取消'
      }
      return texts[status] || status
    },
    
    // 格式化日期
    formatDate(date) {
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    
    // 处理创建评测任务
    handleCreate() {
      this.$emit('create')
    },
    
    // 处理查看评测任务详情
    handleViewEvaluationTaskDetail(task) {
      this.$emit('detail', task)
    },
    
    // 处理查看详情
    handleDetail(task) {
      this.$router.push(`/evaluation-center/task/${task.id}`);
    },
    
    // 处理开始评测
    handleStart(task) {
      this.$confirm('确定要开始评测任务吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        this.$emit('start', task)
      }).catch(() => {})
    },
    
    // 处理取消评测
    handleCancel(task) {
      this.$confirm('确定要取消评测任务吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('cancel', task)
      }).catch(() => {})
    },
    
    // 处理查看报告
    handleViewReport(task) {
      this.$emit('view-report', task)
    },
    
    // 处理删除评测任务
    handleDelete(task) {
      this.$confirm('此操作将永久删除该评测任务, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', task)
      }).catch(() => {})
    }
  },
  created() {
    this.fetchTasks()
  }
}
</script>

<style scoped>
.evaluation-task-list {
  padding: 20px;
}

.table-actions {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-input {
  width: 200px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 