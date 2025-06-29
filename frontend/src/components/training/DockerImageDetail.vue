<template>
  <div class="docker-image-detail">
    <!-- 基本信息卡片 -->
    <el-card class="detail-card">
      <div slot="header">
        <span>镜像信息</span>
        <el-button
          style="float: right; padding: 3px 0"
          type="text"
          @click="handleEdit"
        >编辑</el-button>
      </div>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="镜像名称">{{ image.name }}</el-descriptions-item>
        <el-descriptions-item label="标签">{{ image.tag }}</el-descriptions-item>
        <el-descriptions-item label="仓库">{{ image.registry }}</el-descriptions-item>
        <el-descriptions-item label="大小">{{ formatSize(image.size) }}</el-descriptions-item>
        <el-descriptions-item label="创建者">{{ image.created_by_username }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(image.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ image.description || '暂无描述' }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 使用情况卡片 -->
    <el-card class="detail-card">
      <div slot="header">
        <span>使用情况</span>
      </div>
      
      <div v-if="usageData.length > 0">
        <el-table :data="usageData" style="width: 100%">
          <el-table-column prop="model_name" label="模型名称"></el-table-column>
          <el-table-column prop="version" label="版本"></el-table-column>
          <el-table-column prop="status" label="状态">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间">
            <template slot-scope="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="empty-data">
        <i class="el-icon-info"></i>
        <p>该镜像暂未被使用</p>
      </div>
    </el-card>

    <!-- 操作卡片 -->
    <el-card class="detail-card">
      <div slot="header">
        <span>操作</span>
      </div>
      
      <div class="action-buttons">
        <el-button type="primary" @click="handlePull">
          <i class="el-icon-download"></i> 拉取镜像
        </el-button>
        
        <el-button type="danger" @click="handleDelete">
          <i class="el-icon-delete"></i> 删除镜像
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'DockerImageDetail',
  props: {
    image: {
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
    
    // 格式化大小
    formatSize(size) {
      return `${size} MB`
    },
    
    // 获取状态类型
    getStatusType(status) {
      const types = {
        pending: 'info',
        running: 'warning',
        completed: 'success',
        failed: 'danger'
      }
      return types[status] || 'info'
    },
    
    // 获取状态文本
    getStatusText(status) {
      const texts = {
        pending: '等待中',
        running: '运行中',
        completed: '已完成',
        failed: '失败'
      }
      return texts[status] || status
    },
    
    // 处理编辑
    handleEdit() {
      this.$emit('edit', this.image)
    },
    
    // 处理拉取镜像
    handlePull() {
      this.$message.success('开始拉取镜像')
      // 这里可以调用拉取镜像的API
    },
    
    // 处理删除镜像
    handleDelete() {
      this.$confirm('此操作将永久删除该镜像, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', this.image)
      }).catch(() => {})
    },
    
    // 获取镜像使用情况
    fetchUsageData() {
      // 这里应该调用API获取使用情况数据
      // 模拟数据
      setTimeout(() => {
        if (Math.random() > 0.5) {
          this.usageData = [
            {
              model_name: '模型A',
              version: '1.0.0',
              status: 'completed',
              created_at: new Date()
            },
            {
              model_name: '模型B',
              version: '2.1.0',
              status: 'running',
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
.docker-image-detail {
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