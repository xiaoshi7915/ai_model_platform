<template>
  <div class="dataset-list">
    <!-- 搜索和过滤区域 -->
    <div class="table-actions">
      <el-input
        v-model="searchQuery"
        placeholder="搜索数据集名称"
        class="search-input"
        clearable
        @clear="handleSearch"
        @input="handleSearch"
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      
      <el-select 
        v-model="formatFilter" 
        placeholder="文件格式" 
        clearable 
        @change="handleFormatChange"
        class="format-filter"
      >
        <el-option
          v-for="format in formattedDatasetFormats"
          :key="typeof format === 'object' ? format.value : format"
          :label="typeof format === 'object' ? format.label : format"
          :value="typeof format === 'object' ? format.value : format"
        ></el-option>
      </el-select>
      
      <el-button type="primary" @click="handleCreate">
        <i class="el-icon-plus"></i> 上传数据集
      </el-button>
    </div>
    
    <!-- 数据集列表表格 -->
    <el-table
      v-loading="loading"
      :data="pagedDatasets"
      border
      style="width: 100%"
      @row-click="handleRowClick"
    >
      <el-table-column prop="name" label="数据集名称" min-width="150">
        <template slot-scope="scope">
          <el-link type="primary" @click.stop="handleView(scope.row)">
            {{ scope.row.name }}
          </el-link>
        </template>
      </el-table-column>
      
      <el-table-column prop="file_format" label="文件格式" width="100">
        <template slot-scope="scope">
          <el-tag size="small">{{ scope.row.file_format }}</el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="file_size" label="文件大小" width="120">
        <template slot-scope="scope">
          {{ formatFileSize(scope.row.file_size) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="status" label="状态" width="100">
        <template slot-scope="scope">
          <el-tag 
            :type="getStatusType(scope.row.status)" 
            size="small">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="is_public" label="可见性" width="100">
        <template slot-scope="scope">
          <el-tag 
            :type="scope.row.is_public ? 'success' : 'info'" 
            size="small">
            {{ scope.row.is_public ? '公开' : '私有' }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="created_by_username" label="创建者" width="120"></el-table-column>
      
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.created_at) }}
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
        :total="totalDatasets"
      ></el-pagination>
    </div>
    
    <!-- 上传数据集对话框 -->
    <el-dialog
      :title="dialogType === 'create' ? '上传数据集' : '编辑数据集'"
      :visible.sync="dialogVisible"
      width="600px"
      @closed="resetForm"
    >
      <el-form
        ref="datasetForm"
        :model="currentDataset"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="数据集名称" prop="name">
          <el-input v-model="currentDataset.name" placeholder="请输入数据集名称"></el-input>
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="currentDataset.description"
            type="textarea"
            :rows="4"
            placeholder="请输入数据集描述"
          ></el-input>
        </el-form-item>
        
        <el-form-item v-if="dialogType === 'create'" label="数据集文件" prop="file">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :http-request="handleFileUpload"
            :limit="1"
            :file-list="fileList"
            :before-upload="beforeUpload"
            :on-remove="handleRemove"
            :on-exceed="handleExceed"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">支持CSV、JSON、TXT等格式文件</div>
          </el-upload>
        </el-form-item>
      </el-form>
      
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveDataset" :loading="saveLoading">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import moment from 'moment'

export default {
  name: 'DatasetList',
  data() {
    return {
      searchQuery: '',
      formatFilter: '',
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      dialogType: 'create', // 'create' 或 'edit'
      currentDataset: {
        name: '',
        description: '',
        file: null
      },
      fileList: [],
      saveLoading: false,
      rules: {
        name: [
          { required: true, message: '请输入数据集名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        file: [
          { required: true, message: '请上传数据集文件', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    ...mapState('dataCenter', {
      datasets: state => state.datasets,
      isLoading: state => state.loading,
      error: state => state.error
    }),
    ...mapGetters('dataCenter', [
      'datasetList',
      'datasetCount',
      'datasetFormats'
    ]),
    loading: {
      get() {
        return this.isLoading
      },
      set(value) {
        this.$store.commit('dataCenter/SET_LOADING', value)
      }
    },
    filteredDatasets() {
      console.log('计算过滤数据集，当前数据集:', this.datasets);
      let result = this.datasets;
      
      // 根据搜索关键字过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(dataset => 
          (dataset.name && dataset.name.toLowerCase().includes(query)) ||
          (dataset.description && dataset.description.toLowerCase().includes(query))
        )
      }
      
      // 根据格式过滤
      if (this.formatFilter) {
        result = result.filter(dataset => 
          dataset.file_format === this.formatFilter
        )
      }
      
      return result
    },
    
    // 分页后的数据集
    pagedDatasets() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredDatasets.slice(start, end)
    },
    
    // 总页数
    totalPages() {
      return Math.ceil(this.filteredDatasets.length / this.pageSize)
    },
    
    // 总数据集数量
    totalDatasets() {
      const count = this.datasets ? this.datasets.length : 0;
      console.log('总数据集数量:', count);
      return count;
    },
    
    // 格式化后的数据集格式列表
    formattedDatasetFormats() {
      if (!this.datasetFormats || this.datasetFormats.length === 0) return [];
      
      // 检查datasetFormats是否已经是格式化的对象数组
      if (typeof this.datasetFormats[0] === 'object' && this.datasetFormats[0].value) {
        return this.datasetFormats;
      }
      
      // 确保datasetFormats是数组
      if (!Array.isArray(this.datasetFormats)) {
        console.error('datasetFormats不是数组:', this.datasetFormats);
        return [];
      }
      
      // 将简单数组转换为对象数组
      return this.datasetFormats.map(format => {
        return {
          value: format,
          label: format.toUpperCase()
        };
      });
    }
  },
  methods: {
    // 获取数据集列表
    async fetchDatasets() {
      console.log('开始获取数据集列表...')
      try {
        const response = await this.$store.dispatch('dataCenter/fetchDatasets')
        console.log('数据集获取成功:', response)
        
        // 检查返回的数据
        if (Array.isArray(response)) {
          console.log('数据集结果数量:', response.length)
          return response
        } else if (response && response.results && Array.isArray(response.results)) {
          console.log('数据集结果数量:', response.results.length)
          return response.results
        } else {
          console.warn('数据集结果为空或格式不正确:', response)
          return []
        }
      } catch (error) {
        console.error('获取数据集失败:', error)
        this.$message.error('获取数据集失败')
        return []
      }
    },
    
    // 获取数据集格式列表
    fetchDatasetFormats() {
      return this.$store.dispatch('dataCenter/fetchDatasetFormats')
    },
    
    // 处理搜索
    handleSearch() {
      this.currentPage = 1
    },
    
    // 处理格式过滤变化
    handleFormatChange() {
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
    
    // 处理查看数据集
    handleView(dataset) {
      this.$emit('view', dataset)
    },
    
    // 处理创建数据集
    handleCreate() {
      this.dialogType = 'create'
      this.currentDataset = {
        name: '',
        description: '',
        file: null
      }
      this.fileList = []
      this.dialogVisible = true
    },
    
    // 处理编辑数据集
    handleEdit(dataset) {
      this.dialogType = 'edit'
      this.currentDataset = JSON.parse(JSON.stringify(dataset))
      this.$emit('edit', dataset)
    },
    
    // 处理删除数据集
    handleDelete(dataset) {
      this.$confirm('此操作将永久删除该数据集, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('dataCenter/deleteDataset', dataset.id)
          .then(() => {
            this.$message.success('删除数据集成功')
            this.fetchDatasets()
          })
          .catch(error => {
            console.error('删除数据集失败:', error)
            this.$message.error('删除数据集失败')
          })
      }).catch(() => {})
      
      this.$emit('delete', dataset)
    },
    
    // 保存数据集
    saveDataset() {
      this.$refs.datasetForm.validate(valid => {
        if (valid) {
          this.saveLoading = true
          
          if (this.dialogType === 'create') {
            // 创建数据集
            const formData = {
              name: this.currentDataset.name,
              description: this.currentDataset.description
            }
            
            this.$store.dispatch('dataCenter/createDataset', {
              data: formData,
              file: this.currentDataset.file,
              onProgress: this.handleUploadProgress
            })
              .then(() => {
                this.$message.success('上传数据集成功')
                this.dialogVisible = false
                this.fetchDatasets()
                this.saveLoading = false
              })
              .catch(error => {
                console.error('上传数据集失败:', error)
                this.$message.error('上传数据集失败')
                this.saveLoading = false
              })
          } else {
            // 更新数据集
            const updateData = {
              name: this.currentDataset.name,
              description: this.currentDataset.description
            }
            
            this.$store.dispatch('dataCenter/updateDataset', {
              id: this.currentDataset.id,
              data: updateData
            })
              .then(() => {
                this.$message.success('更新数据集成功')
                this.dialogVisible = false
                this.fetchDatasets()
                this.saveLoading = false
              })
              .catch(error => {
                console.error('更新数据集失败:', error)
                this.$message.error('更新数据集失败')
                this.saveLoading = false
              })
          }
        } else {
          return false
        }
      })
    },
    
    // 处理文件上传
    handleFileUpload(options) {
      this.currentDataset.file = options.file
    },
    
    // 上传前检查
    beforeUpload(file) {
      // 检查文件大小，限制为100MB
      const isLt100M = file.size / 1024 / 1024 < 100
      if (!isLt100M) {
        this.$message.error('上传文件大小不能超过 100MB!')
        return false
      }
      return true
    },
    
    // 处理文件移除
    handleRemove() {
      this.currentDataset.file = null
    },
    
    // 处理超出文件数量限制
    handleExceed() {
      this.$message.warning('只能上传一个文件')
    },
    
    // 处理上传进度
    handleUploadProgress(event) {
      console.log('上传进度:', event.percent)
    },
    
    // 重置表单
    resetForm() {
      if (this.$refs.datasetForm) {
        this.$refs.datasetForm.resetFields()
      }
      this.fileList = []
      this.currentDataset = {
        name: '',
        description: '',
        file: null
      }
    },
    
    // 格式化日期
    formatDate(date) {
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    
    // 格式化文件大小
    formatFileSize(size) {
      if (!size && size !== 0) return '未知'
      
      const units = ['B', 'KB', 'MB', 'GB', 'TB']
      let fileSize = size
      let unitIndex = 0
      
      while (fileSize >= 1024 && unitIndex < units.length - 1) {
        fileSize /= 1024
        unitIndex++
      }
      
      return `${fileSize.toFixed(2)} ${units[unitIndex]}`
    },
    
    /**
     * 获取状态标签类型
     * @param {string} status - 数据集状态
     * @returns {string} - 标签类型
     */
    getStatusType(status) {
      const typeMap = {
        'pending': 'info',
        'processing': 'warning',
        'ready': 'success',
        'error': 'danger'
      }
      return typeMap[status] || 'info'
    },
    
    /**
     * 获取状态文本
     * @param {string} status - 数据集状态
     * @returns {string} - 状态文本
     */
    getStatusText(status) {
      const textMap = {
        'pending': '待处理',
        'processing': '处理中',
        'ready': '可用',
        'error': '错误'
      }
      return textMap[status] || '未知'
    },
    
    /**
     * 切换数据集公开状态
     * @param {Object} dataset - 数据集对象
     */
    togglePublic(dataset) {
      this.$confirm(
        `确定要将数据集 "${dataset.name}" 设为${dataset.is_public ? '私有' : '公开'}吗？`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        this.$store.dispatch('dataCenter/toggleDatasetPublic', dataset.id)
          .then(() => {
            this.$message.success(`数据集已设为${dataset.is_public ? '私有' : '公开'}`)
            // 刷新列表
            this.fetchDatasets()
          })
          .catch(error => {
            this.$message.error(`操作失败: ${error.message || '未知错误'}`)
          })
      }).catch(() => {
        // 取消操作
      })
    }
  },
  async created() {
    console.log('DatasetList 组件创建，开始获取数据...')
    try {
      // 获取数据集格式列表
      const formats = await this.fetchDatasetFormats()
      console.log('数据集格式获取成功:', formats)
      
      // 获取数据集列表
      console.log('开始获取数据集列表...')
      const datasets = await this.fetchDatasets()
      console.log('数据集获取成功:', datasets)
      
      // 检查Vuex状态
      console.log('Vuex store数据集状态:', {
        datasets: this.$store.state.dataCenter.datasets,
        inComputed: this.datasets,
        filteredDatasets: this.filteredDatasets,
        pagedDatasets: this.pagedDatasets,
        totalDatasets: this.totalDatasets
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
.dataset-list {
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
  margin-right: 15px;
}

.format-filter {
  width: 150px;
  margin-right: 15px;
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

.upload-demo {
  width: 100%;
}
</style> 