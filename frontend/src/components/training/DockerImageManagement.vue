<template>
  <div class="docker-image-management">
    <div v-loading="loading">
      <!-- 搜索和操作区域 -->
      <div class="table-actions">
        <el-input
          v-model="searchQuery"
          placeholder="搜索镜像名称或标签"
          class="search-input"
          clearable
          @clear="handleSearch"
          @input="handleSearch"
        >
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
        
        <el-button type="primary" @click="handleCreate">
          <i class="el-icon-plus"></i> 添加镜像
        </el-button>
      </div>
      
      <!-- Docker镜像列表表格 -->
      <el-table
        v-if="filteredImages && filteredImages.length"
        :data="filteredImages"
        border
        style="width: 100%"
      >
        <el-table-column prop="name" label="镜像名称" min-width="150"></el-table-column>
        
        <el-table-column prop="tag" label="标签" width="120"></el-table-column>
        
        <el-table-column prop="registry" label="仓库" min-width="150"></el-table-column>
        
        <el-table-column prop="size" label="大小" width="100">
          <template slot-scope="scope">
            {{ scope.row.size }} MB
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
              @click="handleEdit(scope.row)"
            >编辑</el-button>
            
            <el-button
              size="mini"
              type="text"
              class="danger-text"
              @click="handleDelete(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty v-else description="暂无数据"></el-empty>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalImages"
        ></el-pagination>
      </div>
      
      <!-- Docker镜像表单对话框 -->
      <el-dialog
        :title="dialogType === 'create' ? '添加Docker镜像' : '编辑Docker镜像'"
        :visible.sync="dialogVisible"
        width="600px"
        @closed="resetForm"
      >
        <el-form
          ref="imageForm"
          :model="currentImage"
          :rules="rules"
          label-width="100px"
        >
          <el-form-item label="镜像名称" prop="name">
            <el-input v-model="currentImage.name" placeholder="请输入镜像名称"></el-input>
          </el-form-item>
          
          <el-form-item label="标签" prop="tag">
            <el-input v-model="currentImage.tag" placeholder="请输入标签"></el-input>
          </el-form-item>
          
          <el-form-item label="仓库" prop="registry">
            <el-input v-model="currentImage.registry" placeholder="请输入仓库地址"></el-input>
          </el-form-item>
          
          <el-form-item label="大小(MB)" prop="size">
            <el-input-number v-model="currentImage.size" :min="1" :max="100000"></el-input-number>
          </el-form-item>
          
          <el-form-item label="描述" prop="description">
            <el-input
              v-model="currentImage.description"
              type="textarea"
              :rows="4"
              placeholder="请输入镜像描述"
            ></el-input>
          </el-form-item>
        </el-form>
        
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveImage" :loading="saveLoading">确定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'

export default {
  name: 'DockerImageManagement',
  data() {
    return {
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      dialogType: 'create', // 'create' 或 'edit'
      currentImage: {
        name: '',
        tag: '',
        registry: 'docker.io',
        size: 1000,
        description: ''
      },
      saveLoading: false,
      rules: {
        name: [
          { required: true, message: '请输入镜像名称', trigger: 'blur' },
          { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
        ],
        tag: [
          { required: true, message: '请输入标签', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        registry: [
          { required: true, message: '请输入仓库地址', trigger: 'blur' }
        ],
        size: [
          { required: true, message: '请输入镜像大小', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapState({
      dockerImages: state => state.trainingCenter.dockerImages,
      loading: state => state.trainingCenter.loading,
      totalCount: state => state.trainingCenter.total
    }),
    totalImages() {
      return this.totalCount || 0;
    },
    filteredImages() {
      const images = this.dockerImages || []
      if (!this.searchQuery) {
        return images
      }
      const query = this.searchQuery.toLowerCase()
      return images.filter(image => 
        (image.name && image.name.toLowerCase().includes(query)) ||
        (image.tag && image.tag.toLowerCase().includes(query)) ||
        (image.registry && image.registry.toLowerCase().includes(query))
      )
    }
  },
  methods: {
    // 获取Docker镜像列表
    fetchDockerImages() {
      const params = {
        page: this.currentPage,
        page_size: this.pageSize
      };
      
      // 如果有搜索查询则添加搜索参数
      if (this.searchQuery) {
        params.search = this.searchQuery;
      }
      
      return this.$store.dispatch('trainingCenter/fetchDockerImages', params)
        .catch(error => {
          console.error('获取Docker镜像列表失败:', error)
          this.$message.error('获取Docker镜像列表失败')
        })
    },
    
    // 处理搜索
    handleSearch() {
      this.currentPage = 1;
      this.fetchDockerImages();
    },
    
    // 处理页面大小变化
    handleSizeChange(size) {
      this.pageSize = size;
      this.currentPage = 1;
      this.fetchDockerImages();
    },
    
    // 处理当前页变化
    handleCurrentChange(page) {
      this.currentPage = page;
      this.fetchDockerImages();
    },
    
    // 处理创建Docker镜像
    handleCreate() {
      this.dialogType = 'create'
      this.currentImage = {
        name: '',
        tag: '',
        registry: 'docker.io',
        size: 1000,
        description: ''
      }
      this.dialogVisible = true
    },
    
    // 处理编辑Docker镜像
    handleEdit(image) {
      this.dialogType = 'edit'
      this.currentImage = JSON.parse(JSON.stringify(image))
      this.dialogVisible = true
    },
    
    // 保存Docker镜像
    saveImage() {
      this.$refs.imageForm.validate(valid => {
        if (valid) {
          this.saveLoading = true;
          
          if (this.dialogType === 'create') {
            // 创建Docker镜像
            this.$store.dispatch('trainingCenter/createDockerImage', this.currentImage)
              .then(() => {
                this.$message.success('添加Docker镜像成功');
                this.dialogVisible = false;
                this.fetchDockerImages();
                this.saveLoading = false;
              })
              .catch(error => {
                console.error('添加Docker镜像失败:', error);
                
                // 处理超时错误
                if (error.code === 'ECONNABORTED' && error.message.includes('timeout')) {
                  this.$message({
                    message: '请求超时，但操作可能已成功，正在刷新列表...',
                    type: 'warning'
                  });
                  this.dialogVisible = false;
                  
                  // 延迟刷新列表，给服务器一些处理时间
                  setTimeout(() => {
                    this.fetchDockerImages();
                  }, 2000);
                } else {
                  this.$message.error('添加Docker镜像失败');
                }
                
                this.saveLoading = false;
              });
          } else {
            // 更新Docker镜像
            this.$store.dispatch('trainingCenter/updateDockerImage', {
              id: this.currentImage.id,
              imageData: this.currentImage
            })
              .then(() => {
                this.$message.success('更新Docker镜像成功');
                this.dialogVisible = false;
                this.fetchDockerImages();
                this.saveLoading = false;
              })
              .catch(error => {
                console.error('更新Docker镜像失败:', error);
                
                // 处理超时错误
                if (error.code === 'ECONNABORTED' && error.message.includes('timeout')) {
                  this.$message({
                    message: '请求超时，但操作可能已成功，正在刷新列表...',
                    type: 'warning'
                  });
                  this.dialogVisible = false;
                  
                  // 延迟刷新列表，给服务器一些处理时间
                  setTimeout(() => {
                    this.fetchDockerImages();
                  }, 2000);
                } else {
                  this.$message.error('更新Docker镜像失败');
                }
                
                this.saveLoading = false;
              });
          }
        } else {
          return false;
        }
      });
    },
    
    // 处理删除Docker镜像
    handleDelete(image) {
      this.$confirm('此操作将永久删除该Docker镜像, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('trainingCenter/deleteDockerImage', image.id)
          .then(() => {
            this.$message.success('删除Docker镜像成功')
            this.fetchDockerImages()
          })
          .catch(error => {
            console.error('删除Docker镜像失败:', error)
            this.$message.error('删除Docker镜像失败')
          })
      }).catch(() => {})
    },
    
    // 重置表单
    resetForm() {
      if (this.$refs.imageForm) {
        this.$refs.imageForm.resetFields()
      }
    },
    
    // 格式化日期
    formatDate(date) {
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    }
  },
  created() {
    this.$store.dispatch('trainingCenter/fetchDockerImages')
      .catch(error => {
        console.error('获取Docker镜像列表失败:', error)
        this.$message.error('获取Docker镜像列表失败')
      })
  }
}
</script>

<style scoped>
.docker-image-management {
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
</style> 