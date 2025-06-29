<template>
  <div class="models-manager">
    <div class="toolbar">
      <el-button type="primary" @click="showAddDialog">
        <i class="el-icon-plus"></i> 添加模型
      </el-button>
      
      <el-select 
        v-model="providerFilter" 
        placeholder="按提供商筛选" 
        clearable 
        style="width: 180px; margin-left: 15px;"
        @change="filterModels"
      >
        <el-option
          v-for="provider in providers"
          :key="provider.id"
          :label="provider.name"
          :value="provider.id">
        </el-option>
      </el-select>
    </div>
    
    <el-table 
      :data="filteredModels" 
      border 
      style="width: 100%; margin-top: 20px;"
      v-loading="loading"
    >
      <el-table-column prop="name" label="模型名称"></el-table-column>
      <el-table-column prop="provider_name" label="提供商"></el-table-column>
      <el-table-column prop="model_type_display" label="类型"></el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.is_active ? 'success' : 'info'">
            {{ scope.row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="默认" width="100" align="center">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.is_default" type="warning">默认</el-tag>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250" align="center">
        <template slot-scope="scope">
          <el-button 
            type="primary" 
            size="mini" 
            plain
            @click="editModel(scope.row)"
          >编辑</el-button>
          <el-button 
            type="success" 
            size="mini" 
            plain
            v-if="!scope.row.is_default"
            @click="setAsDefault(scope.row)"
          >设为默认</el-button>
          <el-button 
            type="danger" 
            size="mini" 
            plain
            @click="deleteModel(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 添加/编辑模型对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="50%">
      <el-form 
        :model="formData" 
        :rules="formRules" 
        ref="modelForm" 
        label-width="120px"
      >
        <el-form-item label="模型名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入模型名称"></el-input>
        </el-form-item>
        
        <el-form-item label="提供商" prop="provider_id">
          <el-select v-model="formData.provider_id" placeholder="请选择提供商" style="width: 100%;">
            <el-option
              v-for="provider in providers"
              :key="provider.id"
              :label="provider.name"
              :value="provider.id">
            </el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="模型类型" prop="model_type">
          <el-select v-model="formData.model_type" placeholder="请选择模型类型" style="width: 100%;">
            <el-option
              v-for="item in modelTypes"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="模型标识符" prop="model_identifier">
          <el-input 
            v-model="formData.model_identifier" 
            placeholder="请输入模型在API中的标识符，例如：gpt-4-turbo"
          ></el-input>
          <div class="form-tip">提供商API中使用的实际模型标识符</div>
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input 
            type="textarea" 
            :rows="3" 
            v-model="formData.description" 
            placeholder="请输入模型描述"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="最大令牌数" prop="max_tokens">
          <el-input-number 
            v-model="formData.max_tokens" 
            :min="0" 
            :step="1000" 
            style="width: 180px;"
          ></el-input-number>
          <div class="form-tip">模型支持的最大令牌数（上下文窗口大小）</div>
        </el-form-item>
        
        <el-form-item label="参数配置" prop="params_schema">
          <el-input 
            type="textarea" 
            :rows="5" 
            v-model="formData.params_schema" 
            placeholder="请输入模型参数配置（JSON格式）"
          ></el-input>
          <div class="form-tip">JSON格式的模型参数配置</div>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-switch
            v-model="formData.is_active"
            active-text="启用"
            inactive-text="禁用">
          </el-switch>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveModel" :loading="submitting">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ApiModelsManager',
  data() {
    return {
      models: [],
      filteredModels: [],
      providers: [],
      modelTypes: [],
      loading: false,
      submitting: false,
      dialogVisible: false,
      dialogTitle: '添加模型',
      isEdit: false,
      providerFilter: null,
      formData: this.getDefaultFormData(),
      formRules: {
        name: [
          { required: true, message: '请输入模型名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        provider_id: [
          { required: true, message: '请选择提供商', trigger: 'change' }
        ],
        model_type: [
          { required: true, message: '请选择模型类型', trigger: 'change' }
        ],
        model_identifier: [
          { required: true, message: '请输入模型标识符', trigger: 'blur' }
        ],
        max_tokens: [
          { required: true, message: '请输入最大令牌数', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.loadModelTypes()
    this.loadProviders()
    this.loadModels()
  },
  methods: {
    getDefaultFormData() {
      return {
        name: '',
        provider_id: null,
        model_type: '',
        model_identifier: '',
        description: '',
        max_tokens: 4000,
        params_schema: '{}',
        is_active: true
      }
    },
    async loadModelTypes() {
      try {
        const response = await axios.get('/api/api-connector/models/types/')
        this.modelTypes = response.data || []
      } catch (error) {
        console.error('加载模型类型失败:', error)
        this.$message.error('加载模型类型失败')
      }
    },
    async loadProviders() {
      try {
        const response = await axios.get('/api/api-connector/providers/?all=true')
        this.providers = response.data || []
      } catch (error) {
        console.error('加载API提供商失败:', error)
        this.$message.error('加载API提供商失败')
      }
    },
    async loadModels() {
      this.loading = true
      try {
        const response = await axios.get('/api/api-connector/models/?all=true')
        this.models = response.data || []
        this.filterModels()
      } catch (error) {
        console.error('加载API模型失败:', error)
        this.$message.error('加载API模型失败')
      } finally {
        this.loading = false
      }
    },
    filterModels() {
      if (this.providerFilter) {
        this.filteredModels = this.models.filter(m => m.provider_id === this.providerFilter)
      } else {
        this.filteredModels = [...this.models]
      }
    },
    showAddDialog() {
      this.isEdit = false
      this.dialogTitle = '添加模型'
      this.formData = this.getDefaultFormData()
      this.dialogVisible = true
    },
    editModel(row) {
      this.isEdit = true
      this.dialogTitle = '编辑模型'
      // 复制数据以避免直接修改表格数据
      this.formData = { ...row }
      this.dialogVisible = true
    },
    async saveModel() {
      this.$refs.modelForm.validate(async valid => {
        if (!valid) return
        
        // 尝试解析参数配置确保是有效的JSON
        try {
          JSON.parse(this.formData.params_schema)
        } catch (e) {
          this.$message.error('参数配置必须是有效的JSON格式')
          return
        }
        
        this.submitting = true
        try {
          let response
          if (this.isEdit) {
            // 编辑现有模型
            response = await axios.put(
              `/api/api-connector/models/${this.formData.id}/`,
              this.formData
            )
          } else {
            // 添加新模型
            response = await axios.post(
              '/api/api-connector/models/',
              this.formData
            )
          }
          
          this.$message.success(this.isEdit ? '更新成功' : '添加成功')
          this.dialogVisible = false
          this.loadModels()
        } catch (error) {
          console.error('保存API模型失败:', error)
          this.$message.error('保存失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
        } finally {
          this.submitting = false
        }
      })
    },
    async setAsDefault(row) {
      try {
        await this.$confirm(`确定要将 "${row.name}" 设为默认模型吗？`, '确认操作', {
          type: 'warning'
        })
        
        await axios.post(`/api/api-connector/models/${row.id}/set_default/`)
        this.$message.success('设置默认模型成功')
        this.loadModels()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('设置默认模型失败:', error)
          this.$message.error('设置失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
        }
      }
    },
    async deleteModel(row) {
      try {
        await this.$confirm('确定要删除此模型吗？', '确认删除', {
          type: 'warning'
        })
        
        await axios.delete(`/api/api-connector/models/${row.id}/`)
        this.$message.success('删除成功')
        this.loadModels()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除API模型失败:', error)
          this.$message.error('删除失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
        }
      }
    }
  }
}
</script>

<style scoped>
.models-manager {
  width: 100%;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  line-height: 1.2;
}
</style> 