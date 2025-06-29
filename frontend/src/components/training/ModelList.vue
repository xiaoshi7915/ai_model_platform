<template>
  <div class="model-list">
    <!-- 搜索和操作区域 -->
    <div class="table-actions">
      <el-input
        v-model="searchQuery"
        placeholder="搜索模型名称或描述"
        class="search-input"
        clearable
        @clear="handleSearch"
        @input="handleSearch"
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      
      <el-select 
        v-model="statusFilter" 
        placeholder="状态过滤" 
        clearable 
        @change="handleStatusChange"
        class="status-filter"
      >
        <el-option
          v-for="item in statusOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
      
      <el-button type="primary" @click="handleCreate">
        <i class="el-icon-plus"></i> 创建模型
      </el-button>
    </div>
    
    <!-- 错误信息显示 -->
    <div v-if="error" class="error-message">
      <el-alert :title="error" type="error" show-icon :closable="false"></el-alert>
    </div>
    
    <!-- 模型列表表格 -->
    <el-table
      v-loading="loading"
      :data="filteredModels"
      border
      style="width: 100%"
      @row-click="handleRowClick"
      empty-text="暂无模型数据"
    >
      <el-table-column prop="name" label="模型名称" min-width="150">
        <template slot-scope="scope">
          <el-link type="primary" @click.stop="handleView(scope.row)">
            {{ scope.row.name || '未命名模型' }}
          </el-link>
        </template>
      </el-table-column>
      
      <el-table-column prop="version" label="版本" width="100"></el-table-column>
      
      <el-table-column prop="status" label="状态" width="100">
        <template slot-scope="scope">
          <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="dataset_name" label="训练数据集" width="150"></el-table-column>
      
      <el-table-column prop="created_by_username" label="创建者" width="120"></el-table-column>
      
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="200" fixed="right">
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
            :disabled="!['draft', 'failed'].includes(scope.row.status)"
          >编辑</el-button>
          
          <el-button
            size="mini"
            type="text"
            @click.stop="handleTrain(scope.row)"
            :disabled="scope.row.status === 'training'"
          >训练</el-button>
          
          <el-button
            size="mini"
            type="text"
            class="danger-text"
            @click.stop="handleDelete(scope.row)"
            :disabled="scope.row.status === 'training'"
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
        :total="totalModels"
      ></el-pagination>
    </div>
    
    <!-- 训练对话框 -->
    <el-dialog
      title="开始训练"
      :visible.sync="trainDialogVisible"
      width="600px"
    >
      <div v-if="currentModel">
        <p>您确定要开始训练模型 <strong>{{ currentModel.name }}</strong> (版本: {{ currentModel.version }}) 吗？</p>
        
        <el-form ref="trainForm" :model="trainForm" label-width="120px">
          <el-form-item label="Docker镜像">
            <el-select v-model="trainForm.docker_image_id" placeholder="请选择Docker镜像" style="width: 100%">
              <el-option
                v-for="image in dockerImages"
                :key="image.id"
                :label="`${image.name}:${image.tag}`"
                :value="image.id"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="训练参数">
            <el-input
              type="textarea"
              :rows="5"
              placeholder="请输入训练参数（JSON格式）"
              v-model="trainForm.parameters"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
      
      <div slot="footer" class="dialog-footer">
        <el-button @click="trainDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmTrain" :loading="trainLoading">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'

export default {
  name: 'ModelList',
  data() {
    return {
      searchQuery: '',
      statusFilter: '',
      currentPage: 1,
      pageSize: 10,
      trainDialogVisible: false,
      currentModel: null,
      trainForm: {
        docker_image_id: '',
        parameters: '{}'
      },
      trainLoading: false,
      statusOptions: [
        { value: 'draft', label: '草稿' },
        { value: 'training', label: '训练中' },
        { value: 'completed', label: '已完成' },
        { value: 'failed', label: '失败' }
      ]
    }
  },
  computed: {
    ...mapState({
      models: state => state.trainingCenter.models || [],
      dockerImages: state => state.dockerImages?.dockerImages || [],
      loading: state => state.trainingCenter.loading,
      error: state => state.trainingCenter.error
    }),
    filteredModels() {
      const models = this.models || [];
      
      // 如果有状态过滤
      let filtered = models;
      if (this.statusFilter) {
        filtered = filtered.filter(model => model.status === this.statusFilter);
      }
      
      // 如果有搜索关键词
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(model => 
          (model.name && model.name.toLowerCase().includes(query)) || 
          (model.description && model.description.toLowerCase().includes(query))
        );
      }
      
      return filtered;
    },
    totalModels() {
      return this.filteredModels.length;
    }
  },
  methods: {
    fetchModels() {
      this.$store.dispatch('trainingCenter/fetchModels')
        .catch(error => {
          console.error('获取模型列表失败:', error);
        });
    },
    
    fetchDockerImages() {
      this.$store.dispatch('dockerImages/fetchDockerImages')
        .catch(error => {
          console.error('获取Docker镜像列表失败:', error);
        });
    },
    
    handleSearch() {
      this.currentPage = 1
    },
    
    handleStatusChange() {
      this.currentPage = 1
    },
    
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
    },
    
    handleCurrentChange(page) {
      this.currentPage = page
    },
    
    handleRowClick(row) {
      if (row && row.id) {
        this.handleView(row)
      }
    },
    
    handleView(model) {
      if (model && model.id) {
        this.$emit('view', model)
      }
    },
    
    handleCreate() {
      this.$emit('create')
    },
    
    handleEdit(model) {
      if (model && model.id) {
        this.$emit('edit', model)
      }
    },
    
    handleTrain(model) {
      if (model && model.id) {
        this.currentModel = model
        this.trainForm = {
          docker_image_id: '',
          parameters: JSON.stringify(model.parameters || {}, null, 2)
        }
        this.trainDialogVisible = true
      }
    },
    
    confirmTrain() {
      if (!this.trainForm.docker_image_id) {
        this.$message.warning('请选择Docker镜像')
        return
      }
      
      try {
        const parameters = JSON.parse(this.trainForm.parameters)
        
        this.trainLoading = true
        
        this.$store.dispatch('trainingCenter/trainModel', {
          id: this.currentModel.id,
          data: {
            docker_image_id: this.trainForm.docker_image_id,
            parameters: parameters
          }
        }).then(() => {
          this.$message.success('模型训练任务已提交')
          this.trainDialogVisible = false
          this.fetchModels()
        }).catch(error => {
          console.error('训练模型失败:', error)
          this.$message.error('训练模型失败')
        }).finally(() => {
          this.trainLoading = false
        })
      } catch (error) {
        this.$message.error('训练参数格式不正确，请输入有效的JSON格式')
      }
    },
    
    handleDelete(model) {
      if (!model || !model.id) return;
      
      this.$confirm('此操作将永久删除该模型, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('trainingCenter/deleteModel', model.id)
          .then(() => {
            this.$message.success('删除模型成功')
            this.fetchModels()
          })
          .catch(error => {
            console.error('删除模型失败:', error)
            this.$message.error('删除模型失败')
          })
      }).catch(() => {})
    },
    
    getStatusType(status) {
      const types = {
        'draft': 'info',
        'training': 'warning',
        'completed': 'success',
        'failed': 'danger'
      }
      return types[status] || 'info'
    },
    
    getStatusText(status) {
      const texts = {
        'draft': '草稿',
        'training': '训练中',
        'completed': '已完成',
        'failed': '失败'
      }
      return texts[status] || status
    },
    
    formatDate(date) {
      if (!date) return ''; 
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    }
  },
  created() {
    this.fetchModels()
    this.fetchDockerImages()
  }
}
</script>

<style scoped>
.model-list {
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

.status-filter {
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

.error-message {
  margin-bottom: 15px;
}
</style> 