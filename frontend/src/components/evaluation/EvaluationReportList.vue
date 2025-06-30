<template>
  <div class="evaluation-report-list">
    <!-- 工具栏区域 -->
    <div class="report-toolbar">
      <div class="search-filter">
        <el-input
          v-model="searchQuery"
          placeholder="搜索报告名称或描述"
          prefix-icon="el-icon-search"
          clearable
          @clear="handleSearch"
          @input="handleSearch"
        >
        </el-input>
        
        <el-select 
          v-model="filterModel" 
          placeholder="按模型筛选" 
          clearable 
          @change="handleSearch"
          class="filter-select"
        >
          <el-option
            v-for="model in modelOptions"
            :key="model.value"
            :label="model.label"
            :value="model.value"
          >
          </el-option>
        </el-select>
        
        <el-select 
          v-model="filterStatus" 
          placeholder="按状态筛选" 
          clearable 
          @change="handleSearch"
          class="filter-select"
        >
          <el-option
            v-for="status in statusOptions"
            :key="status.value"
            :label="status.label"
            :value="status.value"
          >
          </el-option>
        </el-select>
        
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="yyyy-MM-dd"
          @change="handleSearch"
          class="date-picker"
        >
        </el-date-picker>
      </div>
      
      <div class="action-buttons">
        <el-button type="primary" icon="el-icon-plus" @click="navigateToCreateTask">
          创建新评测
        </el-button>
      </div>
    </div>
    
    <!-- 报告列表区域 -->
    <el-table
      v-loading="loading"
      :data="filteredReports"
      style="width: 100%"
      border
      highlight-current-row
      @row-click="handleRowClick"
    >
      <el-table-column prop="name" label="报告名称" min-width="180">
        <template slot-scope="scope">
          <div class="report-name">
            <el-badge v-if="scope.row.is_new" is-dot class="report-badge">
              <span>{{ scope.row.name }}</span>
            </el-badge>
            <span v-else>{{ scope.row.name }}</span>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="model_name" label="评测模型" min-width="150">
      </el-table-column>
      
      <el-table-column prop="dataset_name" label="评测数据集" min-width="150">
      </el-table-column>
      
      <el-table-column prop="metrics" label="关键指标" min-width="250">
        <template slot-scope="scope">
          <div class="metrics-list">
            <el-tag v-for="(value, key) in scope.row.key_metrics" :key="key" size="small" class="metric-tag">
              {{ key }}: {{ formatValue(value) }}
            </el-tag>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="status" label="状态" width="100">
        <template slot-scope="scope">
          <el-tag :type="getStatusType(scope.row.status)" size="medium">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="180" fixed="right">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            icon="el-icon-view"
            @click.stop="viewReport(scope.row)"
          >
            查看
          </el-button>
          
          <el-button
            size="mini"
            type="success"
            icon="el-icon-download"
            @click.stop="downloadReport(scope.row.id)"
            :disabled="scope.row.status !== 'completed'"
          >
            下载
          </el-button>
          
          <el-button
            size="mini"
            type="danger"
            icon="el-icon-delete"
            @click.stop="confirmDelete(scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页控件 -->
    <div class="pagination-container">
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalReports"
      >
      </el-pagination>
    </div>
    
    <!-- 删除确认对话框 -->
    <el-dialog
      title="确认删除"
      :visible.sync="deleteDialogVisible"
      width="30%"
    >
      <span>确定要删除报告 "{{ reportToDelete ? reportToDelete.name : '' }}" 吗？此操作无法撤销。</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="deleteReport">确定删除</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import moment from 'moment'

export default {
  name: 'EvaluationReportList',
  data() {
    return {
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      modelOptions: [],
      filterModel: '',
      filterStatus: '',
      dateRange: null,
      deleteDialogVisible: false,
      reportToDelete: null,
      statusOptions: [
        { value: 'pending', label: '等待中' },
        { value: 'running', label: '生成中' },
        { value: 'completed', label: '已完成' },
        { value: 'failed', label: '失败' }
      ]
    }
  },
  computed: {
    ...mapState('evaluationCenter', [
      'reports',
      'models',
      'loading'
    ]),
    
    filteredReports() {
      let result = [...this.reports]
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(report => 
          report.name.toLowerCase().includes(query) || 
          report.description.toLowerCase().includes(query)
        )
      }
      
      if (this.filterModel) {
        result = result.filter(report => report.model_id === this.filterModel)
      }
      
      if (this.filterStatus) {
        result = result.filter(report => report.status === this.filterStatus)
      }
      
      if (this.dateRange && this.dateRange.length === 2) {
        const startDate = moment(this.dateRange[0]).startOf('day')
        const endDate = moment(this.dateRange[1]).endOf('day')
        
        result = result.filter(report => {
          const reportDate = moment(report.created_at)
          return reportDate.isBetween(startDate, endDate, null, '[]')
        })
      }
      
      return result
    },
    
    totalReports() {
      return this.filteredReports.length
    }
  },
  created() {
    this.initialize()
  },
  methods: {
    ...mapActions('evaluationCenter', [
      'fetchReports',
      'fetchModels'
    ]),
    
    async initialize() {
      try {
        await Promise.all([
          this.fetchReportList(),
          this.fetchModelOptions()
        ])
      } catch (error) {
        console.error('初始化数据失败:', error)
      }
    },
    
    async fetchReportList() {
      try {
        await this.fetchReports({
          page: this.currentPage,
          page_size: this.pageSize,
          search: this.searchQuery,
          model: this.filterModel,
          status: this.filterStatus,
          start_date: this.dateRange?.[0],
          end_date: this.dateRange?.[1]
        })
      } catch (error) {
        this.$message.error('获取评测报告列表失败')
        console.error(error)
      }
    },
    
    async fetchModelOptions() {
      try {
        await this.fetchModels()
        this.modelOptions = this.models.map(model => ({
          value: model.id,
          label: model.name
        }))
      } catch (error) {
        this.$message.error('获取模型列表失败')
        console.error(error)
      }
    },
    
    handlePageChange(page) {
      this.currentPage = page
      this.fetchReportList()
    },
    
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
      this.fetchReportList()
    },
    
    handleSearch() {
      this.currentPage = 1
      this.fetchReportList()
    },
    
    viewReport(report) {
      this.$router.push(`/evaluation-center/reports/${report.id}`)
    },
    
    async downloadReport(id) {
      try {
        const response = await this.$api.evaluationCenter.reports.download(id)
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `report-${id}.pdf`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      } catch (error) {
        this.$message.error('下载报告失败：' + error.message)
      }
    },
    
    confirmDelete(report) {
      this.reportToDelete = report
      this.deleteDialogVisible = true
    },
    
    async deleteReport() {
      if (!this.reportToDelete) return
      
      try {
        await this.$store.dispatch('evaluationCenter/deleteReport', this.reportToDelete.id)
        this.$message.success('报告删除成功')
        this.deleteDialogVisible = false
        this.fetchReportList()
      } catch (error) {
        this.$message.error('删除报告失败：' + error.message)
      }
    },
    
    navigateToCreateTask() {
      this.$router.push('/evaluation-center/tasks/create')
    },
    
    formatValue(value) {
      if (typeof value === 'number') {
        return value.toFixed(4)
      }
      return value
    },
    
    formatDate(date) {
      if (!date) return '-'
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    
    getStatusType(status) {
      const statusMap = {
        'pending': 'info',
        'running': 'warning',
        'completed': 'success',
        'failed': 'danger'
      }
      return statusMap[status] || 'info'
    },
    
    getStatusText(status) {
      const statusMap = {
        'pending': '等待中',
        'running': '生成中',
        'completed': '已完成',
        'failed': '失败'
      }
      return statusMap[status] || status
    },
    
    handleRowClick(row) {
      this.viewReport(row)
    }
  }
}
</script>

<style scoped>
.evaluation-report-list {
  padding: 20px;
}

.report-toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  max-width: 80%;
}

.filter-select {
  width: 160px;
}

.date-picker {
  width: 260px;
}

.metrics-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.metric-tag {
  margin-right: 5px;
}

.report-name {
  font-weight: 500;
}

.report-badge >>> .el-badge__content {
  background-color: #409EFF;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 