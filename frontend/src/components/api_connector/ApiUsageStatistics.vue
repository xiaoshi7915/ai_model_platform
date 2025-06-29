<template>
  <div class="api-usage-statistics">
    <el-card>
      <div slot="header" class="card-header">
        <span>API使用统计</span>
        <div class="header-actions">
          <el-button 
            size="small" 
            type="primary" 
            icon="el-icon-refresh" 
            @click="refreshStats"
            :loading="loading"
          >刷新</el-button>
        </div>
      </div>
      
      <!-- 日期选择 -->
      <div class="date-filter">
        <el-radio-group v-model="dateRange" @change="loadStatistics" size="small">
          <el-radio-button label="today">今天</el-radio-button>
          <el-radio-button label="week">本周</el-radio-button>
          <el-radio-button label="month">本月</el-radio-button>
          <el-radio-button label="custom">自定义</el-radio-button>
        </el-radio-group>
        
        <el-date-picker
          v-if="dateRange === 'custom'"
          v-model="customDateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="yyyy-MM-dd"
          value-format="yyyy-MM-dd"
          @change="loadStatistics"
          size="small"
          style="margin-left: 10px; width: 260px;"
        ></el-date-picker>
      </div>
      
      <!-- 统计卡片 -->
      <el-row :gutter="20" class="stat-cards">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-value">{{ formatNumber(totalRequests) }}</div>
            <div class="stat-label">总请求数</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card success-card">
            <div class="stat-value">{{ formatNumber(successRequests) }}</div>
            <div class="stat-label">成功请求</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card error-card">
            <div class="stat-value">{{ formatNumber(failedRequests) }}</div>
            <div class="stat-label">失败请求</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card token-card">
            <div class="stat-value">{{ formatNumber(totalTokens) }}</div>
            <div class="stat-label">总Token消耗</div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 图表区域 -->
      <div class="charts-area" v-loading="loading">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="chart-container">
              <h3>请求统计</h3>
              <div ref="requestsChart" class="chart"></div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chart-container">
              <h3>请求状态分布</h3>
              <div ref="statusChart" class="chart"></div>
            </div>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :span="12">
            <div class="chart-container">
              <h3>提供商使用情况</h3>
              <div ref="providerChart" class="chart"></div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chart-container">
              <h3>Token消耗趋势</h3>
              <div ref="tokenChart" class="chart"></div>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <!-- 提供商统计表格 -->
      <div class="provider-table" style="margin-top: 30px;">
        <h3>提供商详细统计</h3>
        <el-table :data="providerStats" border style="width: 100%">
          <el-table-column prop="provider" label="提供商"></el-table-column>
          <el-table-column prop="requests" label="请求总数"></el-table-column>
          <el-table-column prop="success_rate" label="成功率">
            <template slot-scope="scope">
              {{ (scope.row.success_rate * 100).toFixed(2) }}%
            </template>
          </el-table-column>
          <el-table-column prop="tokens" label="Token消耗"></el-table-column>
          <el-table-column prop="avg_response_time" label="平均响应时间(ms)">
            <template slot-scope="scope">
              {{ scope.row.avg_response_time.toFixed(2) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'
import * as echarts from 'echarts'
import api from '@/api'

export default {
  name: 'ApiUsageStatistics',
  data() {
    return {
      loading: false,
      dateRange: 'week',
      customDateRange: [],
      totalRequests: 0,
      successRequests: 0,
      failedRequests: 0,
      totalTokens: 0,
      providerStats: [],
      dailyStats: [],
      charts: {
        requestsChart: null,
        statusChart: null,
        providerChart: null,
        tokenChart: null
      }
    }
  },
  created() {
    this.loadStatistics()
  },
  mounted() {
    // 窗口大小变化时重绘图表
    window.addEventListener('resize', this.resizeCharts)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeCharts)
    // 销毁所有图表实例
    Object.values(this.charts).forEach(chart => {
      if (chart) {
        chart.dispose()
      }
    })
  },
  methods: {
    async loadStatistics() {
      this.loading = true
      try {
        let params = { period: this.dateRange }
        if (this.dateRange === 'custom' && this.customDateRange && this.customDateRange.length === 2) {
          params.start_date = this.customDateRange[0]
          params.end_date = this.customDateRange[1]
        }
        
        const response = await api.apiConnector.getStatistics(params)
        const data = response
        
        // 更新统计数据
        this.totalRequests = data.total_requests || 0
        this.successRequests = data.success_requests || 0
        this.failedRequests = data.failed_requests || 0
        this.totalTokens = data.total_tokens || 0
        this.providerStats = data.provider_stats || []
        this.dailyStats = data.daily_stats || []
        
        // 初始化图表
        this.$nextTick(() => {
          this.initCharts(data)
        })
      } catch (error) {
        console.error('加载API使用统计失败:', error)
        this.$message.error('加载API使用统计失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
      } finally {
        this.loading = false
      }
    },
    
    refreshStats() {
      this.loadStatistics()
    },
    
    initCharts(data) {
      this.initRequestsChart(data.daily_stats)
      this.initStatusChart(data)
      this.initProviderChart(data.provider_stats)
      this.initTokenChart(data.daily_stats)
    },
    
    initRequestsChart(dailyStats) {
      const chartDom = this.$refs.requestsChart
      if (!chartDom) return
      
      this.charts.requestsChart = echarts.init(chartDom)
      
      const dates = dailyStats.map(item => item.date)
      const requests = dailyStats.map(item => item.requests)
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: dates,
          axisLabel: {
            rotate: 30
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '请求数',
            type: 'bar',
            data: requests,
            itemStyle: {
              color: '#409EFF'
            }
          }
        ]
      }
      
      this.charts.requestsChart.setOption(option)
    },
    
    initStatusChart(data) {
      const chartDom = this.$refs.statusChart
      if (!chartDom) return
      
      this.charts.statusChart = echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          right: 10,
          top: 'center',
          data: ['成功', '失败', '速率限制', '错误']
        },
        series: [
          {
            name: '请求状态',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '15',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: data.success_requests || 0, name: '成功', itemStyle: { color: '#67C23A' } },
              { value: data.failed_requests || 0, name: '失败', itemStyle: { color: '#F56C6C' } },
              { value: data.rate_limited_requests || 0, name: '速率限制', itemStyle: { color: '#E6A23C' } },
              { value: data.error_requests || 0, name: '错误', itemStyle: { color: '#909399' } }
            ]
          }
        ]
      }
      
      this.charts.statusChart.setOption(option)
    },
    
    initProviderChart(providerStats) {
      const chartDom = this.$refs.providerChart
      if (!chartDom) return
      
      this.charts.providerChart = echarts.init(chartDom)
      
      const providers = providerStats.map(item => item.provider)
      const requests = providerStats.map(item => item.requests)
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          right: 10,
          top: 'center',
          data: providers
        },
        series: [
          {
            name: '提供商使用',
            type: 'pie',
            radius: '55%',
            center: ['40%', '50%'],
            data: providerStats.map(item => ({
              name: item.provider,
              value: item.requests
            })),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      
      this.charts.providerChart.setOption(option)
    },
    
    initTokenChart(dailyStats) {
      const chartDom = this.$refs.tokenChart
      if (!chartDom) return
      
      this.charts.tokenChart = echarts.init(chartDom)
      
      const dates = dailyStats.map(item => item.date)
      const tokens = dailyStats.map(item => item.tokens)
      
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: dates,
          axisLabel: {
            rotate: 30
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'Token消耗',
            type: 'line',
            data: tokens,
            markPoint: {
              data: [
                { type: 'max', name: '最大值' },
                { type: 'min', name: '最小值' }
              ]
            },
            itemStyle: {
              color: '#67C23A'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(103, 194, 58, 0.5)' },
                { offset: 1, color: 'rgba(103, 194, 58, 0.1)' }
              ])
            }
          }
        ]
      }
      
      this.charts.tokenChart.setOption(option)
    },
    
    resizeCharts() {
      Object.values(this.charts).forEach(chart => {
        if (chart) {
          chart.resize()
        }
      })
    },
    
    formatNumber(num) {
      if (num === null || num === undefined) return 0
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    }
  }
}
</script>

<style scoped>
.api-usage-statistics {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.date-filter {
  margin-bottom: 20px;
}

.stat-cards {
  margin-top: 20px;
  margin-bottom: 30px;
}

.stat-card {
  text-align: center;
  border-radius: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.success-card .stat-value {
  color: #67C23A;
}

.error-card .stat-value {
  color: #F56C6C;
}

.token-card .stat-value {
  color: #E6A23C;
}

.charts-area {
  margin-top: 30px;
}

.chart-container {
  background-color: #fff;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #ebeef5;
}

.chart-container h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: normal;
  color: #606266;
}

.chart {
  height: 300px;
}
</style> 