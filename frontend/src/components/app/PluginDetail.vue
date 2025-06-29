<template>
  <div class="plugin-detail">
    <!-- 基本信息卡片 -->
    <el-card class="detail-card">
      <div slot="header">
        <span>插件信息</span>
        <el-button
          style="float: right; padding: 3px 0"
          type="text"
          @click="handleEdit"
        >编辑</el-button>
      </div>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="插件名称">{{ plugin.name }}</el-descriptions-item>
        <el-descriptions-item label="版本">{{ plugin.version }}</el-descriptions-item>
        <el-descriptions-item label="创建者">{{ plugin.created_by_username }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(plugin.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ plugin.description || '暂无描述' }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 兼容性信息卡片 -->
    <el-card class="detail-card">
      <div slot="header">
        <span>兼容性信息</span>
      </div>
      
      <div v-if="plugin.compatibility && Object.keys(plugin.compatibility).length > 0">
        <el-descriptions :column="2" border>
          <el-descriptions-item v-for="(value, key) in plugin.compatibility" :key="key" :label="key">
            {{ value }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <div v-else class="empty-data">
        <i class="el-icon-info"></i>
        <p>暂无兼容性信息</p>
      </div>
    </el-card>

    <!-- 使用情况卡片 -->
    <el-card class="detail-card">
      <div slot="header">
        <span>使用情况</span>
      </div>
      
      <div v-if="usageData.length > 0">
        <el-table :data="usageData" style="width: 100%">
          <el-table-column prop="app_name" label="应用名称"></el-table-column>
          <el-table-column prop="status" label="状态">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="enabled" label="插件状态">
            <template slot-scope="scope">
              <el-tag :type="scope.row.enabled ? 'success' : 'info'">
                {{ scope.row.enabled ? '已启用' : '已禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="添加时间">
            <template slot-scope="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="empty-data">
        <i class="el-icon-info"></i>
        <p>该插件暂未被使用</p>
      </div>
    </el-card>

    <!-- 操作卡片 -->
    <el-card class="detail-card">
      <div slot="header">
        <span>操作</span>
      </div>
      
      <div class="action-buttons">
        <el-button
          type="primary"
          @click="handleDownload"
        >
          <i class="el-icon-download"></i> 下载插件
        </el-button>
        
        <el-button
          type="danger"
          @click="handleDelete"
        >
          <i class="el-icon-delete"></i> 删除插件
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'PluginDetail',
  props: {
    plugin: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      // 模拟使用情况数据
      usageData: []
    }
  },
  methods: {
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
    
    // 处理编辑
    handleEdit() {
      this.$emit('edit', this.plugin)
    },
    
    // 处理下载
    handleDownload() {
      if (this.plugin.file) {
        window.open(this.plugin.file, '_blank')
      } else {
        this.$message.warning('插件文件不可用')
      }
    },
    
    // 处理删除
    handleDelete() {
      this.$confirm('此操作将永久删除该插件, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', this.plugin)
      }).catch(() => {})
    },
    
    // 获取插件使用情况
    fetchUsageData() {
      // 这里应该调用API获取使用情况数据
      // 模拟数据
      setTimeout(() => {
        if (Math.random() > 0.5) {
          this.usageData = [
            {
              app_name: '应用A',
              status: 'running',
              enabled: true,
              created_at: new Date()
            },
            {
              app_name: '应用B',
              status: 'stopped',
              enabled: false,
              created_at: new Date()
            }
          ]
        }
      }, 500)
    }
  },
  created() {
    this.fetchUsageData()
  }
}
</script>

<style scoped>
.plugin-detail {
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

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 10px 0;
}
</style> 