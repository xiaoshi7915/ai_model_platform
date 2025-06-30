<template>
  <div class="application-detail">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <i class="el-icon-loading"></i>
      <p>正在加载应用详情...</p>
    </div>
    
    <!-- 空数据提示 -->
    <div v-else-if="!application" class="empty-container">
      <i class="el-icon-warning"></i>
      <p>未找到应用信息</p>
      <el-button @click="$emit('back')">返回列表</el-button>
    </div>
    
    <!-- 基本信息卡片 -->
    <el-card class="detail-card" v-if="application">
      <div slot="header">
        <span>应用信息</span>
        <el-button
          style="float: right; padding: 3px 0"
          type="text"
          @click="handleEdit"
          :disabled="application.status === 'running'"
        >编辑</el-button>
      </div>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="应用名称">{{ application.name }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(application.status)">
            {{ getStatusText(application.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="使用模型">{{ application.model_name }}</el-descriptions-item>
        <el-descriptions-item label="API端点">
          <el-link v-if="application.endpoint" type="primary" :href="application.endpoint" target="_blank">
            {{ application.endpoint }}
          </el-link>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="创建者">{{ application.created_by_username }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(application.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ application.description || '暂无描述' }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 配置信息卡片 -->
    <el-card class="detail-card" v-if="application">
      <div slot="header">
        <span>配置信息</span>
      </div>
      
      <div v-if="application.config">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="最大并发数">{{ application.config.max_concurrency }}</el-descriptions-item>
          <el-descriptions-item label="超时时间">{{ application.config.timeout }}秒</el-descriptions-item>
          <el-descriptions-item label="日志级别">{{ application.config.log_level }}</el-descriptions-item>
          <el-descriptions-item label="缓存大小">{{ application.config.cache_size }}MB</el-descriptions-item>
          <el-descriptions-item label="批处理大小">{{ application.config.batch_size }}</el-descriptions-item>
          <el-descriptions-item label="使用量化">{{ application.config.use_quantization ? '是' : '否' }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 环境变量 -->
        <div v-if="application.config.env_vars && application.config.env_vars.length > 0" class="env-vars-section">
          <h4>环境变量</h4>
          <el-table :data="application.config.env_vars" border style="width: 100%">
            <el-table-column prop="key" label="变量名"></el-table-column>
            <el-table-column prop="value" label="变量值"></el-table-column>
          </el-table>
        </div>
      </div>
      <div v-else class="empty-data">
        <i class="el-icon-info"></i>
        <p>暂无配置信息</p>
      </div>
    </el-card>

    <!-- 监控信息卡片 -->
    <el-card class="detail-card" v-if="application && application.status === 'running'">
      <div slot="header">
        <span>监控信息</span>
        <el-button
          style="float: right; padding: 3px 0"
          type="text"
          @click="refreshMonitoringData"
        >刷新</el-button>
      </div>
      
      <div v-if="monitoringData">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="monitor-item">
              <div class="monitor-title">CPU使用率</div>
              <el-progress
                :percentage="monitoringData.cpu_usage"
                :color="getCpuProgressColor(monitoringData.cpu_usage)"
              ></el-progress>
              <div class="monitor-value">{{ monitoringData.cpu_usage.toFixed(2) }}%</div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="monitor-item">
              <div class="monitor-title">内存使用率</div>
              <el-progress
                :percentage="monitoringData.memory_usage"
                :color="getMemoryProgressColor(monitoringData.memory_usage)"
              ></el-progress>
              <div class="monitor-value">{{ monitoringData.memory_usage.toFixed(2) }}% ({{ formatMemorySize(monitoringData.memory_used) }} / {{ formatMemorySize(monitoringData.memory_total) }})</div>
            </div>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" class="monitor-row">
          <el-col :span="8">
            <div class="stat-card">
              <div class="stat-title">请求总数</div>
              <div class="stat-value">{{ monitoringData.total_requests }}</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-card">
              <div class="stat-title">平均响应时间</div>
              <div class="stat-value">{{ monitoringData.avg_response_time.toFixed(2) }}ms</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-card">
              <div class="stat-title">错误率</div>
              <div class="stat-value">{{ monitoringData.error_rate.toFixed(2) }}%</div>
            </div>
          </el-col>
        </el-row>
      </div>
      <div v-else class="empty-data">
        <i class="el-icon-loading"></i>
        <p>加载监控数据中...</p>
      </div>
    </el-card>

    <!-- 日志信息卡片 -->
    <el-card class="detail-card" v-if="application">
      <div slot="header">
        <span>日志信息</span>
        <div style="float: right;">
          <el-select v-model="logLevel" placeholder="日志级别" size="mini" style="margin-right: 10px;">
            <el-option label="全部" value="all"></el-option>
            <el-option label="INFO" value="info"></el-option>
            <el-option label="WARNING" value="warning"></el-option>
            <el-option label="ERROR" value="error"></el-option>
            <el-option label="DEBUG" value="debug"></el-option>
          </el-select>
          <el-button type="text" @click="refreshLogs">刷新</el-button>
        </div>
      </div>
      
      <div v-if="logs.length > 0" class="logs-container">
        <div
          v-for="(log, index) in filteredLogs"
          :key="index"
          class="log-item"
          :class="getLogClass(log.level)"
        >
          <span class="log-time">{{ formatDate(log.timestamp) }}</span>
          <span class="log-level" :class="getLogClass(log.level)">{{ log.level.toUpperCase() }}</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
      </div>
      <div v-else class="empty-data">
        <i class="el-icon-info"></i>
        <p>暂无日志信息</p>
      </div>
      
      <div class="logs-pagination" v-if="logs.length > 0">
        <el-pagination
          @current-change="handleLogPageChange"
          :current-page="logPage"
          :page-size="10"
          layout="prev, pager, next"
          :total="logs.length"
        ></el-pagination>
      </div>
    </el-card>

    <!-- 插件信息卡片 -->
    <el-card class="detail-card" v-if="application">
      <div slot="header">
        <span>插件信息</span>
        <el-button
          style="float: right; padding: 3px 0"
          type="text"
          @click="handleManagePlugins"
          :disabled="application.status === 'running'"
        >管理插件</el-button>
      </div>
      
      <div v-if="plugins.length > 0">
        <el-table :data="plugins" border style="width: 100%">
          <el-table-column prop="name" label="插件名称"></el-table-column>
          <el-table-column prop="version" label="版本"></el-table-column>
          <el-table-column label="状态">
            <template slot-scope="scope">
              <el-tag :type="scope.row.enabled ? 'success' : 'info'">
                {{ scope.row.enabled ? '已启用' : '已禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template slot-scope="scope">
              <el-switch
                v-model="scope.row.enabled"
                @change="handlePluginStatusChange(scope.row)"
                :disabled="application.status === 'running'"
              ></el-switch>
              <el-button
                size="mini"
                type="danger"
                icon="el-icon-delete"
                circle
                @click="handleRemovePlugin(scope.row)"
                :disabled="application.status === 'running'"
              ></el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="empty-data">
        <i class="el-icon-info"></i>
        <p>暂未添加插件</p>
      </div>
    </el-card>

    <!-- 操作卡片 -->
    <el-card class="detail-card" v-if="application">
      <div slot="header">
        <span>操作</span>
      </div>
      
      <div class="action-buttons">
        <el-button
          type="success"
          @click="handleDeploy"
          v-if="application.status === 'stopped'"
        >
          <i class="el-icon-video-play"></i> 部署应用
        </el-button>
        
        <el-button
          type="warning"
          @click="handleStop"
          v-if="application.status === 'running'"
        >
          <i class="el-icon-video-pause"></i> 停止应用
        </el-button>
        
        <el-button
          type="primary"
          @click="handleEdit"
          :disabled="application.status === 'running'"
        >
          <i class="el-icon-edit"></i> 编辑应用
        </el-button>
        
        <el-button
          type="danger"
          @click="handleDelete"
          :disabled="application.status === 'running'"
        >
          <i class="el-icon-delete"></i> 删除应用
        </el-button>
      </div>
    </el-card>

    <!-- 插件管理对话框 -->
    <el-dialog
      title="管理插件"
      :visible.sync="pluginDialogVisible"
      width="60%"
    >
      <el-transfer
        v-model="selectedPlugins"
        :data="availablePlugins"
        :titles="['可用插件', '已选插件']"
        :props="{
          key: 'id',
          label: item => `${item.name} (${item.version})`
        }"
      ></el-transfer>
      <span slot="footer" class="dialog-footer">
        <el-button @click="pluginDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePlugins">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import moment from 'moment'
import { mapState, mapActions } from 'vuex'
import api from '@/api'
import { generateMockMonitoring, generateMockLogs } from '@/utils/mockData'
import PluginList from './PluginList.vue'

export default {
  name: 'ApplicationDetail',
  props: {
    applicationId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      // 应用数据
      application: null,
      loading: false,
      // 监控数据
      monitoringData: null,
      // 日志数据
      logs: [],
      logLevel: 'all',
      logPage: 1,
      // 插件数据
      plugins: [],
      // 插件管理对话框
      pluginDialogVisible: false,
      availablePlugins: [],
      selectedPlugins: []
    }
  },
  computed: {
    ...mapState({
      allPlugins: state => state.appCenter.plugins || []
    }),
    
    // 过滤后的日志
    filteredLogs() {
      let result = this.logs
      
      // 按日志级别过滤
      if (this.logLevel !== 'all') {
        result = result.filter(log => log.level === this.logLevel)
      }
      
      // 分页
      const start = (this.logPage - 1) * 10
      const end = start + 10
      return result.slice(start, end)
    }
  },
  methods: {
    ...mapActions('appCenter', [
      'fetchPlugins'
    ]),
    
    // 获取应用详情
    async fetchApplicationDetail() {
      if (!this.applicationId) return
      
      this.loading = true
      try {
        const response = await this.$store.dispatch('appCenter/fetchApplicationDetail', this.applicationId)
        this.application = response
        
        // 获取其他数据
        this.refreshMonitoringData()
        this.refreshLogs()
        this.fetchApplicationPlugins()
        this.fetchAvailablePlugins()
      } catch (error) {
        console.error('获取应用详情失败:', error)
        this.$message.error('获取应用详情失败')
        
        // 使用模拟数据作为回退
        this.application = {
          id: this.applicationId,
          name: `应用 ${this.applicationId}`,
          description: '这是一个示例应用',
          status: 'stopped',
          model_name: 'gpt-3.5-turbo',
          endpoint: null,
          created_by_username: 'admin',
          created_at: new Date().toISOString(),
          config: {
            max_concurrency: 10,
            timeout: 30,
            log_level: 'INFO',
            cache_size: 512,
            batch_size: 1,
            use_quantization: false,
            env_vars: []
          }
        }
        
        // 获取其他数据
        this.refreshMonitoringData()
        this.refreshLogs()
        this.fetchApplicationPlugins()
        this.fetchAvailablePlugins()
      } finally {
        this.loading = false
      }
    },
    
    // 格式化日期
    formatDate(date) {
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    
    // 获取状态类型
    getStatusType(status) {
      const types = {
        stopped: 'info',
        running: 'success',
        error: 'danger'
      }
      return types[status] || 'info'
    },
    
    // 获取状态文本
    getStatusText(status) {
      const texts = {
        stopped: '已停止',
        running: '运行中',
        error: '错误'
      }
      return texts[status] || status
    },
    
    // 获取CPU进度条颜色
    getCpuProgressColor(value) {
      if (value < 50) return '#67c23a'
      if (value < 80) return '#e6a23c'
      return '#f56c6c'
    },
    
    // 获取内存进度条颜色
    getMemoryProgressColor(value) {
      if (value < 60) return '#67c23a'
      if (value < 85) return '#e6a23c'
      return '#f56c6c'
    },
    
    // 格式化内存大小
    formatMemorySize(bytes) {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    
    // 获取日志样式类
    getLogClass(level) {
      const classes = {
        info: 'log-info',
        warning: 'log-warning',
        error: 'log-error',
        debug: 'log-debug'
      }
      return classes[level] || ''
    },
    
    // 刷新监控数据
    refreshMonitoringData() {
      if (!this.application) return
      
      // 调用API获取监控数据
      api.appCenter.getApplicationMonitoring(this.application.id)
        .then(response => {
          this.monitoringData = response
        })
        .catch(error => {
          console.error('获取监控数据失败:', error)
          
          // 如果API调用失败，使用模拟数据
          setTimeout(() => {
            this.monitoringData = generateMockMonitoring()
          }, 500)
        })
    },
    
    // 刷新日志
    refreshLogs() {
      if (!this.application) return
      
      // 调用API获取日志数据
      api.appCenter.getApplicationLogs(this.application.id, {
        level: this.logLevel !== 'all' ? this.logLevel : undefined
      })
        .then(response => {
          this.logs = response
          this.logPage = 1
        })
        .catch(error => {
          console.error('获取日志数据失败:', error)
          
          // 如果API调用失败，使用模拟数据
          setTimeout(() => {
            this.logs = generateMockLogs(50)
            this.logPage = 1
          }, 500)
        })
    },
    
    // 处理日志分页变化
    handleLogPageChange(page) {
      this.logPage = page
    },
    
    // 处理编辑应用
    handleEdit() {
      this.$emit('edit', this.application)
    },
    
    // 处理部署应用
    handleDeploy() {
      this.$confirm('确定要部署该应用吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        // 调用API部署应用
        api.appCenter.deployApplication(this.application.id)
          .then(() => {
            this.$message.success('应用部署成功')
            this.$emit('deploy', this.application)
          })
          .catch(error => {
            console.error('应用部署失败:', error)
            this.$message.error('应用部署失败')
          })
      }).catch(() => {})
    },
    
    // 处理停止应用
    handleStop() {
      this.$confirm('确定要停止该应用吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 调用API停止应用
        api.appCenter.stopApplication(this.application.id)
          .then(() => {
            this.$message.success('应用停止成功')
            this.$emit('stop', this.application)
          })
          .catch(error => {
            console.error('应用停止失败:', error)
            this.$message.error('应用停止失败')
          })
      }).catch(() => {})
    },
    
    // 处理删除应用
    handleDelete() {
      this.$confirm('此操作将永久删除该应用, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', this.application)
      }).catch(() => {})
    },
    
    // 处理管理插件
    handleManagePlugins() {
      this.pluginDialogVisible = true
      this.selectedPlugins = this.plugins.map(plugin => plugin.id)
    },
    
    // 处理插件状态变更
    handlePluginStatusChange(plugin) {
      // 调用API更新插件状态
      api.appCenter.addPluginToApplication(this.application.id, {
        plugin_id: plugin.id,
        config: { enabled: plugin.enabled }
      })
        .then(() => {
          this.$message.success(`插件 ${plugin.name} ${plugin.enabled ? '已启用' : '已禁用'}`)
        })
        .catch(error => {
          console.error('更新插件状态失败:', error)
          this.$message.error('更新插件状态失败')
          // 恢复原状态
          plugin.enabled = !plugin.enabled
        })
    },
    
    // 处理移除插件
    handleRemovePlugin(plugin) {
      this.$confirm(`确定要移除插件 ${plugin.name} 吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 调用API移除插件
        api.appCenter.removePluginFromApplication(this.application.id, {
          plugin_id: plugin.id
        })
          .then(() => {
            this.plugins = this.plugins.filter(p => p.id !== plugin.id)
            this.$message.success('插件已移除')
          })
          .catch(error => {
            console.error('移除插件失败:', error)
            this.$message.error('移除插件失败')
          })
      }).catch(() => {})
    },
    
    // 保存插件设置
    savePlugins() {
      // 获取已选插件和未选插件的差异
      const currentPluginIds = this.plugins.map(plugin => plugin.id)
      const addPluginIds = this.selectedPlugins.filter(id => !currentPluginIds.includes(id))
      const removePluginIds = currentPluginIds.filter(id => !this.selectedPlugins.includes(id))
      
      // 创建Promise数组
      const promises = []
      
      // 添加插件
      addPluginIds.forEach(pluginId => {
        promises.push(
          api.appCenter.addPluginToApplication(this.application.id, {
            plugin_id: pluginId,
            config: { enabled: true }
          })
        )
      })
      
      // 移除插件
      removePluginIds.forEach(pluginId => {
        promises.push(
          api.appCenter.removePluginFromApplication(this.application.id, {
            plugin_id: pluginId
          })
        )
      })
      
      // 执行所有Promise
      Promise.all(promises)
        .then(() => {
          // 更新插件列表
          this.fetchApplicationPlugins()
          this.pluginDialogVisible = false
          this.$message.success('插件设置已保存')
        })
        .catch(error => {
          console.error('保存插件设置失败:', error)
          this.$message.error('保存插件设置失败')
        })
    },
    
    // 获取应用插件
    fetchApplicationPlugins() {
      // 调用API获取应用插件
      api.appCenter.getApplicationDetail(this.application.id)
        .then(response => {
          this.plugins = response.plugins || []
        })
        .catch(error => {
          console.error('获取应用插件失败:', error)
          this.$message.error('获取应用插件失败')
          
          // 如果API调用失败，使用模拟数据
          setTimeout(() => {
            this.plugins = [
              {
                id: 1,
                name: '日志分析插件',
                version: '1.0.0',
                enabled: true
              },
              {
                id: 2,
                name: '性能监控插件',
                version: '2.1.0',
                enabled: false
              }
            ]
          }, 500)
        })
    },
    
    // 获取可用插件
    fetchAvailablePlugins() {
      this.fetchPlugins().then(() => {
        this.availablePlugins = this.allPlugins.map(plugin => ({
          id: plugin.id,
          name: plugin.name,
          version: plugin.version
        }))
      })
    }
  },
  created() {
    // 先获取应用详情
    this.fetchApplicationDetail()
  },
}
</script>

<style scoped>
.application-detail {
  padding: 20px;
}

.detail-card {
  margin-bottom: 20px;
}

.empty-data {
  text-align: center;
  padding: 30px 0;
  color: #909399;
}

.empty-data i {
  font-size: 40px;
  margin-bottom: 10px;
}

.env-vars-section {
  margin-top: 20px;
}

.monitor-row {
  margin-top: 20px;
}

.monitor-item {
  margin-bottom: 15px;
}

.monitor-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.monitor-value {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  text-align: right;
}

.stat-card {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 15px;
  text-align: center;
}

.stat-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  color: #303133;
  font-weight: bold;
}

.logs-container {
  max-height: 300px;
  overflow-y: auto;
  background-color: #1e1e1e;
  border-radius: 4px;
  padding: 10px;
  font-family: monospace;
}

.log-item {
  margin-bottom: 5px;
  color: #dcdfe6;
  white-space: pre-wrap;
  word-break: break-all;
}

.log-time {
  color: #909399;
  margin-right: 10px;
}

.log-level {
  display: inline-block;
  width: 70px;
  margin-right: 10px;
  font-weight: bold;
}

.log-info {
  color: #67c23a;
}

.log-warning {
  color: #e6a23c;
}

.log-error {
  color: #f56c6c;
}

.log-debug {
  color: #409eff;
}

.logs-pagination {
  margin-top: 10px;
  text-align: center;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 10px 0;
}

.loading-container, .empty-container {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

.loading-container i, .empty-container i {
  font-size: 48px;
  margin-bottom: 20px;
  display: block;
}

.loading-container p, .empty-container p {
  font-size: 16px;
  margin-bottom: 20px;
}
</style> 