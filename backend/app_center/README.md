# 应用中心模块说明文档

## 概述

应用中心模块是用于管理应用部署和插件的核心功能区域，通过该模块用户可以快速创建、部署和管理基于已训练好的模型的应用实例。

## 模块架构

### 后端架构

#### 数据模型

应用中心模块主要包含以下核心数据模型：

1. **Application (应用)**: 
   - 核心字段：id, name, description, status, model(关联Model模型), endpoint, config
   - 状态选项：stopped(已停止), running(运行中), error(错误)

2. **Plugin (插件)**:
   - 核心字段：id, name, version, description, status
   - 状态选项：enabled(启用), disabled(禁用)

3. **ApplicationPlugin (应用插件)**:
   - 核心字段：application(关联Application), plugin(关联Plugin), config, enabled
   - 记录应用与插件的关联关系

4. **ApplicationLog (应用日志)**:
   - 核心字段：application, timestamp, level, message
   - 记录应用的运行日志

5. **ApplicationMetric (应用监控)**:
   - 核心字段：application, timestamp, cpu_usage, memory_usage, request_count, avg_response_time, error_rate
   - 记录应用的监控指标数据

#### API接口

应用中心提供以下核心API接口：

1. **应用管理**:
   - GET /app-center/applications/：获取应用列表
   - GET /app-center/applications/{id}/：获取应用详情
   - POST /app-center/applications/：创建应用
   - PUT /app-center/applications/{id}/：更新应用
   - DELETE /app-center/applications/{id}/：删除应用
   - POST /app-center/applications/{id}/deploy/：部署应用
   - POST /app-center/applications/{id}/stop/：停止应用

2. **插件管理**:
   - GET /app-center/plugins/：获取插件列表
   - GET /app-center/plugins/{id}/：获取插件详情
   - POST /app-center/plugins/：创建插件
   - PUT /app-center/plugins/{id}/：更新插件
   - DELETE /app-center/plugins/{id}/：删除插件

3. **应用插件管理**:
   - POST /app-center/applications/{id}/add_plugin/：为应用添加插件
   - POST /app-center/applications/{id}/remove_plugin/：从应用移除插件

4. **应用监控与日志**:
   - GET /app-center/applications/{id}/monitoring/：获取应用监控数据
   - GET /app-center/applications/{id}/logs/：获取应用日志

### 前端架构

#### 组件结构

应用中心前端由以下核心组件构成：

1. **视图组件**:
   - `AppCenter.vue`: 应用中心主视图，管理应用和插件两个标签页
   
2. **应用管理组件**:
   - `ApplicationManagement.vue`: 应用管理容器组件，处理页面视图切换
   - `ApplicationList.vue`: 应用列表组件，展示所有应用并提供操作入口
   - `ApplicationDetail.vue`: 应用详情组件，展示应用详细信息和监控数据
   - `ApplicationForm.vue`: 应用表单组件，用于创建和编辑应用

3. **插件管理组件**:
   - `PluginManagement.vue`: 插件管理容器组件
   - `PluginList.vue`: 插件列表组件，展示所有插件并提供操作入口
   - `PluginDetail.vue`: 插件详情组件
   - `PluginForm.vue`: 插件表单组件，用于创建和编辑插件

#### 状态管理

应用中心使用Vuex进行状态管理:

1. **状态 (State)**:
   - `applications`: 应用列表
   - `currentApplication`: 当前应用
   - `plugins`: 插件列表
   - `loading`: 加载状态
   - `error`: 错误信息

2. **主要操作 (Actions)**:
   - 获取应用列表 `fetchApplications`
   - 获取应用详情 `fetchApplicationDetail`
   - 创建应用 `createApplication`
   - 更新应用 `updateApplication`
   - 删除应用 `deleteApplication`
   - 部署应用 `deployApplication`
   - 停止应用 `stopApplication`
   - 获取插件列表 `fetchPlugins`
   - 管理应用插件 `addPluginToApplication`, `removePluginFromApplication`

## 功能说明

### 应用管理

#### 应用创建流程

1. 用户点击应用列表中的"创建应用"按钮
2. 系统显示应用表单，用户填写以下信息：
   - 基本信息：应用名称、使用模型、描述
   - 配置参数：最大并发数、超时时间、日志级别
   - 高级配置：缓存大小、批处理大小、是否量化、环境变量
3. 用户提交表单，系统创建应用并返回应用列表

#### 应用部署流程

1. 用户在应用列表或应用详情中点击"部署"按钮
2. 系统弹出确认对话框
3. 用户确认后，系统开始部署应用
4. 部署成功后，应用状态更新为"运行中"，并生成API端点
5. 用户可通过API端点访问应用服务

#### 应用停止流程

1. 用户在应用列表或应用详情中点击"停止"按钮
2. 系统弹出确认对话框
3. 用户确认后，系统停止应用
4. 停止成功后，应用状态更新为"已停止"，API端点不再可用

#### 应用监控

应用监控功能展示以下指标：
- CPU使用率（%）
- 内存使用率（%）
- 总请求数
- 平均响应时间（ms）
- 错误率（%）

### 插件管理

#### 插件能力

插件系统允许用户扩展应用的基础能力，常见插件类型包括：
- 数据处理插件：用于预处理输入数据
- 回答优化插件：优化模型输出结果
- 安全过滤插件：过滤敏感信息
- 日志分析插件：分析应用日志
- 自定义功能插件：扩展特定业务功能

#### 插件管理流程

1. 用户在应用详情页查看已安装插件
2. 用户可通过"管理插件"功能添加或移除插件
3. 用户可启用或禁用已安装的插件
4. 插件配置反映在应用运行时行为中

## 使用指南

### 创建应用最佳实践

1. 选择合适的模型：根据业务需求选择适合的模型，考虑模型大小、精度和速度
2. 合理设置并发数：根据预期流量和硬件资源调整最大并发数
3. 优化内存使用：大模型应用注意内存使用，适当调整缓存大小
4. 测试与调优：创建应用后进行充分测试，调整参数以获得最佳性能

### 常见问题排查

1. 应用部署失败：
   - 检查模型是否存在并已完成训练
   - 检查系统资源是否充足
   - 查看日志了解详细错误原因

2. 应用性能问题：
   - 检查并发数是否设置合理
   - 考虑调整批处理大小
   - 是否可以启用量化减少内存占用
   - 监控系统资源使用情况

3. 插件相关问题：
   - 检查插件是否与当前应用兼容
   - 验证插件配置是否正确
   - 禁用部分插件测试是否为插件冲突

## 开发指南

### 添加新功能

如需向应用中心添加新功能，推荐以下步骤：

1. 后端开发：
   - 在`models.py`中添加新的数据模型
   - 创建相应的`serializers.py`序列化类
   - 在`views.py`中实现API视图
   - 更新`urls.py`添加新的API路由

2. 前端开发：
   - 在`api/appCenter.js`中添加新的API调用方法
   - 在`store/modules/appCenter.js`中添加新的状态管理
   - 创建新的Vue组件或更新现有组件
   
### 自定义插件开发

开发新的插件需要：

1. 实现插件接口：创建符合插件规范的类或模块
2. 注册插件：将插件注册到系统
3. 前端支持：添加插件配置界面
4. 测试集成：测试插件在应用中的表现

## 更新日志

### 当前版本

- 支持应用基本管理功能（创建、部署、停止、删除）
- 支持插件系统
- 提供应用监控和日志功能
- 支持应用配置管理

### 规划功能

- 应用版本管理
- 应用一键复制
- 应用性能测试
- 批量操作支持
- 更丰富的插件生态 