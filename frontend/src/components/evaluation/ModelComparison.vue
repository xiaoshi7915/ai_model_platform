<template>
  <div class="model-comparison">
    <div class="page-header">
      <h2>模型比较</h2>
      <el-button type="primary" @click="showCreateForm">创建模型比较</el-button>
    </div>

    <!-- 比较列表 -->
    <el-table
      v-loading="loading"
      :data="comparisons"
      stripe
      border
      style="width: 100%"
    >
      <el-table-column prop="name" label="比较名称" min-width="150"></el-table-column>
      <el-table-column prop="description" label="描述" min-width="200"></el-table-column>
      <el-table-column label="包含模型数量" min-width="120">
        <template slot-scope="scope">
          {{ scope.row.model_list ? scope.row.model_list.length : 0 }}
        </template>
      </el-table-column>
      <el-table-column prop="dataset.name" label="使用数据集" min-width="150"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" min-width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template slot-scope="scope">
          <el-button size="mini" @click="viewComparison(scope.row)">查看</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
    </div>

    <!-- 创建比较对话框 -->
    <el-dialog title="创建模型比较" :visible.sync="dialogVisible" width="50%">
      <el-form ref="form" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="比较名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入比较名称"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            type="textarea"
            v-model="form.description"
            placeholder="请输入比较描述"
            :rows="3"
          ></el-input>
        </el-form-item>
        <el-form-item label="选择数据集" prop="dataset">
          <el-select v-model="form.dataset" placeholder="请选择数据集" style="width: 100%">
            <el-option
              v-for="dataset in datasets"
              :key="dataset.id"
              :label="dataset.name"
              :value="dataset.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择模型" prop="model_list">
          <el-transfer
            v-model="form.model_list"
            :data="availableModels"
            :titles="['可用模型', '已选模型']"
            :button-texts="['移除', '添加']"
            :props="{
              key: 'id',
              label: 'name'
            }"
          ></el-transfer>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createComparison" :loading="submitting">创建</el-button>
      </span>
    </el-dialog>

    <!-- 查看比较详情对话框 -->
    <el-dialog title="模型比较详情" :visible.sync="detailVisible" width="70%" fullscreen>
      <div v-if="currentComparison" class="comparison-detail">
        <div class="info-section">
          <h3>基本信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="比较名称">{{ currentComparison.name }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDate(currentComparison.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="创建者">{{ currentComparison.created_by_username }}</el-descriptions-item>
            <el-descriptions-item label="数据集">{{ currentComparison.dataset ? currentComparison.dataset.name : '未指定' }}</el-descriptions-item>
            <el-descriptions-item label="描述" :span="2">{{ currentComparison.description }}</el-descriptions-item>
          </el-descriptions>
        </div>
        
        <div class="results-section">
          <h3>比较结果</h3>
          <!-- 表格展示比较结果 -->
          <el-table
            :data="comparisonResults"
            border
            style="width: 100%"
          >
            <el-table-column prop="model_name" label="模型" width="180"></el-table-column>
            <el-table-column v-for="metric in metrics" :key="metric" :prop="metric" :label="metric" min-width="120">
              <template slot-scope="scope">
                {{ formatMetric(scope.row[metric]) }}
              </template>
            </el-table-column>
          </el-table>
          
          <!-- 图表展示比较结果 -->
          <div class="chart-container" v-if="metrics.length > 0">
            <h4>指标比较</h4>
            <div ref="comparisonChart" class="chart"></div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import evaluationCenter from '@/api/evaluationCenter'
import dataCenter from '@/api/dataCenter'
import trainingCenter from '@/api/trainingCenter'
import moment from 'moment'
import * as echarts from 'echarts'
import { mapState, mapActions } from 'vuex'

export default {
  name: 'ModelComparison',
  props: {
    id: {
      type: String,
      required: false
    }
  },
  data() {
    return {
      loading: false,
      submitting: false,
      currentPage: 1,
      pageSize: 10,
      total: 0,
      availableModels: [],
      dialogVisible: false,
      detailVisible: false,
      currentComparison: null,
      metrics: [],
      comparisonResults: [],
      form: {
        name: '',
        description: '',
        dataset: '',
        model_list: []
      },
      rules: {
        name: [
          { required: true, message: '请输入比较名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        dataset: [
          { required: true, message: '请选择数据集', trigger: 'change' }
        ],
        model_list: [
          { type: 'array', required: true, message: '请至少选择两个模型', trigger: 'change', validator: (rule, value, callback) => {
            if (value.length < 2) {
              callback(new Error('请至少选择两个模型进行比较'));
            } else {
              callback();
            }
          }}
        ]
      },
      chart: null,
      searchQuery: '',
      selectedModels: [],
      selectedDataset: null,
      comparisonName: '',
      comparisonDescription: ''
    }
  },
  computed: {
    ...mapState('evaluationCenter', {
      storeComparisons: 'comparisons',
      storeModels: 'models',
      storeDatasets: 'datasets',
      storeLoading: 'loading'
    }),
    // 使用store中的数据，避免命名冲突
    comparisons() {
      return this.storeComparisons || []
    },
    models() {
      return this.storeModels || []
    },
    datasets() {
      return this.storeDatasets || []
    },
    // 比较ID可以从props或路由参数中获取
    comparisonId() {
      return this.id || this.$route.params.id;
    }
  },
  created() {
    this.initialize()
    
    // 如果有比较ID参数，自动加载比较详情
    if (this.comparisonId) {
      this.loadComparisonById(this.comparisonId);
    }
  },
  watch: {
    comparisonId(newVal) {
      if (newVal) {
        this.loadComparisonById(newVal);
      }
    }
  },
  methods: {
    ...mapActions('evaluationCenter', [
      'fetchComparisons',
      'fetchAllModels',
      'fetchAllDatasets',
      'createModelComparison'
    ]),
    
    // 初始化数据
    async initialize() {
      try {
        await Promise.all([
          this.fetchComparisonList(),
          this.fetchModels(),
          this.fetchDatasets()
        ])
      } catch (error) {
        console.error('初始化数据失败:', error)
      }
    },
    
    // 获取比较列表
    async fetchComparisonList() {
      try {
        await this.fetchComparisons({
          page: this.currentPage,
          page_size: this.pageSize,
          search: this.searchQuery
        })
      } catch (error) {
        this.$message.error('获取模型比较列表失败')
        console.error(error)
      }
    },
    
    // 获取模型列表
    async fetchModels() {
      try {
        await this.fetchAllModels()
        // 准备可用模型列表用于Transfer组件
        this.availableModels = this.models.map(model => ({
          key: model.id,
          label: model.name,
          id: model.id,
          name: model.name
        }))
      } catch (error) {
        this.$message.error('获取模型列表失败')
        console.error(error)
      }
    },
    
    // 获取数据集列表
    async fetchDatasets() {
      try {
        await this.fetchAllDatasets()
      } catch (error) {
        this.$message.error('获取数据集列表失败')
        console.error(error)
      }
    },
    
    // 显示创建表单
    showCreateForm() {
      this.dialogVisible = true
      this.resetForm()
    },
    
    // 创建新的比较
    async createComparison() {
      this.$refs.form.validate(async (valid) => {
        if (!valid) {
          return false
        }
        
        this.submitting = true
        try {
          await this.createModelComparison(this.form)
          
          this.$message.success('创建比较成功')
          this.dialogVisible = false
          this.resetForm()
          await this.fetchComparisonList()
        } catch (error) {
          this.$message.error('创建比较失败: ' + (error.message || '未知错误'))
          console.error(error)
        } finally {
          this.submitting = false
        }
      })
    },
    
    // 重置表单
    resetForm() {
      this.form = {
        name: '',
        description: '',
        dataset: '',
        model_list: []
      }
      if (this.$refs.form) {
        this.$refs.form.resetFields()
      }
    },
    
    // 查看比较详情
    async viewComparison(comparison) {
      try {
        this.currentComparison = comparison
        this.prepareComparisonData()
        this.detailVisible = true
        
        this.$nextTick(() => {
          this.initChart()
        })
      } catch (error) {
        this.$message.error('查看比较详情失败')
        console.error(error)
      }
    },
    
    // 删除比较
    async handleDelete(comparison) {
      this.$confirm('确定要删除这个模型比较吗？', '确认删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await evaluationCenter.deleteModelComparison(comparison.id)
          this.$message.success('删除成功')
          await this.fetchComparisonList()
        } catch (error) {
          this.$message.error('删除失败: ' + (error.message || '未知错误'))
          console.error(error)
        }
      }).catch(() => {
        // 用户取消删除
      })
    },
    
    // 处理页码变化
    handleCurrentChange(page) {
      this.currentPage = page
      this.fetchComparisonList()
    },
    
    // 处理每页条数变化
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
      this.fetchComparisonList()
    },
    
    // 根据ID加载比较详情
    async loadComparisonById(id) {
      try {
        const response = await evaluationCenter.getModelComparisonDetail(id)
        this.currentComparison = response.data || response
        this.prepareComparisonData()
        this.detailVisible = true
        this.$nextTick(() => {
          this.initChart()
        })
      } catch (error) {
        console.error('获取模型比较详情失败', error)
        this.$message.error('获取模型比较详情失败：' + (error.message || '未知错误'))
      }
    },
    
    // 准备比较数据
    prepareComparisonData() {
      if (!this.currentComparison || !this.currentComparison.results) {
        this.metrics = []
        this.comparisonResults = []
        return
      }
      
      // 提取指标列表
      this.metrics = this.currentComparison.results.metrics || []
      
      // 准备表格数据
      this.comparisonResults = this.currentComparison.results.data || []
    },
    
    // 初始化图表
    initChart() {
      if (!this.$refs.comparisonChart || this.metrics.length === 0) {
        return
      }
      
      // 销毁现有图表
      if (this.chart) {
        this.chart.dispose()
      }
      
      // 创建新图表
      this.chart = echarts.init(this.$refs.comparisonChart)
      
      // 准备图表数据
      const xAxisData = this.comparisonResults.map(item => item.model_name)
      const series = this.metrics.map(metric => ({
        name: metric,
        type: 'bar',
        data: this.comparisonResults.map(item => item[metric] || 0)
      }))
      
      const option = {
        title: {
          text: '模型性能比较',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: this.metrics,
          top: 30
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: xAxisData,
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value'
        },
        series: series
      }
      
      this.chart.setOption(option)
    },
    
    // 格式化日期
    formatDate(date) {
      if (!date) return '-'
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    
    // 格式化指标值
    formatMetric(value) {
      if (typeof value === 'number') {
        return value.toFixed(4)
      }
      return value || '-'
    }
  },
  
  beforeDestroy() {
    // 销毁图表实例
    if (this.chart) {
      this.chart.dispose()
    }
  }
}
</script>

<style scoped>
.model-comparison {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.comparison-detail {
  padding: 20px;
}

.info-section,
.results-section {
  margin-bottom: 30px;
}

.chart-container {
  margin-top: 30px;
}

.chart {
  width: 100%;
  height: 400px;
}
</style> 