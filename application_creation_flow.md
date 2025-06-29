# 应用创建流程图

以下流程图展示了应用创建的完整流程：

```mermaid
graph TD
    A[用户点击"创建应用"按钮] --> B[切换到表单视图]
    B --> C[填写应用表单]
    C --> D[验证表单数据]
    D -->|不通过| C
    D -->|通过| E[提交表单]
    E --> F[调用Vuex createApplication action]
    F --> G[发送API请求到后端]
    G --> H[后端验证数据]
    H -->|不通过| I[返回错误信息]
    I --> C
    H -->|通过| J[创建应用实例]
    J --> K[返回应用数据]
    K --> L[更新前端状态]
    L --> M[显示成功消息]
    M --> N[切换回列表视图]
```

## 组件交互图

以下图表展示了不同组件之间的交互关系：

```mermaid
sequenceDiagram
    participant User
    participant AppList as ApplicationList.vue
    participant AppManagement as ApplicationManagement.vue
    participant AppForm as ApplicationForm.vue
    participant Vuex as Vuex Store
    participant API as API Service
    participant Backend as Backend Server
    
    User->>AppList: 点击"创建应用"
    AppList->>AppManagement: 触发create事件
    AppManagement->>AppForm: 切换到表单视图
    User->>AppForm: 填写表单
    User->>AppForm: 点击提交
    AppForm->>AppForm: 验证表单
    AppForm->>AppManagement: 触发submit事件(formData)
    AppManagement->>Vuex: 调用createApplication(formData)
    Vuex->>API: 调用api.appCenter.createApplication(formData)
    API->>Backend: 发送POST请求
    Backend->>Backend: 验证数据
    Backend->>Backend: 创建应用
    Backend->>API: 返回应用数据
    API->>Vuex: 返回应用数据
    Vuex->>Vuex: 添加应用到状态
    Vuex->>AppManagement: 返回成功
    AppManagement->>User: 显示成功消息
    AppManagement->>AppList: 切换回列表视图
```

## 应用状态转换图

以下状态转换图展示了应用在不同状态之间的转换：

```mermaid
stateDiagram-v2
    [*] --> stopped: 创建应用
    stopped --> running: 部署
    running --> stopped: 停止
    stopped --> [*]: 删除
    running --> error: 发生错误
    error --> stopped: 停止
```

## 数据流图

以下数据流图展示了应用创建过程中的数据流向：

```mermaid
flowchart LR
    User[用户输入] --> |表单数据| Form[ApplicationForm]
    Form --> |formData| Management[ApplicationManagement]
    Management --> |formData| Vuex[Vuex Store]
    Vuex --> |HTTP请求| Backend[后端API]
    Backend --> |验证| DB[(数据库)]
    DB --> |应用实例| Backend
    Backend --> |应用数据| Vuex
    Vuex --> |状态更新| Management
    Management --> |视图切换| List[ApplicationList]
``` 