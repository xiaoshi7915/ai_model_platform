# 大型模型构建管理平台 - 用户指南与部署手册

## 项目概述与价值

### 项目简介
本平台是一个专为AI模型开发者和使用者设计的综合性管理系统，实现了大型模型从数据准备、训练到评估和部署的全生命周期管理。无论您是人工智能专家还是业务人员，本平台都能帮助您轻松构建、管理和应用AI模型。

### 核心价值
- **简化模型管理**：通过直观的界面管理数据集、模型训练和应用部署
- **提高开发效率**：自动化工作流程，减少重复工作，加速模型迭代
- **降低技术门槛**：友好的用户界面，使非技术人员也能参与AI模型开发
- **全面的评测分析**：专业的模型评测工具，帮助您做出更明智的决策

## 系统架构与功能模块

### 系统架构
本项目采用前后端分离的现代化架构：

- **前端技术**：
  - Vue.js 2.x 框架：构建用户界面
  - Element UI 组件库：提供美观的UI界面
  - ECharts 图表库：数据可视化展示
  - Axios：处理HTTP请求

- **后端技术**：
  - Django / Django REST Framework：提供API服务
  - PostgreSQL / pgvector：存储结构化数据和向量数据
  - Redis：缓存和消息队列
  - Celery：处理异步任务

### 核心功能模块

#### 1. 数据中心
数据中心是模型训练的基础，提供数据管理和知识库功能：

- **数据集管理**：
  - 上传和导入各类数据集（表格、文本、图像等）
  - 数据集预览和统计分析
  - 数据集版本控制和共享

- **知识库管理**：
  - 创建和维护专业领域知识库
  - 支持多种格式文档导入
  - 知识检索和内容更新

#### 2. 训练中心
训练中心负责模型的训练和管理：

- **模型管理**：
  - 创建和配置模型
  - 模型版本控制
  - 模型参数管理

- **训练任务**：
  - 创建和配置训练任务
  - 实时监控训练进程
  - 训练结果可视化展示

- **Docker镜像管理**：
  - 上传和管理训练环境
  - 镜像版本控制
  - 镜像兼容性检查

#### 3. 应用中心
应用中心负责模型的部署和应用：

- **应用管理**：
  - 创建和部署模型应用
  - 应用状态监控
  - 应用配置管理

- **资源监控**：
  - CPU和内存使用率监控
  - 请求量和响应时间统计
  - 系统健康状态检查

- **插件管理**：
  - 上传和管理应用插件
  - 插件兼容性检查
  - 插件版本控制

#### 4. 评测中心
评测中心负责模型的性能评估：

- **评测任务**：
  - 创建和配置评测任务
  - 选择评测指标和数据集
  - 评测结果可视化展示

- **模型对比**：
  - 多模型性能对比
  - 指标差异分析
  - 对比结果可视化展示

- **评测报告**：
  - 生成专业评测报告
  - 报告导出和分享
  - 模型优化建议

## 前后端路由配置

### 后端路由配置

后端API路由配置采用了以下结构:

- `/api/data-center/` - 数据中心API
- `/api/training-center/` - 训练中心API
- `/api/app-center/` - 应用中心API
- `/api/evaluation-center/` - 评测中心API
- `/api/api-connector/` - API连接服务

同时，为了向后兼容，保留了带版本号的API路由:

- `/api/v1/data-center/`
- `/api/v1/training-center/`
- `/api/v1/app-center/`
- `/api/v1/evaluation-center/`
- `/api/v1/api-connector/`

### 前端路由配置

前端路由配置采用了以下结构:

- `/data-center` - 数据中心
  - `/data-center/datasets` - 数据集管理
  - `/data-center/knowledge` - 知识库管理
- `/training-center` - 训练中心
  - `/training-center/models` - 模型管理
  - `/training-center/jobs` - 训练任务管理
  - `/training-center/docker-images` - 镜像管理
- `/app-center` - 应用中心
  - `/app-center/applications` - 应用管理
  - `/app-center/plugins` - 插件管理
- `/evaluation-center` - 评测中心
  - `/evaluation-center/tasks` - 评测任务管理
  - `/evaluation-center/task/:id` - 评测任务详情
  - `/evaluation-center/comparison` - 模型对比
  - `/evaluation-center/reports` - 评测报告列表
  - `/evaluation-center/reports/:id` - 评测报告详情
- `/api-connector` - API连接服务

### API调用说明

前端通过axios库调用后端API，统一使用`/api/`前缀。各模块API调用示例:

```javascript
// 数据中心API
axios.get('/api/data-center/datasets/');

// 训练中心API
axios.get('/api/training-center/models/');

// 应用中心API
axios.get('/api/app-center/applications/');

// 评测中心API
axios.get('/api/evaluation-center/tasks/');

// API连接服务
axios.get('/api/api-connector/providers/');
```

注意: 通过更新前后端路由配置，确保了前端页面能够正确访问后端API，解决了路径不匹配的问题。

## 新用户快速入门指南

### 第一步：登录系统
1. 打开浏览器，访问系统地址：http://localhost:5588/（本地部署）或服务器地址
2. 输入默认账号：admin
3. 输入默认密码：admin123456@
4. 点击"登录"按钮

### 第二步：创建您的第一个数据集
1. 在左侧导航栏中点击"数据中心"
2. 在数据集管理页面点击"上传数据集"按钮
3. 填写数据集名称（如"客户反馈数据"）
4. 选择数据集类型（文本、图像、表格等）
5. 上传数据文件（支持CSV、Excel、ZIP等格式）
6. 添加数据集描述和标签
7. 点击"提交"完成创建

### 第三步：训练您的第一个模型
1. 在左侧导航栏中点击"训练中心"
2. 在模型管理页面点击"创建模型"按钮
3. 选择模型类型（文本分类、图像识别等）
4. 选择基础模型（如BERT、ResNet等）
5. 配置训练参数（学习率、批次大小等）
6. 选择您刚才创建的数据集
7. 点击"开始训练"按钮开始训练
8. 在训练任务页面实时查看训练进度和指标

### 第四步：部署您的第一个应用
1. 在左侧导航栏中点击"应用中心"
2. 在应用管理页面点击"创建应用"按钮
3. 选择您训练好的模型
4. 配置应用参数（名称、描述、资源限制等）
5. 选择部署模式（开发环境、生产环境）
6. 点击"部署"按钮开始部署
7. 等待应用状态变为"运行中"
8. 点击"访问"按钮测试您的应用

### 第五步：评测您的模型性能
1. 在左侧导航栏中点击"评测中心"
2. 在评测任务页面点击"创建评测任务"按钮
3. 选择您的模型和评测数据集
4. 选择评测指标（准确率、F1值等）
5. 点击"开始评测"按钮
6. 查看评测结果和可视化图表
7. 导出评测报告或与其他模型进行对比

## 深入使用指南

### 数据管理最佳实践
- **数据准备技巧**：
  - 确保数据格式统一，避免特殊字符和编码问题
  - 对于文本数据，建议进行预处理（去除停用词、标点等）
  - 对于图像数据，建议统一分辨率和格式
  - 合理划分训练集、验证集和测试集

- **知识库构建方法**：
  - 按主题或领域组织知识结构
  - 定期更新和维护知识内容
  - 添加关键词和标签，提高检索效率

### 模型训练技巧
- **参数选择建议**：
  - 学习率：通常从小值开始（如0.001），根据训练情况调整
  - 批次大小：根据GPU内存和数据特点选择，常见值为16、32、64
  - 训练轮次：避免过拟合，使用早停策略

- **训练监控要点**：
  - 关注损失函数曲线，确保其持续下降
  - 监控验证集性能，避免过拟合
  - 检查资源利用率，优化训练效率

### 应用部署策略
- **资源配置建议**：
  - CPU：根据模型复杂度和并发请求量决定
  - 内存：通常为模型大小的2-3倍
  - GPU：对于大型模型或高并发场景建议使用

- **应用监控要点**：
  - 定期检查资源利用率
  - 关注异常请求和错误日志
  - 监控平均响应时间

### 模型评测深入解析
- **常用评测指标说明**：
  - 分类任务：准确率、精确率、召回率、F1值
  - 回归任务：MSE、MAE、R²
  - 生成任务：BLEU、ROUGE、困惑度

- **评测结果分析方法**：
  - 分析错误样本，找出模型弱点
  - 比较不同参数设置下的性能差异
  - 结合业务目标评估模型实用性

## 部署指南

### 方式一：源码部署（推荐开发者使用）

1. **环境准备**：
   ```bash
   # 安装必要的系统依赖
   sudo apt update
   sudo apt install python3.9 python3.9-venv python3-pip nodejs npm redis-server nginx postgresql -y
   
   # 创建和配置PostgreSQL数据库
   sudo -u postgres psql -c "CREATE USER pgvector WITH PASSWORD 'pgvector';"
   sudo -u postgres psql -c "CREATE DATABASE ai_model_app OWNER pgvector;"
   sudo -u postgres psql -c "ALTER USER pgvector WITH SUPERUSER;"
   ```

2. **获取代码**：
   ```bash
   # 克隆代码仓库（如果适用）
   git clone https://your-repository-url.git
   cd big_model_app
   ```

3. **配置环境变量**：
   - 编辑 `backend/.env` 文件，确保数据库和Redis配置正确
   ```
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=ai_model_app
   DB_USER=pgvector
   DB_PASSWORD=pgvector
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. **执行部署脚本**：
   ```bash
   # 赋予脚本执行权限
   chmod +x production_deploy.sh
   
   # 执行部署脚本
   ./production_deploy.sh
   ```

5. **访问系统**：
   - 前端地址：http://your_server_ip:5588/
   - 后端API地址：http://your_server_ip:5688/api/v1/
   - 默认账号：admin
   - 默认密码：admin123456@

### 方式二：Docker部署（推荐生产环境使用）

1. **安装Docker环境**：
   ```bash
   # 安装Docker和Docker Compose
   sudo apt update
   sudo apt install docker.io docker-compose -y
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

2. **准备配置文件**：
   - 确保 `docker-compose.yml` 文件中的配置正确
   - 修改 `backend/.env` 文件中的数据库和Redis配置

3. **启动容器**：
   ```bash
   # 构建和启动所有服务
   docker-compose up -d
   ```

4. **访问系统**：
   - 前端地址：http://your_server_ip:5588/
   - 默认账号：admin
   - 默认密码：admin123456@

### 方式三：快速开发环境（本地测试）

1. **执行快速启动脚本**：
   ```bash
   # 赋予脚本执行权限
   chmod +x quick_start.sh
   
   # 执行快速启动脚本
   ./quick_start.sh
   ```

2. **访问系统**：
   - 前端地址：http://localhost:5588/
   - 后端API地址：http://localhost:5688/api/v1/
   - 默认账号：admin
   - 默认密码：admin123456@

## 常见问题与解决方案

### 1. 系统无法启动
- **症状**：访问系统地址时显示连接错误
- **可能原因**：
  - 服务未正常启动
  - 端口被占用
  - 网络设置问题
- **解决方法**：
  - 检查服务状态：`docker-compose ps` 或 `systemctl status nginx`
  - 检查端口占用：`netstat -tulpn | grep 5588`
  - 查看错误日志：`logs/backend.log` 和 `logs/frontend.log`

### 2. 无法登录系统
- **症状**：输入账号密码后无法登录
- **可能原因**：
  - 账号密码错误
  - 数据库连接问题
  - 会话问题
- **解决方法**：
  - 确认使用默认账号：admin/admin123456@
  - 检查数据库连接：`python backend/check_db.py`
  - 清除浏览器缓存和Cookie

### 3. 上传数据失败
- **症状**：上传数据时出现错误
- **可能原因**：
  - 文件格式不支持
  - 文件太大
  - 存储权限问题
- **解决方法**：
  - 检查支持的文件格式
  - 检查文件大小限制（默认50MB）
  - 检查目录权限：`chmod -R 755 media/`

### 4. 训练任务失败
- **症状**：训练任务状态显示"失败"
- **可能原因**：
  - 数据集有问题
  - 训练参数不合适
  - 资源不足
- **解决方法**：
  - 检查数据集格式和内容
  - 调整训练参数（减小批次大小等）
  - 查看训练日志：`logs/celery_worker.log`

### 5. 应用无法访问
- **症状**：应用部署成功但无法访问
- **可能原因**：
  - 应用未正常启动
  - 端口映射问题
  - 网络配置问题
- **解决方法**：
  - 检查应用状态
  - 检查网络配置
  - 查看应用日志：`logs/app_center.log`

## 维护与优化建议

### 定期维护
- **数据库备份**：每周备份数据库，防止数据丢失
- **日志清理**：每月清理过期日志，避免磁盘空间不足
- **系统更新**：定期更新系统和依赖包，修复安全漏洞

### 性能优化
- **数据库优化**：定期分析和优化数据库查询
- **资源分配**：根据使用情况调整资源分配
- **缓存策略**：优化缓存配置，提高响应速度

### 扩展建议
- **模型库扩展**：添加更多预训练模型，支持更多应用场景
- **数据处理增强**：增加更多数据处理和增强功能
- **集成第三方服务**：集成外部AI服务，扩展系统能力

## 联系与支持

如果您在使用过程中遇到任何问题，或有任何建议和反馈，请通过以下方式联系我们：

- **技术支持邮箱**：support@example.com
- **问题反馈**：在系统中点击"帮助"→"提交反馈"
- **文档中心**：访问 docs/ 目录查看详细文档

感谢您使用大型模型构建管理平台！我们将不断完善系统功能，为您提供更好的AI模型开发体验。 