<template>
  <div class="evaluation-center">
    <el-card class="page-header">
      <div class="page-title">
        <h2>模型评测中心</h2>
        <div class="page-description">
          对模型进行全面评测，获取详细的性能报告和优化建议
        </div>
      </div>
    </el-card>
    
    <!-- 顶部操作栏 -->
    <div class="action-bar">
      <el-button type="primary" @click="showCreateTaskDialog">
        <i class="el-icon-plus"></i> 创建评测任务
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="搜索评测任务"
        prefix-icon="el-icon-search"
        clearable
        class="search-input"
      ></el-input>
      <el-select v-model="statusFilter" placeholder="状态筛选" clearable class="filter-select">
        <el-option label="全部" value=""></el-option>
        <el-option label="进行中" value="running"></el-option>
        <el-option label="已完成" value="completed"></el-option>
        <el-option label="失败" value="failed"></el-option>
      </el-select>
    </div>

    <!-- 评测任务列表 -->
    <el-table
      v-loading="loading"
      :data="filteredTasks"
      style="width: 100%"
      border
      stripe
      :default-sort="{ prop: 'createTime', order: 'descending' }"
    >
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="name" label="任务名称" min-width="180">
        <template slot-scope="scope">
          <router-link :to="`/evaluation-center/task/${scope.row.id}`" class="task-name-link">
            {{ scope.row.name }}
          </router-link>
        </template>
      </el-table-column>
      <el-table-column prop="modelName" label="评测模型" min-width="150"></el-table-column>
      <el-table-column prop="datasetName" label="评测数据集" min-width="150"></el-table-column>
      <el-table-column prop="metrics" label="评测指标" min-width="150">
        <template slot-scope="scope">
          <el-tag v-for="metric in scope.row.metrics" :key="metric" size="mini" class="metric-tag">
            {{ metric }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template slot-scope="scope">
          <el-tag :type="getStatusType(scope.row.status)" size="mini">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="progress" label="进度" width="180">
        <template slot-scope="scope">
          <el-progress 
            :percentage="scope.row.progress" 
            :status="getProgressStatus(scope.row.status)"
          ></el-progress>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="创建时间" width="180" sortable>
        <template slot-scope="scope">
          {{ formatDate(scope.row.createTime) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            icon="el-icon-view"
            @click="viewTaskDetails(scope.row.id)"
            circle
          ></el-button>
          <el-button
            size="mini"
            type="danger"
            icon="el-icon-delete"
            @click="confirmDeleteTask(scope.row)"
            circle
            :disabled="scope.row.status === 'running'"
          ></el-button>
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
        :total="totalTasks"
      ></el-pagination>
    </div>

    <!-- 创建评测任务对话框 -->
    <el-dialog title="创建评测任务" :visible.sync="createTaskDialogVisible" width="650px">
      <el-form :model="newTask" :rules="taskRules" ref="taskForm" label-width="120px">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="newTask.name" placeholder="请输入评测任务名称"></el-input>
        </el-form-item>
        <el-form-item label="评测模型" prop="modelId">
          <el-select v-model="newTask.modelId" placeholder="请选择要评测的模型" style="width: 100%">
            <el-option
              v-for="model in availableModels"
              :key="model.id"
              :label="model.name"
              :value="model.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="评测数据集" prop="datasetId">
          <el-select v-model="newTask.datasetId" placeholder="请选择评测数据集" style="width: 100%">
            <el-option
              v-for="dataset in availableDatasets"
              :key="dataset.id"
              :label="dataset.name"
              :value="dataset.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="评测指标" prop="metrics">
          <el-checkbox-group v-model="newTask.metrics">
            <el-checkbox label="accuracy">准确率</el-checkbox>
            <el-checkbox label="precision">精确率</el-checkbox>
            <el-checkbox label="recall">召回率</el-checkbox>
            <el-checkbox label="f1">F1分数</el-checkbox>
            <el-checkbox label="latency">延迟</el-checkbox>
            <el-checkbox label="throughput">吞吐量</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="评测参数" prop="parameters">
          <el-input
            type="textarea"
            v-model="newTask.parameters"
            placeholder="请输入评测参数 (JSON格式)"
            :rows="4"
          ></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            type="textarea"
            v-model="newTask.description"
            placeholder="请输入任务描述"
            :rows="3"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="createTaskDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createTask" :loading="submitting">创建</el-button>
      </span>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      title="确认删除"
      :visible.sync="deleteDialogVisible"
      width="400px"
    >
      <p>确定要删除评测任务 "{{ taskToDelete.name }}" 吗？此操作不可恢复。</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="deleteTask" :loading="deleting">删除</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { formatDate } from '@/utils/dateFormat'

export default {
  name: 'EvaluationCenter',
  data() {
    return {
      // 评测任务列表
      tasks: [],
      loading: true,
      
      // 搜索和筛选
      searchQuery: '',
      statusFilter: '',
      
      // 分页
      currentPage: 1,
      pageSize: 10,
      totalTasks: 0,
      
      // 创建任务对话框
      createTaskDialogVisible: false,
      submitting: false,
      newTask: {
        name: '',
        modelId: '',
        datasetId: '',
        metrics: [],
        parameters: '{}',
        description: ''
      },
      taskRules: {
        name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
        modelId: [{ required: true, message: '请选择评测模型', trigger: 'change' }],
        datasetId: [{ required: true, message: '请选择评测数据集', trigger: 'change' }],
        metrics: [{ type: 'array', required: true, message: '请至少选择一个评测指标', trigger: 'change' }]
      },
      
      // 可选模型和数据集
      availableModels: [],
      availableDatasets: [],
      
      // 删除对话框
      deleteDialogVisible: false,
      deleting: false,
      taskToDelete: {}
    }
  },
  computed: {
    filteredTasks() {
      return this.tasks.filter(task => {
        // 搜索过滤
        const matchesSearch = !this.searchQuery || 
          task.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          task.modelName.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          task.datasetName.toLowerCase().includes(this.searchQuery.toLowerCase());
        
        // 状态过滤
        const matchesStatus = !this.statusFilter || task.status === this.statusFilter;
        
        return matchesSearch && matchesStatus;
      });
    }
  },
  created() {
    this.fetchEvaluationTasks();
    this.fetchAvailableModels();
    this.fetchAvailableDatasets();
  },
  methods: {
    formatDate,
    
    // 获取评测任务列表
    async fetchEvaluationTasks() {
      this.loading = true;
      try {
        // 模拟API调用
        setTimeout(() => {
          this.tasks = [
            {
              id: 1,
              name: 'GPT-4性能评测',
              modelName: 'GPT-4',
              datasetName: 'MMLU数据集',
              metrics: ['accuracy', 'latency'],
              status: 'completed',
              progress: 100,
              createTime: '2023-05-15T10:30:00'
            },
            {
              id: 2,
              name: 'Claude 3性能评测',
              modelName: 'Claude 3',
              datasetName: 'GSM8K数据集',
              metrics: ['accuracy', 'precision', 'recall'],
              status: 'running',
              progress: 65,
              createTime: '2023-05-16T14:20:00'
            },
            {
              id: 3,
              name: 'LLaMA 3性能评测',
              modelName: 'LLaMA 3',
              datasetName: 'HumanEval数据集',
              metrics: ['accuracy', 'f1'],
              status: 'failed',
              progress: 30,
              createTime: '2023-05-14T09:15:00'
            }
          ];
          this.totalTasks = this.tasks.length;
          this.loading = false;
        }, 1000);
        
        // 实际API调用
        // const response = await this.$api.evaluation.getTasks({
        //   page: this.currentPage,
        //   pageSize: this.pageSize
        // });
        // this.tasks = response.data.items;
        // this.totalTasks = response.data.total;
      } catch (error) {
        this.$message.error('获取评测任务列表失败');
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    
    // 获取可用模型列表
    async fetchAvailableModels() {
      try {
        // 从训练中心获取模型列表
        const response = await this.$store.dispatch('trainingCenter/fetchModels');
        this.availableModels = response?.results || response || [];
      } catch (error) {
        this.$message.error('获取模型列表失败');
        console.error(error);
        this.availableModels = [];
      }
    },
    
    // 获取可用数据集列表
    async fetchAvailableDatasets() {
      try {
        // 从数据中心获取数据集列表
        const response = await this.$store.dispatch('dataCenter/fetchDatasets');
        this.availableDatasets = response?.results || response || [];
      } catch (error) {
        this.$message.error('获取数据集列表失败');
        console.error(error);
        this.availableDatasets = [];
      }
    },
    
    // 显示创建任务对话框
    showCreateTaskDialog() {
      this.createTaskDialogVisible = true;
      this.newTask = {
        name: '',
        modelId: '',
        datasetId: '',
        metrics: [],
        parameters: '{}',
        description: ''
      };
      // 在下一个事件循环中重置表单验证
      this.$nextTick(() => {
        if (this.$refs.taskForm) {
          this.$refs.taskForm.resetFields();
        }
      });
    },
    
    // 创建评测任务
    async createTask() {
      this.$refs.taskForm.validate(async (valid) => {
        if (!valid) return;
        
        this.submitting = true;
        try {
          // 验证JSON格式
          try {
            JSON.parse(this.newTask.parameters);
          } catch (e) {
            this.$message.error('评测参数必须是有效的JSON格式');
            this.submitting = false;
            return;
          }
          
          // 模拟API调用
          setTimeout(() => {
            const newTaskId = this.tasks.length + 1;
            const modelName = this.availableModels.find(m => m.id === this.newTask.modelId)?.name || '';
            const datasetName = this.availableDatasets.find(d => d.id === this.newTask.datasetId)?.name || '';
            
            this.tasks.unshift({
              id: newTaskId,
              name: this.newTask.name,
              modelName: modelName,
              datasetName: datasetName,
              metrics: this.newTask.metrics,
              status: 'running',
              progress: 0,
              createTime: new Date().toISOString()
            });
            
            this.totalTasks++;
            this.createTaskDialogVisible = false;
            this.$message.success('评测任务创建成功');
            this.submitting = false;
          }, 1000);
          
          // 实际API调用
          // await this.$api.evaluation.createTask(this.newTask);
          // this.$message.success('评测任务创建成功');
          // this.createTaskDialogVisible = false;
          // this.fetchEvaluationTasks();
        } catch (error) {
          this.$message.error('创建评测任务失败');
          console.error(error);
        } finally {
          this.submitting = false;
        }
      });
    },
    
    // 查看任务详情
    viewTaskDetails(taskId) {
      this.$router.push(`/evaluation-center/task/${taskId}`);
    },
    
    // 确认删除任务
    confirmDeleteTask(task) {
      this.taskToDelete = task;
      this.deleteDialogVisible = true;
    },
    
    // 删除任务
    async deleteTask() {
      this.deleting = true;
      try {
        // 模拟API调用
        setTimeout(() => {
          const index = this.tasks.findIndex(t => t.id === this.taskToDelete.id);
          if (index !== -1) {
            this.tasks.splice(index, 1);
            this.totalTasks--;
          }
          this.deleteDialogVisible = false;
          this.$message.success('评测任务删除成功');
          this.deleting = false;
        }, 1000);
        
        // 实际API调用
        // await this.$api.evaluation.deleteTask(this.taskToDelete.id);
        // this.$message.success('评测任务删除成功');
        // this.fetchEvaluationTasks();
        // this.deleteDialogVisible = false;
      } catch (error) {
        this.$message.error('删除评测任务失败');
        console.error(error);
      } finally {
        this.deleting = false;
      }
    },
    
    // 获取状态类型
    getStatusType(status) {
      switch (status) {
        case 'running': return 'primary';
        case 'completed': return 'success';
        case 'failed': return 'danger';
        default: return 'info';
      }
    },
    
    // 获取状态文本
    getStatusText(status) {
      switch (status) {
        case 'running': return '进行中';
        case 'completed': return '已完成';
        case 'failed': return '失败';
        default: return '未知';
      }
    },
    
    // 获取进度条状态
    getProgressStatus(status) {
      if (status === 'completed') {
        return 'success';
      } else if (status === 'failed') {
        return 'exception';
      } else {
        return ''; // Default for 'running' or any other status
      }
    },
    
    // 分页处理
    handleSizeChange(size) {
      this.pageSize = size;
      this.fetchEvaluationTasks();
    },
    
    handleCurrentChange(page) {
      this.currentPage = page;
      this.fetchEvaluationTasks();
    }
  }
}
</script>

<style scoped>
.evaluation-center {
  padding: 0;
}

.page-header {
  margin-bottom: 20px;
}

.page-title {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.page-title h2 {
  margin: 0 0 10px 0;
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.page-description {
  color: #606266;
  font-size: 14px;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-input {
  width: 250px;
  margin-left: auto;
  margin-right: 15px;
}

.filter-select {
  width: 150px;
}

.task-name-link {
  color: #409EFF;
  text-decoration: none;
  font-weight: 500;
}

.task-name-link:hover {
  text-decoration: underline;
}

.metric-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style> 