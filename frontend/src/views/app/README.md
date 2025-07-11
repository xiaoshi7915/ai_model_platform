# 应用中心 (Application Center)

## 功能概述

应用中心是一个用于管理大模型应用的模块，提供了应用的全生命周期管理功能，包括创建、部署、监控和管理大模型应用。用户可以通过应用中心将训练好的模型快速部署为可用的API服务，并通过插件扩展功能。

主要功能包括：

1. **应用管理**：创建、编辑、部署、停止和删除应用
2. **应用监控**：查看应用的运行状态、资源使用情况和请求统计
3. **日志查看**：查看应用运行日志，支持按日志级别筛选
4. **插件管理**：为应用添加和管理功能插件，扩展应用能力
5. **向导式创建**：通过向导引导用户完成应用创建流程，适合新手用户

## 模块架构

应用中心模块由以下主要组件构成：

1. **应用管理（ApplicationManagement.vue）**：
   - 应用中心的主视图，负责应用的整体操作流程管理
   - 管理应用的不同视图状态（列表、详情、表单、向导）
   - 处理应用的创建、编辑、部署等操作

2. **应用列表（ApplicationList.vue）**：
   - 显示应用列表，支持分页和搜索
   - 提供快速操作按钮（查看详情、编辑、部署、停止、删除）
   - 显示应用的核心信息（名称、状态、API地址等）

3. **应用详情（ApplicationDetail.vue）**：
   - 展示应用的详细信息
   - 包含基本信息、配置信息、监控信息、日志和插件信息
   - 提供应用操作按钮

4. **应用表单（ApplicationForm.vue）**：
   - 用于创建和编辑应用的表单
   - 包含基本信息、配置参数和环境变量设置

5. **应用向导（ApplicationWizard.vue）**：
   - 提供分步骤的应用创建体验
   - 更加用户友好，适合首次使用的用户
   - 根据模型大小自动推荐配置参数

6. **插件管理（PluginManagement.vue）**：
   - 管理系统中可用的插件
   - 提供插件的安装、启用、禁用和删除功能

## 数据流向

应用中心的数据流向如下：

1. **获取数据**：
   - 从后端API获取应用列表和详情
   - 从后端API获取可用模型和插件列表

2. **状态管理**：
   - 使用Vuex管理应用状态
   - 主要状态包括应用列表、当前应用、模型列表和插件列表

3. **操作流程**：
   - 用户操作（如创建、部署）通过组件事件传递
   - 组件调用Vuex actions执行API请求
   - 请求结果更新Vuex状态，UI自动响应变化

## 使用指南

### 创建应用

创建应用有两种方式：

1. **标准创建**：
   - 点击应用列表页的"创建应用"按钮
   - 填写应用名称、选择模型
   - 配置运行参数（并发数、超时时间等）
   - 设置环境变量（可选）
   - 提交表单创建应用

2. **向导创建**：
   - 点击应用列表页的"向导创建"按钮
   - 按照向导步骤填写信息
   - 系统会根据选择的模型自动推荐配置参数
   - 可视化选择插件
   - 确认信息后提交创建

### 管理应用

1. **查看详情**：
   - 点击应用名称或"详情"按钮
   - 查看应用的详细信息、配置和监控数据

2. **部署应用**：
   - 在应用列表或详情页点击"部署"按钮
   - 系统将启动应用部署流程
   - 部署成功后状态变为"运行中"，API地址可用

3. **停止应用**：
   - 对于运行中的应用，点击"停止"按钮
   - 系统将停止应用实例

4. **删除应用**：
   - 点击"删除"按钮
   - 确认删除操作

### 管理插件

1. **系统插件管理**：
   - 切换到"插件管理"标签
   - 查看所有可用插件
   - 安装、启用或禁用插件

2. **应用插件管理**：
   - 在应用详情页的"插件信息"区域
   - 查看应用已启用的插件
   - 管理应用的插件启用状态

## 开发指南

### 添加新功能

1. **扩展应用配置**：
   - 在ApplicationForm.vue和ApplicationWizard.vue中添加新的配置字段
   - 在相应的数据模型和表单验证中添加字段

2. **添加新的插件类型**：
   - 在插件管理组件中添加新的插件类型
   - 更新插件兼容性检查逻辑

### 调试提示

1. **应用状态**：
   - 应用状态变化是异步的，部署和停止操作需要轮询服务器状态
   - 使用Vue Devtools查看Vuex状态变化

2. **API交互**：
   - 应用API交互在store/modules/application.js中定义
   - 查看浏览器网络面板调试API请求

## 最佳实践

1. **配置推荐**：
   - 根据模型大小选择合适的配置参数
   - 小型模型（<3B参数）：并发数10，批处理大小8
   - 中型模型（3-13B参数）：并发数5，批处理大小4
   - 大型模型（>13B参数）：并发数2，批处理大小1

2. **应用命名**：
   - 使用有意义的应用名称，便于识别
   - 仅使用字母、数字、下划线和连字符

3. **插件选择**：
   - 仅选择必要的插件，过多插件可能影响性能
   - 确保插件之间相互兼容

# 评测中心 (Evaluation Center) 重构和修复报告

## 问题描述

评测中心存在多个路由跳转问题，导致以下功能无法正常使用：

1. 点击任务名称跳转到404页面
2. 点击操作按钮（如查看详情）跳转到404页面
3. 点击模型比对跳转到404页面

这些问题主要是由于路由配置不完整和组件中的路由路径不一致导致的。

## 修复方案

### 1. 路由配置修复

在`router/index.js`中：

1. 添加了任务详情路由 `/evaluation-center/task/:id`
2. 添加了模型比对详情路由 `/evaluation-center/comparison/:id`
3. 添加了评测报告详情路由 `/evaluation-center/report/:id`

### 2. 组件修复

1. 评测中心组件(`EvaluationCenter.vue`)
   - 修复了跳转路径，从`/evaluation/task/{id}`改为`/evaluation-center/task/{id}`

2. 评测任务详情组件(`EvaluationTaskDetail.vue`)
   - 添加了对路由参数的支持，通过prop接收任务ID
   - 修复了返回和报告查看的路由路径

3. 评测报告组件(`EvaluationReport.vue`)
   - 添加了对路由参数的支持
   - 实现了自动加载报告的功能
   - 修复了返回按钮的跳转路径

4. 模型比对组件(`ModelComparison.vue`)
   - 添加了对路由参数的支持
   - 实现了自动加载比对详情的功能
   - 修复了比对详情的查看路径

5. 评测中心视图组件(`views/evaluation/EvaluationCenter.vue`)
   - 修复了标签页和路由的联动逻辑
   - 确保路径中包含`evaluation-center`而非`evaluation`

### 3. 路由跳转统一

确保所有相关组件使用一致的路由路径：

- 任务列表：`/evaluation-center/tasks`
- 任务详情：`/evaluation-center/task/:id`
- 模型比对：`/evaluation-center/comparison`
- 模型比对详情：`/evaluation-center/comparison/:id`
- 评测报告：`/evaluation-center/reports`
- 评测报告详情：`/evaluation-center/report/:id`

## 优化建议

1. **路由命名规范化**：所有路由采用了统一的命名规范，单数表示单个资源（如task/:id），复数表示列表（如tasks）

2. **组件解耦**：将路由处理和数据处理分离，提高组件的复用性

3. **路由参数响应**：使用计算属性和watch监听路由参数变化，确保组件能够正确响应路由变化

4. **错误处理**：在加载详情数据失败时，提供友好的错误提示

## 测试验证

修复后，以下功能已恢复正常：

- 从任务列表点击任务名称可正确跳转到任务详情页
- 点击"查看"按钮可正确跳转到任务详情页
- 在模型比对列表页点击"查看"按钮可正确跳转到比对详情
- 在任务详情页点击"查看完整报告"可正确跳转到评测报告页

所有页面之间的导航链接现在都可以正常工作，用户可以在评测中心的各个功能之间无缝切换。 