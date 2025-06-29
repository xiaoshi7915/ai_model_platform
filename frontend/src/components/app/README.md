# 应用中心组件

本目录包含应用中心相关的所有组件，用于实现应用部署和插件管理功能。

## 组件结构

```
app/
├── ApplicationDetail.vue    # 应用详情组件
├── ApplicationForm.vue      # 应用表单组件
├── ApplicationList.vue      # 应用列表组件
├── ApplicationManagement.vue # 应用管理组件
├── PluginDetail.vue         # 插件详情组件
├── PluginForm.vue           # 插件表单组件
├── PluginList.vue           # 插件列表组件
├── PluginManagement.vue     # 插件管理组件
└── README.md                # 组件说明文档
```

## 组件说明

### 应用管理组件

#### ApplicationManagement.vue

应用管理主组件，包含应用列表和创建应用按钮。

**功能特点：**
- 集成应用列表组件
- 提供创建应用按钮
- 处理应用搜索和筛选

#### ApplicationList.vue

应用列表组件，显示所有应用。

**功能特点：**
- 显示应用列表
- 支持搜索和状态筛选
- 提供应用操作按钮（查看、启动、停止、删除）

#### ApplicationForm.vue

应用表单组件，用于创建和编辑应用。

**功能特点：**
- 提供应用表单
- 支持选择模型
- 配置应用参数

#### ApplicationDetail.vue

应用详情组件，用于展示应用的详细信息和操作。

**功能特点：**
- 显示应用基本信息（名称、状态、模型等）
- 显示应用配置信息
- 提供应用操作（启动、停止、删除等）
- 显示应用监控信息（CPU、内存、请求数等）
- 显示应用日志（运行日志、错误日志）

### 插件管理组件

#### PluginManagement.vue

插件管理主组件，包含插件列表和创建插件按钮。

**功能特点：**
- 集成插件列表组件
- 提供创建插件按钮
- 处理插件搜索和筛选

#### PluginList.vue

插件列表组件，显示所有插件。

**功能特点：**
- 显示插件列表
- 支持搜索和版本筛选
- 提供插件操作按钮（查看、安装、删除）

#### PluginForm.vue

插件表单组件，用于创建和编辑插件。

**功能特点：**
- 提供插件表单
- 支持上传插件文件
- 配置插件兼容性信息

#### PluginDetail.vue

插件详情组件，用于展示插件的详细信息和操作。

**功能特点：**
- 显示插件基本信息（名称、版本、描述等）
- 显示插件兼容性信息
- 显示插件使用情况
- 提供插件操作（安装到应用、删除等）

## 使用方法

### 应用管理

```vue
<template>
  <div class="app-center-view">
    <el-tabs v-model="activeTab" type="card" @tab-click="handleTabClick">
      <el-tab-pane label="应用管理" name="applications">
        <application-management />
      </el-tab-pane>
      
      <el-tab-pane label="插件管理" name="plugins">
        <plugin-management />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import ApplicationManagement from '@/components/app/ApplicationManagement.vue'
import PluginManagement from '@/components/app/PluginManagement.vue'

export default {
  components: {
    ApplicationManagement,
    PluginManagement
  },
  data() {
    return {
      activeTab: 'applications'
    }
  },
  methods: {
    handleTabClick(tab) {
      let path = '/app'
      if (this.activeTab === 'plugins') {
        path = '/app/plugins'
      } else {
        path = '/app/applications'
      }
      
      if (this.$route.path !== path) {
        this.$router.push(path)
      }
    }
  }
}
</script>
```

### 应用详情

```vue
<template>
  <div class="application-detail">
    <el-page-header @back="goBack" :content="application.name || '应用详情'"></el-page-header>
    
    <!-- 应用信息卡片 -->
    <el-card class="detail-card">
      <!-- 应用信息内容 -->
    </el-card>
    
    <!-- 操作按钮 -->
    <el-card class="detail-card">
      <div class="action-buttons">
        <el-button type="primary" @click="handleStart">启动应用</el-button>
        <el-button type="warning" @click="handleStop">停止应用</el-button>
        <el-button type="danger" @click="handleDelete">删除应用</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getApplication, startApplication, stopApplication, deleteApplication } from '@/api/application'

export default {
  data() {
    return {
      application: {
        id: null,
        name: '',
        // 其他应用属性
      }
    }
  },
  created() {
    this.fetchApplicationDetail()
  },
  methods: {
    async fetchApplicationDetail() {
      const id = this.$route.params.id
      const response = await getApplication(id)
      this.application = response.data
    },
    // 其他方法
  }
}
</script>
```

### 插件详情

```vue
<template>
  <div class="plugin-detail">
    <el-page-header @back="goBack" :content="plugin.name || '插件详情'"></el-page-header>
    
    <!-- 插件信息卡片 -->
    <el-card class="detail-card">
      <!-- 插件信息内容 -->
    </el-card>
    
    <!-- 操作按钮 -->
    <el-card class="detail-card">
      <div class="action-buttons">
        <el-button type="primary" @click="handleInstall">安装到应用</el-button>
        <el-button type="danger" @click="handleDelete">删除插件</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getPlugin, deletePlugin, installPlugin } from '@/api/plugin'

export default {
  data() {
    return {
      plugin: {
        id: null,
        name: '',
        // 其他插件属性
      }
    }
  },
  created() {
    this.fetchPluginDetail()
  },
  methods: {
    async fetchPluginDetail() {
      const id = this.$route.params.id
      const response = await getPlugin(id)
      this.plugin = response.data
    },
    // 其他方法
  }
}
</script>
```

## API 接口

应用中心组件使用以下API接口与后端交互：

### 应用管理接口

- `getApplications` - 获取应用列表
- `getApplication` - 获取应用详情
- `createApplication` - 创建应用
- `updateApplication` - 更新应用
- `deleteApplication` - 删除应用
- `startApplication` - 启动应用
- `stopApplication` - 停止应用
- `getApplicationLogs` - 获取应用日志
- `getApplicationMonitoring` - 获取应用监控数据

### 插件管理接口

- `getPlugins` - 获取插件列表
- `getPlugin` - 获取插件详情
- `createPlugin` - 创建插件
- `updatePlugin` - 更新插件
- `deletePlugin` - 删除插件
- `installPlugin` - 安装插件到应用
- `uninstallPlugin` - 从应用卸载插件

## 注意事项

1. 应用启动和停止操作可能需要一定时间，请实现状态轮询或WebSocket实时更新
2. 监控数据应定期刷新，建议使用定时器或WebSocket实现实时更新
3. 图表组件使用ECharts，确保正确配置图表选项
4. 应用日志可能较长，建议实现分页加载或滚动加载

## 更新日志

### 2024-03-12

- 优化应用中心组件结构，统一组件路径
- 改进路由配置，优化页面加载性能
- 添加应用监控功能，支持CPU、内存、请求数和响应时间监控

### 2024-03-11

- 完善应用详情页面，添加日志查看功能
- 优化插件详情页面，添加兼容性信息显示
- 改进应用列表，添加搜索和状态筛选功能 