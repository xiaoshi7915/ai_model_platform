<template>
  <div class="knowledge-base-list">
    <!-- 搜索和操作区域 -->
    <div class="table-actions">
      <el-input
        v-model="searchQuery"
        placeholder="搜索知识库名称或内容"
        class="search-input"
        clearable
        @clear="handleSearch"
        @input="handleSearch"
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      
      <div class="action-buttons">
        <el-button type="primary" @click="handleCreate">
          <i class="el-icon-plus"></i> 创建知识库
        </el-button>
        <el-button type="success" @click="showBatchImportDialog">
          <i class="el-icon-upload"></i> 批量导入
        </el-button>
      </div>
    </div>
    
    <!-- 知识库列表表格 -->
    <el-table
      v-loading="loading"
      :data="pagedKnowledgeBases"
      border
      style="width: 100%"
      @row-click="handleRowClick"
    >
      <el-table-column prop="name" label="知识库名称" min-width="150">
        <template slot-scope="scope">
          <el-link type="primary" @click.stop="handleView(scope.row)">
            {{ scope.row.name }}
          </el-link>
        </template>
      </el-table-column>
      
      <el-table-column prop="description" label="描述" min-width="200">
        <template slot-scope="scope">
          <span class="description-text">{{ scope.row.description || '暂无描述' }}</span>
        </template>
      </el-table-column>
      
      <el-table-column prop="content" label="内容预览" min-width="250">
        <template slot-scope="scope">
          <span class="content-preview">{{ getContentPreview(scope.row.content) }}</span>
        </template>
      </el-table-column>
      
      <el-table-column prop="created_by_username" label="创建者" width="120"></el-table-column>
      
      <el-table-column prop="updated_at" label="更新时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.updated_at) }}
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="150" fixed="right">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            @click.stop="handleView(scope.row)"
          >查看</el-button>
          
          <el-button
            size="mini"
            type="text"
            @click.stop="handleEdit(scope.row)"
          >编辑</el-button>
          
          <el-button
            size="mini"
            type="text"
            class="danger-text"
            @click.stop="handleDelete(scope.row)"
          >删除</el-button>
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
        :total="totalKnowledgeBases"
      ></el-pagination>
    </div>
    
    <!-- 批量导入对话框 -->
    <el-dialog
      title="批量导入知识库"
      :visible.sync="batchImportVisible"
      width="600px"
    >
      <div class="batch-import-content">
        <p class="import-tip">支持批量导入多个知识库文件，每个文件将创建为一个独立的知识库。</p>
        
        <el-upload
          class="upload-demo"
          drag
          action="#"
          :http-request="handleBatchImport"
          multiple
          :limit="10"
          :file-list="batchFileList"
          :before-upload="beforeBatchUpload"
          :on-remove="handleBatchRemove"
          :on-exceed="handleBatchExceed"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">支持 .txt、.md、.json 格式文件，单个文件不超过10MB</div>
        </el-upload>
        
        <div class="import-progress" v-if="importingFiles">
          <p>正在导入文件 ({{ importedCount }}/{{ totalImportCount }})</p>
          <el-progress :percentage="importProgress" :format="progressFormat"></el-progress>
        </div>
      </div>
      
      <div slot="footer" class="dialog-footer">
        <el-button @click="batchImportVisible = false" :disabled="importingFiles">取消</el-button>
        <el-button type="primary" @click="startBatchImport" :loading="importingFiles" :disabled="batchFileList.length === 0">开始导入</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import moment from 'moment'

export default {
  name: 'KnowledgeBaseList',
  data() {
    return {
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      batchImportVisible: false,
      batchFileList: [],
      importingFiles: false,
      importedCount: 0,
      totalImportCount: 0,
      importProgress: 0
    }
  },
  computed: {
    ...mapState('dataCenter', {
      knowledgeBases: state => state.knowledgeBases,
      isLoading: state => state.loading,
      error: state => state.error
    }),
    ...mapGetters('dataCenter', [
      'knowledgeBaseList',
      'knowledgeBaseCount'
    ]),
    loading: {
      get() {
        return this.isLoading
      },
      set(value) {
        this.$store.commit('dataCenter/SET_LOADING', value)
      }
    },
    filteredKnowledgeBases() {
      let result = this.knowledgeBaseList
      
      // 根据搜索关键字过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(kb => 
          kb.name.toLowerCase().includes(query) ||
          kb.description.toLowerCase().includes(query)
        )
      }
      
      return result
    },
    pagedKnowledgeBases() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredKnowledgeBases.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredKnowledgeBases.length / this.pageSize)
    },
    totalKnowledgeBases() {
      return this.knowledgeBaseCount
    }
  },
  methods: {
    // 获取知识库列表
    async fetchKnowledgeBases() {
      console.log('开始获取知识库列表...')
      try {
        const response = await this.$store.dispatch('dataCenter/fetchKnowledgeBases')
        console.log('知识库获取成功:', response)
        
        // 检查返回的数据
        if (Array.isArray(response)) {
          console.log('知识库结果数量:', response.length)
          return response
        } else if (response && response.results && Array.isArray(response.results)) {
          console.log('知识库结果数量:', response.results.length)
          return response.results
        } else {
          console.warn('知识库结果为空或格式不正确:', response)
          return []
        }
      } catch (error) {
        console.error('获取知识库失败:', error)
        this.$message.error('获取知识库失败')
        return []
      }
    },
    
    // 处理搜索
    handleSearch() {
      this.currentPage = 1
    },
    
    // 处理页面大小变化
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
    },
    
    // 处理当前页变化
    handleCurrentChange(page) {
      this.currentPage = page
    },
    
    // 处理行点击
    handleRowClick(row) {
      this.handleView(row)
    },
    
    // 处理查看知识库
    handleView(knowledgeBase) {
      this.$emit('view', knowledgeBase)
    },
    
    // 处理创建知识库
    handleCreate() {
      this.$emit('create')
    },
    
    // 处理编辑知识库
    handleEdit(knowledgeBase) {
      this.$emit('edit', knowledgeBase)
    },
    
    // 处理删除知识库
    handleDelete(knowledgeBase) {
      this.$emit('delete', knowledgeBase)
    },
    
    // 获取内容预览
    getContentPreview(content) {
      if (!content) return '暂无内容'
      
      // 截取前100个字符作为预览
      return content.length > 100 ? content.substring(0, 100) + '...' : content
    },
    
    // 格式化日期
    formatDate(date) {
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    
    // 显示批量导入对话框
    showBatchImportDialog() {
      this.batchImportVisible = true
      this.batchFileList = []
      this.importingFiles = false
      this.importedCount = 0
      this.totalImportCount = 0
      this.importProgress = 0
    },
    
    // 批量上传前检查
    beforeBatchUpload(file) {
      // 检查文件类型
      const isValidType = ['.txt', '.md', '.json'].some(ext => file.name.endsWith(ext))
      if (!isValidType) {
        this.$message.error('只支持 .txt、.md、.json 格式文件!')
        return false
      }
      
      // 检查文件大小，限制为10MB
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        this.$message.error('文件大小不能超过 10MB!')
        return false
      }
      
      return true
    },
    
    // 处理批量文件移除
    handleBatchRemove(file, fileList) {
      this.batchFileList = fileList
    },
    
    // 处理超出文件数量限制
    handleBatchExceed() {
      this.$message.warning('最多只能上传10个文件')
    },
    
    // 处理批量导入
    handleBatchImport(options) {
      // 这里只是将文件添加到列表中，不立即上传
      this.batchFileList.push(options.file)
      return Promise.resolve() // 返回一个已解决的Promise
    },
    
    // 开始批量导入
    async startBatchImport() {
      if (this.batchFileList.length === 0) {
        this.$message.warning('请先选择要导入的文件')
        return
      }
      
      this.importingFiles = true
      this.importedCount = 0
      this.totalImportCount = this.batchFileList.length
      this.importProgress = 0
      
      let failCount = 0
      
      // 逐个处理文件
      for (let i = 0; i < this.batchFileList.length; i++) {
        const file = this.batchFileList[i]
        
        try {
          // 读取文件内容
          const content = await this.readFileContent(file)
          
          // 创建知识库
          const knowledgeBase = {
            name: file.name.split('.').slice(0, -1).join('.'), // 使用文件名作为知识库名称
            description: `从文件 ${file.name} 导入的知识库`,
            content: content
          }
          
          // 调用API创建知识库
          await this.$store.dispatch('dataCenter/createKnowledgeBase', knowledgeBase)
          
          this.importedCount++
          this.importProgress = Math.floor((this.importedCount / this.totalImportCount) * 100)
        } catch (error) {
          console.error('导入文件失败:', error)
          failCount++
        }
      }
      
      // 导入完成后刷新列表
      await this.fetchKnowledgeBases()
      
      this.$message.success(`批量导入完成，成功导入 ${this.importedCount} 个知识库，失败 ${failCount} 个`)
      this.importingFiles = false
      this.batchImportVisible = false
    },
    
    // 读取文件内容
    readFileContent(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        
        reader.onload = (e) => {
          try {
            // 尝试解析为JSON
            if (file.name.endsWith('.json')) {
              const jsonObj = JSON.parse(e.target.result)
              resolve(JSON.stringify(jsonObj, null, 2))
            } else {
              // 文本文件直接读取
              resolve(e.target.result)
            }
          } catch (error) {
            reject(error)
          }
        }
        
        reader.onerror = () => {
          reject(new Error('文件读取失败'))
        }
        
        reader.readAsText(file)
      })
    },
    
    // 格式化进度条
    progressFormat(percentage) {
      return `${this.importedCount}/${this.totalImportCount}`
    }
  },
  async created() {
    console.log('KnowledgeBaseList 组件创建，开始获取数据...')
    try {
      // 获取知识库列表
      const knowledgeBases = await this.fetchKnowledgeBases()
      console.log('知识库获取成功:', knowledgeBases)
      
      // 检查Vuex状态
      console.log('Vuex store知识库状态:', {
        knowledgeBases: this.$store.state.dataCenter.knowledgeBases,
        inComputed: this.knowledgeBases,
        filteredKnowledgeBases: this.filteredKnowledgeBases,
        pagedKnowledgeBases: this.pagedKnowledgeBases,
        totalKnowledgeBases: this.totalKnowledgeBases
      })
      
      // 更新本地数据
      this.loading = false
    } catch (error) {
      console.error('数据获取失败:', error)
      this.$message.error('数据获取失败')
      this.loading = false
    }
  }
}
</script>

<style scoped>
.knowledge-base-list {
  padding: 20px;
}

.table-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.danger-text {
  color: #F56C6C;
}

.danger-text:hover {
  color: #f78989;
}

.el-table {
  margin-bottom: 20px;
}

.el-table >>> .el-table__row {
  cursor: pointer;
}

.description-text, .content-preview {
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

.batch-import-content {
  padding: 10px 0;
}

.import-tip {
  margin-bottom: 15px;
  color: #666;
}

.import-progress {
  margin-top: 20px;
}
</style> 