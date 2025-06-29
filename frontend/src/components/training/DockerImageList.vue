<template>
  <div class="docker-image-list">
    <!-- 搜索和操作区域 -->
    <div class="table-actions">
      <el-input
        v-model="searchQuery"
        placeholder="搜索镜像名称、标签或仓库"
        class="search-input"
        clearable
        @clear="fetchDockerImages"
        @keyup.enter.native="fetchDockerImages"
      >
        <el-button slot="append" icon="el-icon-search" @click="fetchDockerImages"></el-button>
      </el-input>
      
      <div>
        <el-button type="primary" @click="handleCreate">添加镜像</el-button>
      </div>
    </div>

    <!-- 镜像列表表格 -->
    <el-table
      v-loading="loading"
      :data="filteredImages"
      border
      style="width: 100%"
      @sort-change="handleSortChange"
    >
      <el-table-column
        prop="name"
        label="名称"
        width="180"
        sortable="custom"
      ></el-table-column>
      
      <el-table-column
        prop="tag"
        label="标签"
        width="150"
      ></el-table-column>
      
      <el-table-column
        prop="registry"
        label="仓库"
        width="180"
      ></el-table-column>
      
      <el-table-column
        prop="size"
        label="大小"
        width="100"
        sortable="custom"
      >
        <template slot-scope="scope">
          {{ scope.row.size }} MB
        </template>
      </el-table-column>
      
      <el-table-column
        prop="created_by_username"
        label="创建者"
        width="120"
      ></el-table-column>
      
      <el-table-column
        prop="created_at"
        label="创建时间"
        width="180"
        sortable="custom"
      >
        <template slot-scope="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      
      <el-table-column
        label="操作"
        width="150"
        fixed="right"
      >
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            icon="el-icon-edit"
            @click="handleEdit(scope.row)"
            circle
          ></el-button>
          <el-button
            size="mini"
            type="danger"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            circle
          ></el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页器 -->
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalCount"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'

export default {
  name: 'DockerImageList',
  data() {
    return {
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      sortBy: 'created_at',
      sortOrder: 'descending'
    }
  },
  computed: {
    ...mapState({
      dockerImages: state => state.dockerImages.dockerImages,
      loading: state => state.dockerImages.loading,
      error: state => state.dockerImages.error,
      totalCount: state => state.dockerImages.count
    }),
    
    // 过滤的镜像列表
    filteredImages() {
      if (!this.searchQuery) {
        return this.dockerImages
      }
      
      const query = this.searchQuery.toLowerCase()
      
      return this.dockerImages.filter(image => {
        return (image.name && image.name.toLowerCase().includes(query)) ||
               (image.tag && image.tag.toLowerCase().includes(query)) ||
               (image.registry && image.registry.toLowerCase().includes(query))
      })
    }
  },
  methods: {
    // 获取Docker镜像列表
    fetchDockerImages() {
      const params = {
        page: this.currentPage,
        page_size: this.pageSize
      }
      
      // 添加排序参数
      if (this.sortBy) {
        params.ordering = this.sortOrder === 'descending' ? `-${this.sortBy}` : this.sortBy
      }
      
      // 添加搜索参数
      if (this.searchQuery) {
        params.search = this.searchQuery
      }
      
      this.$store.dispatch('dockerImages/fetchDockerImages', params)
        .catch(error => {
          console.error('获取Docker镜像列表失败:', error)
          this.$message.error('获取Docker镜像列表失败')
        })
    },
    
    // 创建Docker镜像
    handleCreate() {
      this.$emit('create')
    },
    
    // 编辑Docker镜像
    handleEdit(image) {
      this.$emit('edit', image)
    },
    
    // 删除Docker镜像
    handleDelete(image) {
      this.$confirm('此操作将永久删除该Docker镜像, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('dockerImages/deleteDockerImage', image.id)
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
    
    // 处理页码变化
    handleCurrentChange(page) {
      this.currentPage = page
      this.fetchDockerImages()
    },
    
    // 处理每页数量变化
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
      this.fetchDockerImages()
    },
    
    // 处理排序变化
    handleSortChange({ prop, order }) {
      if (prop) {
        this.sortBy = prop
        this.sortOrder = order
      } else {
        this.sortBy = 'created_at'
        this.sortOrder = 'descending'
      }
      this.fetchDockerImages()
    },
    
    // 格式化日期
    formatDate(date) {
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    }
  },
  created() {
    this.fetchDockerImages()
  }
}
</script>

<style scoped>
.docker-image-list {
  padding: 20px;
}

.table-actions {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-input {
  width: 300px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 