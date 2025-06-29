# 训练中心组件

训练中心组件是大型模型构建管理平台的核心功能之一，用于管理模型训练、模型管理和Docker镜像管理。

## 组件结构

训练中心组件包含以下主要组件：

### 视图组件

- `views/TrainingCenter.vue`: 训练中心主视图组件，作为路由入口点
- `views/training/TrainingCenter.vue`: 训练中心详细视图组件，负责管理所有子组件

### 模型管理

- `ModelManagement.vue`: 模型管理主组件，负责协调模型列表、详情和表单组件
- `ModelList.vue`: 模型列表组件，显示所有模型并提供搜索、过滤和分页功能
- `ModelDetail.vue`: 模型详情组件，显示模型的详细信息、训练参数和性能指标
- `ModelForm.vue`: 模型表单组件，用于创建和编辑模型

### 训练任务管理

- `TrainingJobs.vue`: 训练任务管理主组件
- `TrainingJobList.vue`: 训练任务列表组件，显示所有训练任务并提供状态过滤和模型过滤功能

### Docker镜像管理

- `DockerImageManagement.vue`: Docker镜像管理主组件
- `DockerImageList.vue`: Docker镜像列表组件，显示所有Docker镜像并提供搜索和分页功能
- `DockerImageDetail.vue`: Docker镜像详情组件，显示Docker镜像的详细信息
- `DockerImageForm.vue`: Docker镜像表单组件，用于创建和编辑Docker镜像

## 功能特点

### 模型管理

1. **模型列表**：
   - 搜索和过滤功能
   - 分页显示
   - 支持按模型状态过滤

2. **模型详情**：
   - 显示模型基本信息
   - 显示训练参数
   - 显示性能指标
   - 显示训练任务历史

3. **模型操作**：
   - 创建模型（设置名称、版本、描述和训练参数）
   - 编辑模型信息
   - 删除模型
   - 开始训练模型

### 训练任务管理

1. **训练任务列表**：
   - 状态过滤功能（等待中、运行中、已完成、失败、已取消）
   - 模型过滤功能
   - 分页显示

2. **训练任务详情**：
   - 显示训练任务基本信息
   - 显示训练日志
   - 显示训练进度

3. **训练任务操作**：
   - 查看训练日志
   - 取消训练任务

### Docker镜像管理

1. **Docker镜像列表**：
   - 搜索功能
   - 分页显示

2. **Docker镜像详情**：
   - 显示Docker镜像基本信息
   - 显示使用该镜像的训练任务

3. **Docker镜像操作**：
   - 添加Docker镜像（设置名称、标签、仓库和描述）
   - 编辑Docker镜像信息
   - 删除Docker镜像

## 路由结构

训练中心的路由结构如下：

- `/training`: 训练中心主页，默认重定向到模型管理页面
  - `/training/models`: 模型管理页面
  - `/training/jobs`: 训练任务页面
  - `/training/docker-images`: Docker镜像管理页面

## 使用方法

### 模型管理

1. **创建模型**：
   - 点击"创建模型"按钮
   - 填写模型名称、版本和描述
   - 选择训练数据集
   - 设置训练参数
   - 点击"保存"按钮完成创建

2. **查看模型**：
   - 在模型列表中点击模型名称或"查看"按钮
   - 查看模型详情、训练参数和性能指标

3. **编辑模型**：
   - 在模型列表或详情页点击"编辑"按钮
   - 修改模型名称、版本、描述和训练参数
   - 点击"保存"按钮完成编辑

4. **训练模型**：
   - 在模型详情页点击"训练"按钮
   - 选择Docker镜像
   - 确认训练参数
   - 点击"开始训练"按钮开始训练

5. **删除模型**：
   - 在模型列表或详情页点击"删除"按钮
   - 确认删除操作

### 训练任务管理

1. **查看训练任务**：
   - 在训练任务列表中查看所有训练任务
   - 使用状态过滤器和模型过滤器筛选任务

2. **查看训练日志**：
   - 在训练任务列表中点击"查看日志"按钮
   - 查看训练日志详情

3. **取消训练任务**：
   - 在训练任务列表中点击"取消"按钮
   - 确认取消操作

### Docker镜像管理

1. **添加Docker镜像**：
   - 点击"添加镜像"按钮
   - 填写镜像名称、标签、仓库和描述
   - 点击"确定"按钮完成添加

2. **编辑Docker镜像**：
   - 在Docker镜像列表中点击"编辑"按钮
   - 修改镜像信息
   - 点击"确定"按钮完成编辑

3. **删除Docker镜像**：
   - 在Docker镜像列表中点击"删除"按钮
   - 确认删除操作

## 数据流

训练中心组件使用Vuex进行状态管理，主要数据流如下：

1. 组件通过dispatch action从API获取数据
2. API返回数据后，通过mutation更新state
3. 组件通过computed属性或mapState获取state中的数据
4. 用户操作触发action，更新后端数据并同步更新state

## API接口

训练中心组件使用以下API接口：

### 模型管理API

- `GET /api/v1/training-center/models/`: 获取模型列表
- `GET /api/v1/training-center/models/{id}/`: 获取模型详情
- `POST /api/v1/training-center/models/`: 创建模型
- `PUT /api/v1/training-center/models/{id}/`: 更新模型
- `DELETE /api/v1/training-center/models/{id}/`: 删除模型
- `POST /api/v1/training-center/models/{id}/train/`: 开始训练模型
- `POST /api/v1/training-center/models/{id}/cancel/`: 取消训练模型

### 训练任务API

- `GET /api/v1/training-center/jobs/`: 获取训练任务列表
- `GET /api/v1/training-center/jobs/{id}/`: 获取训练任务详情
- `POST /api/v1/training-center/jobs/`: 创建训练任务
- `POST /api/v1/training-center/jobs/{id}/cancel/`: 取消训练任务
- `GET /api/v1/training-center/jobs/{id}/log/`: 获取训练任务日志
- `GET /api/v1/training-center/jobs/{id}/progress/`: 获取训练任务进度

### Docker镜像API

- `GET /api/v1/training-center/docker-images/`: 获取Docker镜像列表
- `GET /api/v1/training-center/docker-images/{id}/`: 获取Docker镜像详情
- `POST /api/v1/training-center/docker-images/`: 创建Docker镜像
- `PUT /api/v1/training-center/docker-images/{id}/`: 更新Docker镜像
- `DELETE /api/v1/training-center/docker-images/{id}/`: 删除Docker镜像
- `POST /api/v1/training-center/docker-images/pull/`: 从远程仓库拉取Docker镜像

## 注意事项

1. 只有处于"草稿"或"失败"状态的模型才能进行编辑
2. 处于"训练中"状态的模型不能被删除
3. 只有处于"等待中"或"运行中"状态的训练任务才能被取消
4. 被训练任务使用的Docker镜像不能被删除 