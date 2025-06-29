<template>
  <div class="api-logs-viewer">
    <el-card>
      <div slot="header" class="card-header">
        <span>API请求日志</span>
        <div class="header-actions">
          <el-button 
            size="small" 
            type="primary" 
            icon="el-icon-refresh" 
            @click="refreshLogs"
            :loading="loading"
          >刷新</el-button>
        </div>
      </div>
      
      <!-- 筛选条件 -->
      <el-form :inline="true" :model="filterForm" class="filter-form" size="small">
        <el-form-item label="API提供商">
          <el-select v-model="filterForm.provider" placeholder="全部" clearable style="width: 130px;">
            <el-option
              v-for="item in providers"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="请求模型">
          <el-input v-model="filterForm.model" placeholder="模型名称" clearable style="width: 120px;"></el-input>
        </el-form-item>
        
        <el-form-item label="状态码">
          <el-select v-model="filterForm.status_code" placeholder="全部" clearable style="width: 100px;">
            <el-option-group label="成功">
              <el-option label="200 OK" value="200"></el-option>
              <el-option label="201 Created" value="201"></el-option>
              <el-option label="204 No Content" value="204"></el-option>
            </el-option-group>
            <el-option-group label="客户端错误">
              <el-option label="400 Bad Request" value="400"></el-option>
              <el-option label="401 Unauthorized" value="401"></el-option>
              <el-option label="403 Forbidden" value="403"></el-option>
              <el-option label="404 Not Found" value="404"></el-option>
              <el-option label="429 Too Many Requests" value="429"></el-option>
            </el-option-group>
            <el-option-group label="服务器错误">
              <el-option label="500 Internal Server Error" value="500"></el-option>
              <el-option label="502 Bad Gateway" value="502"></el-option>
              <el-option label="503 Service Unavailable" value="503"></el-option>
              <el-option label="504 Gateway Timeout" value="504"></el-option>
            </el-option-group>
          </el-select>
        </el-form-item>
        
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="filterForm.date_range"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd HH:mm:ss"
            :picker-options="pickerOptions"
            style="width: 360px;">
          </el-date-picker>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="searchLogs">查询</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 数据表格 -->
      <el-table
        :data="logsList"
        style="width: 100%"
        v-loading="loading"
        border
        stripe
        :default-sort="{ prop: 'request_time', order: 'descending' }"
      >
        <el-table-column
          prop="id"
          label="ID"
          width="80"
          sortable>
        </el-table-column>
        
        <el-table-column
          prop="request_time"
          label="请求时间"
          width="160"
          sortable>
          <template slot-scope="scope">
            {{ formatDate(scope.row.request_time) }}
          </template>
        </el-table-column>
        
        <el-table-column
          prop="provider"
          label="提供商"
          width="100">
          <template slot-scope="scope">
            <el-tag size="small" :type="getProviderTagType(scope.row.provider)">
              {{ scope.row.provider }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="model"
          label="模型"
          width="120">
        </el-table-column>
        
        <el-table-column
          prop="endpoint"
          label="API端点"
          width="150">
        </el-table-column>
        
        <el-table-column
          prop="request_method"
          label="方法"
          width="80">
          <template slot-scope="scope">
            <el-tag size="small" :type="getMethodTagType(scope.row.request_method)">
              {{ scope.row.request_method }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="status_code"
          label="状态码"
          width="90"
          sortable>
          <template slot-scope="scope">
            <el-tag size="small" :type="getStatusTagType(scope.row.status_code)">
              {{ scope.row.status_code }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="response_time_ms"
          label="响应时间(ms)"
          width="120"
          sortable>
        </el-table-column>
        
        <el-table-column
          prop="token_usage"
          label="Token用量"
          width="120">
          <template slot-scope="scope">
            <div v-if="scope.row.token_usage">
              {{ getTotalTokens(scope.row.token_usage) }}
            </div>
            <div v-else>-</div>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="cost"
          label="费用($)"
          width="100"
          sortable>
          <template slot-scope="scope">
            <span v-if="scope.row.cost !== null">{{ formatCost(scope.row.cost) }}</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        
        <el-table-column
          label="操作"
          fixed="right"
          width="100">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="text"
              @click="viewLogDetail(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
      
      <!-- 日志详情弹窗 -->
      <el-dialog
        title="API日志详情"
        :visible.sync="dialogVisible"
        width="70%"
        class="log-detail-dialog"
      >
        <template v-if="currentLog">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="请求ID">{{ currentLog.id }}</el-descriptions-item>
            <el-descriptions-item label="请求时间">{{ formatDate(currentLog.request_time) }}</el-descriptions-item>
            <el-descriptions-item label="提供商">{{ currentLog.provider }}</el-descriptions-item>
            <el-descriptions-item label="模型">{{ currentLog.model }}</el-descriptions-item>
            <el-descriptions-item label="API端点">{{ currentLog.endpoint }}</el-descriptions-item>
            <el-descriptions-item label="请求方法">{{ currentLog.request_method }}</el-descriptions-item>
            <el-descriptions-item label="状态码">{{ currentLog.status_code }}</el-descriptions-item>
            <el-descriptions-item label="响应时间">{{ currentLog.response_time_ms }} ms</el-descriptions-item>
            <el-descriptions-item label="Token用量" :span="2">
              <div v-if="currentLog.token_usage">
                <p>输入: {{ currentLog.token_usage.prompt_tokens || 0 }} | 
                   输出: {{ currentLog.token_usage.completion_tokens || 0 }} | 
                   总计: {{ getTotalTokens(currentLog.token_usage) }}</p>
              </div>
              <div v-else>无Token信息</div>
            </el-descriptions-item>
            <el-descriptions-item label="估算费用">{{ formatCost(currentLog.cost) }} $</el-descriptions-item>
            <el-descriptions-item label="用户ID">{{ currentLog.user_id || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="错误信息" :span="2" v-if="currentLog.error">
              <div class="error-message">{{ currentLog.error }}</div>
            </el-descriptions-item>
          </el-descriptions>
          
          <el-tabs v-model="activeTab" class="detail-tabs">
            <el-tab-pane label="请求参数" name="request">
              <pre class="code-block"><code>{{ formatJSON(currentLog.request_data) }}</code></pre>
            </el-tab-pane>
            <el-tab-pane label="响应内容" name="response">
              <pre class="code-block"><code>{{ formatJSON(currentLog.response_data) }}</code></pre>
            </el-tab-pane>
            <el-tab-pane label="请求头" name="headers">
              <pre class="code-block"><code>{{ formatJSON(currentLog.request_headers) }}</code></pre>
            </el-tab-pane>
          </el-tabs>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'
import api from '@/api'

export default {
  name: 'ApiLogsViewer',
  data() {
    return {
      loading: false,
      logsList: [],
      providers: [],
      filterForm: {
        provider: '',
        model: '',
        status_code: '',
        date_range: null
      },
      pagination: {
        currentPage: 1,
        pageSize: 20,
        total: 0
      },
      pickerOptions: {
        shortcuts: [
          {
            text: '最近一小时',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '今天',
            onClick(picker) {
              const end = new Date()
              const start = new Date(new Date().toDateString())
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近三天',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 3)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近一周',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
              picker.$emit('pick', [start, end])
            }
          }
        ]
      },
      dialogVisible: false,
      currentLog: null,
      activeTab: 'request'
    }
  },
  created() {
    this.loadProviders()
    this.loadLogs()
  },
  methods: {
    // 加载API提供商列表
    async loadProviders() {
      try {
        const response = await api.apiConnector.getProviders()
        this.providers = response.map(provider => {
          return {
            label: provider.name,
            value: provider.code
          }
        })
      } catch (error) {
        console.error('加载API提供商失败:', error)
        this.$message.error('加载API提供商失败')
      }
    },
    
    // 加载日志列表
    async loadLogs() {
      this.loading = true
      try {
        let params = {
          page: this.pagination.currentPage,
          page_size: this.pagination.pageSize
        }
        
        // 添加筛选条件
        if (this.filterForm.provider) {
          params.provider = this.filterForm.provider
        }
        if (this.filterForm.model) {
          params.model = this.filterForm.model
        }
        if (this.filterForm.status_code) {
          params.status_code = this.filterForm.status_code
        }
        if (this.filterForm.date_range && this.filterForm.date_range.length === 2) {
          params.start_time = this.filterForm.date_range[0]
          params.end_time = this.filterForm.date_range[1]
        }
        
        const response = await api.apiConnector.getLogs(params)
        this.logsList = response.results
        this.pagination.total = response.count
      } catch (error) {
        console.error('加载日志失败:', error)
        this.$message.error('加载日志失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
      } finally {
        this.loading = false
      }
    },
    
    // 刷新日志
    refreshLogs() {
      this.loadLogs()
    },
    
    // 搜索日志
    searchLogs() {
      this.pagination.currentPage = 1
      this.loadLogs()
    },
    
    // 重置筛选条件
    resetFilters() {
      this.filterForm = {
        provider: '',
        model: '',
        status_code: '',
        date_range: null
      }
      this.searchLogs()
    },
    
    // 处理页码变化
    handleCurrentChange(page) {
      this.pagination.currentPage = page
      this.loadLogs()
    },
    
    // 处理每页条数变化
    handleSizeChange(size) {
      this.pagination.pageSize = size
      this.loadLogs()
    },
    
    // 查看日志详情
    async viewLogDetail(log) {
      try {
        const response = await axios.get(`/api/api-connector/logs/${log.id}/`)
        this.currentLog = response.data
        this.dialogVisible = true
      } catch (error) {
        console.error('获取日志详情失败:', error)
        this.$message.error('获取日志详情失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
      }
    },
    
    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleString()
    },
    
    // 获取提供商标签类型
    getProviderTagType(provider) {
      const providerColors = {
        'openai': 'success',
        'azure': 'primary',
        'anthropic': 'warning',
        'google': 'danger',
        'cohere': 'info'
      }
      return providerColors[provider] || ''
    },
    
    // 获取请求方法标签类型
    getMethodTagType(method) {
      const methodColors = {
        'GET': '',
        'POST': 'success',
        'PUT': 'warning',
        'DELETE': 'danger'
      }
      return methodColors[method] || ''
    },
    
    // 获取状态码标签类型
    getStatusTagType(statusCode) {
      if (statusCode < 300) return 'success'
      if (statusCode < 400) return ''
      if (statusCode < 500) return 'warning'
      return 'danger'
    },
    
    // 获取总Token数
    getTotalTokens(tokenUsage) {
      if (!tokenUsage) return 0
      const promptTokens = tokenUsage.prompt_tokens || 0
      const completionTokens = tokenUsage.completion_tokens || 0
      return promptTokens + completionTokens
    },
    
    // 格式化费用
    formatCost(cost) {
      if (cost === null || cost === undefined) return '-'
      return cost.toFixed(6)
    },
    
    // 格式化JSON
    formatJSON(data) {
      if (!data) return '{}'
      try {
        const jsonString = typeof data === 'string' ? data : JSON.stringify(data, null, 2)
        return jsonString
      } catch (e) {
        return String(data)
      }
    }
  }
}
</script>

<style scoped>
.api-logs-viewer {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-form {
  margin-bottom: 20px;
}

.pagination-container {
  text-align: right;
  margin-top: 20px;
}

.log-detail-dialog .el-dialog__body {
  padding: 20px;
}

.detail-tabs {
  margin-top: 20px;
}

.code-block {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  overflow: auto;
  max-height: 300px;
  font-family: monospace;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
}

.error-message {
  color: #f56c6c;
  font-size: 14px;
}
</style> 