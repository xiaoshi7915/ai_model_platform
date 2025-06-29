# 大模型构建管理平台 - 项目结构概览

## 系统架构

### 前端架构 (Vue.js)
- 使用Vue.js框架构建
- 使用Vuex进行状态管理
- 使用Vue Router进行路由管理
- 使用Axios进行HTTP请求

### 后端架构 (Django)
- 使用Django框架构建
- 使用Django REST Framework提供API
- 使用Celery进行异步任务处理
- 使用Redis作为消息队列

### 数据库
- 支持SQLite（默认）和PostgreSQL
- PostgreSQL支持向量搜索功能

### 部署方式
- 提供Docker Compose配置，支持容器化部署
- 提供简单的启动脚本，用于开发环境

## 项目目录结构

### 根目录
- `backend/` - 后端Django项目
- `frontend/` - 前端Vue.js项目
- `media/` - 媒体文件存储
- `static/` - 静态文件存储
- `logs/` - 日志文件存储
- 各种启动脚本和配置文件

### 后端目录 (`backend/`)
- `big_model_app/` - 主Django项目配置
- `api/` - 用户认证和通用API
- `data_center/` - 数据中心模块
- `training_center/` - 训练中心模块
- `app_center/` - 应用中心模块
- `evaluation_center/` - 评测中心模块
- `utils/` - 工具函数

### 前端目录 (`frontend/`)
- `src/` - 源代码
  - `api/` - API请求配置
  - `assets/` - 静态资源
  - `components/` - Vue组件
  - `router/` - 路由配置
  - `store/` - Vuex状态管理
  - `views/` - 页面视图

## 主要功能模块

### 数据中心
- 数据集管理
- 知识库管理

### 训练中心
- 模型管理
- 训练任务管理
- 镜像管理

### 应用中心
- 应用管理
- 插件管理

### 评测中心
- 评测任务管理
- 模型对比
- 评测报告

## API结构

### 认证API
- 用户登录/注册
- 用户资料管理

### 功能模块API
- 各模块均有自己的API端点，用于数据交互

## 部署与运行

### 开发环境
1. 运行`start.sh`脚本，自动安装依赖并启动服务
2. 后端服务默认运行在端口5688
3. 前端服务使用Vue CLI默认端口(8080)

### 生产环境
1. 使用Docker Compose构建和运行服务
2. 前端服务通过Nginx提供，端口5588
3. 后端服务与Celery通过内部网络通信 