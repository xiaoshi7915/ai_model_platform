<template>
  <div class="plugin-list">
    <!-- 搜索和过滤区域 -->
    <div class="table-actions">
      <el-input
        v-model="searchQuery"
        placeholder="搜索插件名称"
        class="search-input"
        clearable
        @clear="handleSearch"
        @input="handleSearch"
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      
      <el-button type="primary" @click="handleCreate">
        <i class="el-icon-plus"></i> 上传插件
      </el-button>
    </div>

    <!-- 插件列表表格 -->
    <el-table
      v-loading="loading"
      :data="filteredPlugins"
      border
      style="width: 100%"
    >
      <el-table-column prop="name" label="插件名称" min-width="150">
        <template slot-scope="scope">
          <el-link type="primary" @click="handleDetail(scope.row)">{{ scope.row.name }}</el-link>
        </template>
      </el-table-column>
      
      <el-table-column prop="version" label="版本" width="100"></el-table-column>
      
      <el-table-column label="兼容性" min-width="150">
        <template slot-scope="scope">
          <el-tag
            v-for="(value, key) in scope.row.compatibility"
            :key="key"
            size="mini"
            style="margin-right: 5px; margin-bottom: 5px;"
          >{{ key }}: {{ value }}</el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="200" fixed="right">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            @click="handleEdit(scope.row)"
          >编辑</el-button>
          
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.row)"
          >删除</el-button>
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
        :total="total"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import moment from 'moment'

export default {
  name: 'PluginList',
  data() {
    return {
      loading: false,
      searchQuery: '',
      currentPage: 1,
      pageSize: 10
    }
  },
  computed: {
    ...mapState({
      plugins: state => state.appCenter.plugins || []
    }),
    filteredPlugins() {
      // Ensure plugins is always an array
      let result = Array.isArray(this.plugins) ? this.plugins : [];

      // 搜索过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(plugin => 
          (plugin.name && plugin.name.toLowerCase().includes(query)) ||
          (plugin.version && plugin.version.toLowerCase().includes(query)) ||
          (plugin.description && plugin.description.toLowerCase().includes(query))
        );
      }

      // 分页
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return result.slice(start, end);
    },
    total() {
      return Array.isArray(this.plugins) ? this.plugins.length : 0;
    }
  },
  methods: {
    ...mapActions('appCenter', ['fetchPlugins']),
    
    // 格式化日期
    formatDate(date) {
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    
    // 处理搜索
    handleSearch() {
      this.currentPage = 1
    },
    
    // 处理页码变化
    handleCurrentChange(val) {
      this.currentPage = val
    },
    
    // 处理每页数量变化
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
    },
    
    // 处理创建插件
    handleCreate() {
      this.$emit('create')
    },
    
    // 处理查看详情
    handleDetail(plugin) {
      this.$emit('detail', plugin)
    },
    
    // 处理编辑插件
    handleEdit(plugin) {
      this.$emit('edit', plugin)
    },
    
    // 处理删除插件
    handleDelete(plugin) {
      this.$confirm('此操作将永久删除该插件, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', plugin)
      }).catch(() => {})
    }
  },
  created() {
    this.loading = true
    this.fetchPlugins().finally(() => {
      this.loading = false
    })
  }
}
</script>

<style scoped>
.plugin-list {
  padding: 20px;
}

.table-actions {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-input {
  width: 200px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 