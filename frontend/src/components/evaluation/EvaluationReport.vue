<template>
  <div class="evaluation-report">
    <div class="report-header">
      <h2>{{ report.task ? report.task.name + ' 评测报告' : '评测报告' }}</h2>
      <div class="report-actions">
        <el-button type="primary" size="small" @click="downloadReport" :loading="downloading">
          <i class="el-icon-download"></i> 下载报告
        </el-button>
        <el-button size="small" @click="goBack">
          <i class="el-icon-back"></i> 返回
        </el-button>
      </div>
    </div>

    <el-card v-loading="loading" class="report-card">
      <div v-if="!loading && report">
        <div class="report-summary">
          <h3>报告摘要</h3>
          <el-alert
            :title="report.summary"
            type="info"
            :closable="false"
            show-icon
          ></el-alert>
        </div>

        <div class="report-metrics">
          <h3>评测指标</h3>
          <el-row :gutter="20">
            <el-col :span="6" v-for="(detail, metric) in report.details" :key="metric">
              <el-card shadow="hover" class="metric-card">
                <div slot="header" class="metric-header">
                  {{ metric }}
                </div>
                <div class="metric-value">{{ formatValue(detail.value) }}</div>
                <div class="metric-description">{{ detail.description }}</div>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <div class="report-charts" v-if="report.charts">
          <h3>可视化图表</h3>
          <el-tabs type="border-card">
            <el-tab-pane v-for="(chart, chartName) in report.charts" :key="chartName" :label="formatChartName(chartName)">
              <div class="chart-container">
                <div :ref="'chart_' + chartName" class="chart"></div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>

        <div class="report-task-info">
          <h3>任务信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="任务名称">{{ report.task ? report.task.name : '-' }}</el-descriptions-item>
            <el-descriptions-item label="模型">{{ report.task && report.task.model ? report.task.model.name : '-' }}</el-descriptions-item>
            <el-descriptions-item label="数据集">{{ report.task && report.task.dataset ? report.task.dataset.name : '-' }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDate(report.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="创建者">{{ report.task ? report.task.created_by_username : '-' }}</el-descriptions-item>
            <el-descriptions-item label="完成时间">{{ formatDate(report.updated_at) }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="report-suggestions" v-if="report.suggestions">
          <h3>优化建议</h3>
          <el-alert
            :title="report.suggestions"
            type="success"
            :closable="false"
            show-icon
          ></el-alert>
        </div>
      </div>
      <div v-else-if="!loading && !report">
        <el-empty description="未找到评测报告"></el-empty>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import moment from 'moment'
import * as echarts from 'echarts'

export default {
  name: 'EvaluationReport',
  props: {
    id: {
      type: String,
      required: false
    },
    isFromTask: {
      type: Boolean,
      default: false
    }
  },
  
  data() {
    return {
      loading: false,
      downloading: false,
      charts: {}
    }
  },
  
  computed: {
    ...mapState('evaluationCenter', ['currentReport']),
    
    // 报告ID可以从props或路由参数中获取
    reportId() {
      return this.id || this.$route.params.id
    },
    
    report() {
      return this.currentReport
    }
  },
  
  watch: {
    reportId: {
      handler(val) {
        if (val) {
          this.fetchReport()
        }
      },
      immediate: true
    }
  },
  
  methods: {
    ...mapActions('evaluationCenter', [
      'fetchEvaluationReportDetail',
      'downloadEvaluationReport'
    ]),
    
    async fetchReport() {
      if (!this.reportId) return
      
      this.loading = true
      try {
        await this.fetchEvaluationReportDetail(this.reportId)
        this.$nextTick(() => {
          this.initCharts()
        })
      } catch (error) {
        this.$message.error('获取评测报告失败')
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    
    async downloadReport() {
      if (!this.reportId) return
      
      this.downloading = true
      try {
        await this.downloadEvaluationReport(this.reportId)
        this.$message.success('报告下载成功')
      } catch (error) {
        this.$message.error('下载评测报告失败')
        console.error(error)
      } finally {
        this.downloading = false
      }
    },
    
    initCharts() {
      if (!this.report || !this.report.charts) return
      
      // 初始化雷达图
      if (this.report.charts.metrics_radar) {
        const radarChart = echarts.init(this.$refs.metricsRadar)
        const radarOption = {
          title: {
            text: '评测指标雷达图'
          },
          tooltip: {},
          radar: {
            indicator: this.report.charts.metrics_radar.categories.map(cat => ({
              name: cat,
              max: 1
            }))
          },
          series: [{
            name: '评测指标',
            type: 'radar',
            data: [{
              value: this.report.charts.metrics_radar.values,
              name: '指标得分'
            }]
          }]
        }
        radarChart.setOption(radarOption)
        this.charts.metricsRadar = radarChart
      }
      
      // 初始化性能柱状图
      if (this.report.charts.performance_bar) {
        const barChart = echarts.init(this.$refs.performanceBar)
        const barOption = {
          title: {
            text: '性能指标'
          },
          tooltip: {},
          xAxis: {
            data: this.report.charts.performance_bar.categories
          },
          yAxis: {},
          series: [{
            name: '性能指标',
            type: 'bar',
            data: this.report.charts.performance_bar.values
          }]
        }
        barChart.setOption(barOption)
        this.charts.performanceBar = barChart
      }
    },
    
    goBack() {
      if (this.isFromTask) {
        this.$router.go(-1)
      } else {
        this.$router.push('/evaluation-center/reports')
      }
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
    
    formatChartName(name) {
      // 将snake_case转换为更易读的格式
      const formatted = name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
      
      // 特殊处理一些常见的图表名称
      const nameMap = {
        'Confusion Matrix': '混淆矩阵',
        'Roc Curve': 'ROC曲线',
        'Precision Recall Curve': '精确率-召回率曲线',
        'Feature Importance': '特征重要性',
        'Learning Curve': '学习曲线',
        'Class Distribution': '类别分布'
      }
      
      return nameMap[formatted] || formatted
    }
  },
  
  beforeDestroy() {
    // 销毁图表实例
    Object.values(this.charts).forEach(chart => {
      chart.dispose()
    })
  }
}
</script>

<style scoped>
.evaluation-report {
  padding: 20px;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.report-card {
  margin-bottom: 20px;
}

.report-summary,
.report-metrics,
.report-charts,
.report-task-info,
.report-suggestions {
  margin-bottom: 30px;
}

.metric-card {
  height: 160px;
  margin-bottom: 20px;
}

.metric-header {
  font-weight: bold;
}

.metric-value {
  font-size: 24px;
  color: #409EFF;
  margin: 10px 0;
  text-align: center;
}

.metric-description {
  font-size: 12px;
  color: #666;
}

.chart-container {
  height: 400px;
  margin: 20px 0;
}

.chart {
  width: 100%;
  height: 100%;
}
</style> 