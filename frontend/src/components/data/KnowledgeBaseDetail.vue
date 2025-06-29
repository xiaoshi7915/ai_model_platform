<template>
  <div class="knowledge-base-detail">
    <div class="page-header">
      <el-page-header @back="handleBack" :content="knowledgeBaseDetail ? knowledgeBaseDetail.name : '知识库详情'"></el-page-header>
      
      <div class="header-actions" v-if="knowledgeBaseDetail">
        <el-button type="primary" size="small" @click="handleEdit">编辑</el-button>
        <el-button type="danger" size="small" @click="handleDelete">删除</el-button>
      </div>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!knowledgeBaseDetail" class="empty-container">
      <el-empty description="未找到知识库详情"></el-empty>
    </div>
    
    <div v-else>
      <!-- 基本信息卡片 -->
      <el-card class="detail-card">
        <div slot="header">
          <span>基本信息</span>
        </div>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="知识库名称">{{ knowledgeBaseDetail.name }}</el-descriptions-item>
          <el-descriptions-item label="知识库ID">{{ knowledgeBaseDetail.id }}</el-descriptions-item>
          <el-descriptions-item label="创建者">{{ knowledgeBaseDetail.created_by_username }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(knowledgeBaseDetail.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ formatDate(knowledgeBaseDetail.updated_at) }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ knowledgeBaseDetail.description || '暂无描述' }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
      
      <!-- 内容卡片 -->
      <el-card class="detail-card">
        <div slot="header">
          <span>知识库内容</span>
          <div class="header-actions">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索内容"
              prefix-icon="el-icon-search"
              clearable
              size="small"
              class="search-input"
              @input="handleSearch"
              @clear="clearSearch"
            ></el-input>
            <el-button 
              style="padding: 3px 0; margin-left: 15px" 
              type="text"
              @click="handleCopyContent"
            >复制内容</el-button>
            <el-dropdown @command="handleExport" trigger="click">
              <el-button 
                style="padding: 3px 0; margin-left: 15px" 
                type="text"
              >导出<i class="el-icon-arrow-down el-icon--right"></i></el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="txt">导出为TXT</el-dropdown-item>
                <el-dropdown-item command="json">导出为JSON</el-dropdown-item>
                <el-dropdown-item command="md">导出为Markdown</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>
        
        <div class="search-info" v-if="searchKeyword && searchResults.length > 0">
          找到 {{ searchResults.length }} 处匹配结果
          <el-button type="text" size="mini" @click="navigateSearchResult(-1)" :disabled="currentSearchIndex <= 0">
            <i class="el-icon-arrow-up"></i>
          </el-button>
          <el-button type="text" size="mini" @click="navigateSearchResult(1)" :disabled="currentSearchIndex >= searchResults.length - 1">
            <i class="el-icon-arrow-down"></i>
          </el-button>
          <span class="search-index">{{ searchResults.length > 0 ? currentSearchIndex + 1 : 0 }}/{{ searchResults.length }}</span>
        </div>
        
        <div class="search-info" v-else-if="searchKeyword">
          未找到匹配结果
        </div>
        
        <div class="content-container" ref="contentContainer">
          <pre class="content-text" v-html="highlightedContent"></pre>
        </div>
      </el-card>
      
      <!-- 使用情况卡片 -->
      <el-card class="detail-card">
        <div slot="header">
          <span>使用情况</span>
        </div>
        
        <div v-if="usageLoading" class="loading-container">
          <el-skeleton :rows="3" animated />
        </div>
        
        <div v-else-if="!usageData || usageData.length === 0" class="empty-container">
          <el-empty description="暂无使用记录"></el-empty>
        </div>
        
        <div v-else>
          <el-table
            :data="usageData"
            border
            style="width: 100%"
          >
            <el-table-column prop="type" label="使用类型" width="120"></el-table-column>
            <el-table-column prop="name" label="名称" min-width="150"></el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180">
              <template slot-scope="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template slot-scope="scope">
                <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="text"
                  @click="handleViewUsage(scope.row)"
                >查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'KnowledgeBaseDetail',
  props: {
    knowledgeBaseId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      loading: true,
      usageLoading: true,
      knowledgeBaseDetail: null,
      usageData: [],
      searchKeyword: '',
      searchResults: [],
      currentSearchIndex: 0
    }
  },
  computed: {
    // 高亮显示搜索结果的内容
    highlightedContent() {
      if (!this.knowledgeBaseDetail || !this.knowledgeBaseDetail.content) {
        return ''
      }
      
      if (!this.searchKeyword) {
        return this.escapeHtml(this.knowledgeBaseDetail.content)
      }
      
      // 转义HTML特殊字符
      const content = this.escapeHtml(this.knowledgeBaseDetail.content)
      
      // 使用正则表达式高亮所有匹配项
      const regex = new RegExp(this.escapeRegExp(this.searchKeyword), 'gi')
      return content.replace(regex, match => {
        return `<span class="highlight">${match}</span>`
      })
    }
  },
  methods: {
    // 获取知识库详情
    fetchKnowledgeBaseDetail() {
      this.loading = true
      this.$store.dispatch('dataCenter/fetchKnowledgeBaseDetail', this.knowledgeBaseId)
        .then(response => {
          this.knowledgeBaseDetail = response
          
          // 确保有内容字段
          if (!this.knowledgeBaseDetail.content) {
            this.knowledgeBaseDetail.content = '这是知识库的示例内容。在实际环境中，这里会显示知识库的详细内容。';
          }
          
          this.loading = false
          this.fetchUsageData()
        })
        .catch(error => {
          console.error('获取知识库详情失败:', error)
          
          // 创建一个模拟的知识库详情作为回退方案
          this.knowledgeBaseDetail = {
            id: this.knowledgeBaseId,
            name: `知识库 ${this.knowledgeBaseId}`,
            description: '这是一个示例知识库，用于展示知识库详情页面的布局和功能。',
            content: '这是知识库的示例内容。在实际环境中，这里会显示知识库的详细内容。',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            created_by_username: 'admin',
            type: 'document',
            status: 'active'
          }
          
          this.$message({
            message: '已显示模拟数据，实际API请求失败',
            type: 'warning'
          })
          
          this.loading = false
          this.fetchUsageData()
        })
    },
    
    // 获取使用情况数据
    async fetchUsageData() {
      if (!this.knowledgeBaseId) return
      
      this.usageLoading = true
      try {
        // 获取训练任务中的使用情况
        const trainingResponse = await this.$store.dispatch('trainingCenter/fetchKnowledgeBaseUsage', this.knowledgeBaseId)
        
        // 获取评测任务中的使用情况
        const evaluationResponse = await this.$store.dispatch('evaluationCenter/fetchKnowledgeBaseUsage', this.knowledgeBaseId)
        
        // 获取应用中的使用情况
        const applicationResponse = await this.$store.dispatch('appCenter/fetchKnowledgeBaseUsage', this.knowledgeBaseId)
        
        // 合并所有使用情况数据
        this.usageData = [
          ...(trainingResponse?.data || []).map(item => ({
            ...item,
            type: '训练'
          })),
          ...(evaluationResponse?.data || []).map(item => ({
            ...item,
            type: '评测'
          })),
          ...(applicationResponse?.data || []).map(item => ({
            ...item,
            type: '应用'
          }))
        ].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        
      } catch (error) {
        console.error('获取使用情况失败:', error)
        this.$message.warning('获取使用情况失败')
      } finally {
        this.usageLoading = false
      }
    },
    
    // 处理返回
    handleBack() {
      this.$emit('back')
    },
    
    // 处理编辑
    handleEdit() {
      this.$emit('edit', this.knowledgeBaseDetail)
    },
    
    // 处理删除
    handleDelete() {
      this.$emit('delete', this.knowledgeBaseDetail)
    },
    
    // 处理复制内容
    handleCopyContent() {
      if (!this.knowledgeBaseDetail || !this.knowledgeBaseDetail.content) {
        this.$message.warning('没有可复制的内容')
        return
      }
      
      // 创建临时文本区域
      const textarea = document.createElement('textarea')
      textarea.value = this.knowledgeBaseDetail.content
      document.body.appendChild(textarea)
      textarea.select()
      
      try {
        // 执行复制命令
        const successful = document.execCommand('copy')
        if (successful) {
          this.$message.success('内容已复制到剪贴板')
        } else {
          this.$message.error('复制失败')
        }
      } catch (err) {
        this.$message.error('复制失败: ' + err)
      }
      
      // 移除临时文本区域
      document.body.removeChild(textarea)
    },
    
    // 处理导出
    handleExport(format) {
      if (!this.knowledgeBaseDetail || !this.knowledgeBaseDetail.content) {
        this.$message.warning('没有可导出的内容')
        return
      }
      
      let content = this.knowledgeBaseDetail.content
      let fileName = this.knowledgeBaseDetail.name || 'knowledge_base'
      let mimeType = 'text/plain'
      
      // 根据格式处理内容
      if (format === 'json') {
        try {
          // 尝试解析内容为JSON对象
          const jsonObj = JSON.parse(content)
          content = JSON.stringify(jsonObj, null, 2)
        } catch (e) {
          // 如果内容不是有效的JSON，则创建一个包含内容的JSON对象
          content = JSON.stringify({
            name: this.knowledgeBaseDetail.name,
            description: this.knowledgeBaseDetail.description,
            content: content
          }, null, 2)
        }
        mimeType = 'application/json'
        fileName += '.json'
      } else if (format === 'md') {
        // 添加Markdown标题
        content = `# ${this.knowledgeBaseDetail.name}\n\n${this.knowledgeBaseDetail.description ? `> ${this.knowledgeBaseDetail.description}\n\n` : ''}${content}`
        mimeType = 'text/markdown'
        fileName += '.md'
      } else {
        // 纯文本格式
        fileName += '.txt'
      }
      
      // 创建Blob对象
      const blob = new Blob([content], { type: mimeType })
      
      // 创建下载链接
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = fileName
      
      // 触发点击事件下载文件
      document.body.appendChild(link)
      link.click()
      
      // 清理
      URL.revokeObjectURL(link.href)
      document.body.removeChild(link)
      
      this.$message.success(`已导出为${format.toUpperCase()}文件`)
    },
    
    // 处理查看使用情况
    handleViewUsage(usage) {
      const { type, id } = usage
      switch (type.toLowerCase()) {
        case '训练':
          this.$router.push({
            name: 'TrainingTaskDetail',
            params: { id }
          })
          break
        case '评测':
          this.$router.push({
            name: 'EvaluationTaskDetail',
            params: { id }
          })
          break
        case '应用':
          this.$router.push({
            name: 'ApplicationDetail',
            params: { id }
          })
          break
        default:
          this.$message.warning('暂不支持查看该类型的使用情况')
      }
    },
    
    // 处理搜索
    handleSearch() {
      if (!this.searchKeyword || !this.knowledgeBaseDetail || !this.knowledgeBaseDetail.content) {
        this.searchResults = []
        this.currentSearchIndex = 0
        return
      }
      
      // 查找所有匹配项的位置
      const content = this.knowledgeBaseDetail.content
      const keyword = this.searchKeyword.toLowerCase()
      const results = []
      
      let position = content.toLowerCase().indexOf(keyword)
      while (position !== -1) {
        results.push(position)
        position = content.toLowerCase().indexOf(keyword, position + 1)
      }
      
      this.searchResults = results
      this.currentSearchIndex = results.length > 0 ? 0 : -1
      
      // 滚动到第一个搜索结果
      this.$nextTick(() => {
        this.scrollToCurrentSearchResult()
      })
    },
    
    // 清除搜索
    clearSearch() {
      this.searchKeyword = ''
      this.searchResults = []
      this.currentSearchIndex = 0
    },
    
    // 导航到下一个或上一个搜索结果
    navigateSearchResult(direction) {
      if (this.searchResults.length === 0) return
      
      this.currentSearchIndex = (this.currentSearchIndex + direction + this.searchResults.length) % this.searchResults.length
      
      this.$nextTick(() => {
        this.scrollToCurrentSearchResult()
      })
    },
    
    // 滚动到当前搜索结果
    scrollToCurrentSearchResult() {
      if (this.searchResults.length === 0 || this.currentSearchIndex < 0) return
      
      const container = this.$refs.contentContainer
      const highlights = container.querySelectorAll('.highlight')
      
      if (highlights.length > this.currentSearchIndex) {
        const highlight = highlights[this.currentSearchIndex]
        
        // 添加当前高亮样式
        highlights.forEach(el => el.classList.remove('current-highlight'))
        highlight.classList.add('current-highlight')
        
        // 滚动到当前高亮位置
        highlight.scrollIntoView({
          behavior: 'smooth',
          block: 'center'
        })
      }
    },
    
    // 转义HTML特殊字符
    escapeHtml(text) {
      return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;')
    },
    
    // 转义正则表达式特殊字符
    escapeRegExp(string) {
      return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    },
    
    // 格式化日期
    formatDate(date) {
      return date ? moment(date).format('YYYY-MM-DD HH:mm:ss') : '未知'
    },
    
    // 获取状态类型
    getStatusType(status) {
      const types = {
        'active': 'success',
        'running': 'warning',
        'completed': 'success',
        'failed': 'danger',
        'pending': 'info',
        'cancelled': 'info'
      }
      return types[status] || 'info'
    }
  },
  created() {
    this.fetchKnowledgeBaseDetail()
  },
  watch: {
    knowledgeBaseId: {
      handler(newVal) {
        if (newVal) {
          this.fetchKnowledgeBaseDetail()
        }
      },
      immediate: true
    }
  }
}
</script>

<style scoped>
.knowledge-base-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.loading-container, .empty-container {
  min-height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.detail-card {
  margin-bottom: 20px;
}

.detail-card >>> .el-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  width: 200px;
}

.search-info {
  margin-bottom: 10px;
  padding: 5px 10px;
  background-color: #f0f9eb;
  border-radius: 4px;
  display: flex;
  align-items: center;
}

.search-index {
  margin-left: 5px;
  color: #67c23a;
  font-weight: bold;
}

.content-container {
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  min-height: 200px;
  max-height: 500px;
  overflow: auto;
}

.content-text {
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
  padding: 0;
}

.content-text >>> .highlight {
  background-color: #ffeaa7;
  border-radius: 2px;
}

.content-text >>> .current-highlight {
  background-color: #fdcb6e;
  border-radius: 2px;
  font-weight: bold;
}
</style> 