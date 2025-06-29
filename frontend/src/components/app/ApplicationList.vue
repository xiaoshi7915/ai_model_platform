<template>
  <div class="application-list">
    <div class="list-header">
      <el-row type="flex" justify="space-between" align="middle">
        <el-col :span="12">
          <h2>应用列表</h2>
        </el-col>
        <el-col :span="12" class="header-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索应用名称"
            prefix-icon="el-icon-search"
            clearable
            @clear="handleSearch"
            @keyup.enter.native="handleSearch"
            style="width: 220px; margin-right: 16px;"
          ></el-input>
          <el-button-group>
            <el-button 
              type="primary" 
              icon="el-icon-plus" 
              @click="handleCreate"
            >创建应用</el-button>
            <el-button 
              type="success" 
              icon="el-icon-magic-stick" 
              @click="handleCreateWithWizard"
            >向导创建</el-button>
          </el-button-group>
        </el-col>
      </el-row>
    </div>

    <el-table
      v-loading="loading"
      :data="filteredApplications"
      border
      style="width: 100%"
      @row-click="handleRowClick"
    >
      <el-table-column prop="name" label="应用名称" min-width="150">
        <template slot-scope="scope">
          <el-link type="primary" @click.stop="handleViewDetail(scope.row)">{{ scope.row.name }}</el-link>
        </template>
      </el-table-column>
      
      <el-table-column prop="model_name" label="使用模型" min-width="120"></el-table-column>
      
      <el-table-column prop="status" label="状态" width="100">
        <template slot-scope="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="created_by_username" label="创建者" width="120"></el-table-column>
      
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="api_endpoint" label="API地址" min-width="200">
        <template slot-scope="scope">
          <div v-if="scope.row.api_endpoint" class="endpoint-cell">
            <el-tooltip effect="dark" content="点击复制" placement="top">
              <span class="endpoint-text" @click.stop="copyEndpoint(scope.row.api_endpoint)">
                {{ scope.row.api_endpoint }}
              </span>
            </el-tooltip>
            <el-button 
              type="text" 
              icon="el-icon-document-copy" 
              @click.stop="copyEndpoint(scope.row.api_endpoint)"
            ></el-button>
          </div>
          <span v-else>-</span>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="200" fixed="right">
        <template slot-scope="scope">
          <el-button-group>
            <el-button 
              size="mini" 
              type="primary" 
              icon="el-icon-view"
              @click.stop="handleViewDetail(scope.row)"
            >详情</el-button>
            
            <el-dropdown split-button size="mini" type="primary" @click="handleMoreActions(scope.row)" @command="command => handleCommand(command, scope.row)">
              <i class="el-icon-more"></i>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="edit" :disabled="!canEdit(scope.row)">
                  <i class="el-icon-edit"></i> 编辑
                </el-dropdown-item>
                <el-dropdown-item command="deploy" :disabled="!canDeploy(scope.row)">
                  <i class="el-icon-video-play"></i> 部署
                </el-dropdown-item>
                <el-dropdown-item command="stop" :disabled="!canStop(scope.row)">
                  <i class="el-icon-video-pause"></i> 停止
                </el-dropdown-item>
                <el-dropdown-item command="delete" divided>
                  <i class="el-icon-delete"></i> 删除
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalItems"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import moment from 'moment';

export default {
  name: 'ApplicationList',
  data() {
    return {
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      loading: false,
      total: 0,
      totalItems: 0
    }
  },
  computed: {
    ...mapState({
      applications: state => state.appCenter.applications || [],
      isLoading: state => state.appCenter.loading
    }),
    filteredApplications() {
      if (!Array.isArray(this.applications)) return []
      return this.applications.filter(app => {
        if (!this.searchQuery) return true
        const searchLower = this.searchQuery.toLowerCase()
        return (app.name && app.name.toLowerCase().includes(searchLower)) ||
               (app.description && app.description.toLowerCase().includes(searchLower))
      })
    }
  },
  watch: {
    applications: {
      handler(newVal) {
        if (Array.isArray(newVal)) {
          this.totalItems = newVal.length
          this.total = newVal.length
        }
      },
      immediate: true
    }
  },
  methods: {
    ...mapActions({
      fetchApplications: 'appCenter/fetchApplications',
      deleteApplication: 'appCenter/deleteApplication',
      deployApplication: 'appCenter/deployApplication',
      stopApplication: 'appCenter/stopApplication'
    }),
    async init() {
      try {
        await this.fetchApplications()
      } catch (error) {
        console.error('获取应用列表失败:', error)
        this.$message.error('获取应用列表失败')
      }
    },
    handleCurrentChange(page) {
      this.currentPage = page
      this.fetchApplications({
        page: this.currentPage,
        pageSize: this.pageSize
      })
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
      this.fetchApplications({
        page: this.currentPage,
        pageSize: this.pageSize
      })
    },
    getStatusType(status) {
      const statusMap = {
        'running': 'success',
        'stopped': 'info',
        'created': 'warning',
        'failed': 'danger'
      }
      return statusMap[status] || 'info'
    },
    formatDate(date) {
      if (!date) return '未知'
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    handleSearch() {
      this.currentPage = 1;
      this.fetchApplications({
        page: this.currentPage,
        pageSize: this.pageSize
      });
    },
    handleCreate() {
      this.$emit('create');
    },
    handleCreateWithWizard() {
      this.$emit('create-wizard');
    },
    handleViewDetail(row) {
      this.$emit('view', row.id);
    },
    handleRowClick(row) {
      this.handleViewDetail(row);
    },
    handleMoreActions(row) {
      // Default action for the split button
      this.handleViewDetail(row);
    },
    async handleCommand(command, row) {
      switch (command) {
        case 'edit':
          this.$emit('edit', row.id);
          break;
        case 'deploy':
          this.handleDeploy(row);
          break;
        case 'stop':
          this.handleStop(row);
          break;
        case 'delete':
          this.handleDelete(row);
          break;
      }
    },
    async handleDeploy(row) {
      try {
        this.loading = true;
        await this.deployApplication(row.id);
        this.$message.success(`已开始部署应用: ${row.name}`);
        this.fetchApplications({
          page: this.currentPage,
          pageSize: this.pageSize
        });
      } catch (error) {
        console.error('Failed to deploy application:', error);
        this.$message.error(`部署应用失败: ${error.message || '未知错误'}`);
      } finally {
        this.loading = false;
      }
    },
    async handleStop(row) {
      try {
        this.loading = true;
        await this.stopApplication(row.id);
        this.$message.success(`已停止应用: ${row.name}`);
        this.fetchApplications({
          page: this.currentPage,
          pageSize: this.pageSize
        });
      } catch (error) {
        console.error('Failed to stop application:', error);
        this.$message.error(`停止应用失败: ${error.message || '未知错误'}`);
      } finally {
        this.loading = false;
      }
    },
    async handleDelete(row) {
      this.$confirm(`确定要删除应用 "${row.name}" 吗?`, '删除确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          this.loading = true;
          await this.deleteApplication(row.id);
          this.$message.success(`应用已删除: ${row.name}`);
          this.fetchApplications({
            page: this.currentPage,
            pageSize: this.pageSize
          });
        } catch (error) {
          console.error('Failed to delete application:', error);
          this.$message.error(`删除应用失败: ${error.message || '未知错误'}`);
        } finally {
          this.loading = false;
        }
      }).catch(() => {
        // 用户取消删除
      });
    },
    getStatusText(status) {
      const statusMap = {
        'pending': '待部署',
        'deploying': '部署中',
        'running': '运行中',
        'stopping': '停止中',
        'stopped': '已停止',
        'failed': '失败'
      };
      return statusMap[status] || status;
    },
    copyEndpoint(endpoint) {
      navigator.clipboard.writeText(endpoint)
        .then(() => {
          this.$message.success('API地址已复制到剪贴板');
        })
        .catch(() => {
          this.$message.error('复制失败，请手动复制');
        });
    },
    canEdit(row) {
      return ['stopped', 'pending', 'failed'].includes(row.status);
    },
    canDeploy(row) {
      return ['stopped', 'pending', 'failed'].includes(row.status);
    },
    canStop(row) {
      return ['running', 'deploying'].includes(row.status);
    }
  },
  created() {
    this.init()
  }
};
</script>

<style scoped>
.application-list {
  padding: 20px;
}

.list-header {
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.endpoint-cell {
  display: flex;
  align-items: center;
  max-width: 100%;
}

.endpoint-text {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
  font-family: monospace;
  font-size: 12px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style> 