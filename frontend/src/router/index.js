import Vue from 'vue'
import VueRouter from 'vue-router'
import Cookies from 'js-cookie'
import Layout from '../views/Layout.vue'
import store from '../store'

Vue.use(VueRouter)

// 路由懒加载
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const NotFound = () => import('../views/NotFound.vue')
const ApiConnector = () => import('../views/ApiConnector.vue')

// 数据中心路由
const dataRoutes = {
  path: 'data-center',
  component: () => import('../views/DataCenter.vue'),
  meta: { title: '数据中心', requiresAuth: true },
  children: [
    {
      path: 'datasets',
      name: 'Datasets',
      component: () => import('../components/data/DatasetManagement.vue'),
      meta: { title: '数据集管理', requiresAuth: true }
    },
    {
      path: 'knowledge',
      name: 'Knowledge',
      component: () => import('../components/data/KnowledgeBaseManagement.vue'),
      meta: { title: '知识库管理', requiresAuth: true }
    }
  ]
}

// 训练中心路由
const trainingRoutes = {
  path: 'training-center',
  component: () => import('../views/TrainingCenter.vue'),
  meta: { title: '训练中心', requiresAuth: true },
  children: [
    {
      path: 'models',
      name: 'Models',
      component: () => import('../components/training/ModelManagement.vue'),
      meta: { title: '模型管理', requiresAuth: true }
    },
    {
      path: 'jobs',
      name: 'TrainingJobs',
      component: () => import('../components/training/TrainingJobs.vue'),
      meta: { title: '训练任务管理', requiresAuth: true }
    },
    {
      path: 'docker-images',
      name: 'DockerImages',
      component: () => import('../components/training/DockerImageManagement.vue'),
      meta: { title: '镜像管理', requiresAuth: true }
    }
  ]
}

// 应用中心路由
const appRoutes = {
  path: 'app-center',
  component: () => import('../views/AppCenter.vue'),
  meta: { title: '应用中心', requiresAuth: true },
  children: [
    {
      path: 'applications',
      name: 'Applications',
      component: () => import('../components/app/ApplicationManagement.vue'),
      meta: { title: '应用管理', requiresAuth: true }
    },
    {
      path: 'plugins',
      name: 'Plugins',
      component: () => import('../components/app/PluginManagement.vue'),
      meta: { title: '插件管理', requiresAuth: true }
    }
  ]
}

// 评测中心路由
const evaluationRoutes = {
  path: 'evaluation-center',
  component: () => import('../views/EvaluationCenter.vue'),
  meta: { title: '评测中心', requiresAuth: true },
  children: [
    {
      path: 'tasks',
      name: 'EvaluationTasks',
      component: () => import('../components/evaluation/EvaluationTaskList.vue'),
      meta: { title: '评测任务管理', requiresAuth: true }
    },
    {
      path: 'tasks/create',
      name: 'CreateEvaluationTask',
      component: () => import('../components/evaluation/EvaluationTaskCreate.vue'),
      meta: { title: '创建评测任务', requiresAuth: true }
    },
    {
      path: 'task/:id',
      name: 'EvaluationTaskDetail',
      component: () => import('../components/evaluation/EvaluationTaskDetail.vue'),
      props: true,
      meta: { title: '评测任务详情', requiresAuth: true }
    },
    {
      path: 'comparison',
      name: 'ModelComparison',
      component: () => import('../components/evaluation/ModelComparison.vue'),
      meta: { title: '模型对比', requiresAuth: true }
    },
    {
      path: 'comparison/create',
      name: 'CreateModelComparison',
      component: () => import('../components/evaluation/ModelComparisonCreate.vue'),
      meta: { title: '创建模型对比', requiresAuth: true }
    },
    {
      path: 'comparison/:id',
      name: 'ModelComparisonDetail',
      component: () => import('../components/evaluation/ModelComparison.vue'),
      props: true,
      meta: { title: '模型对比详情', requiresAuth: true }
    },
    {
      path: 'reports',
      name: 'EvaluationReports',
      component: () => import('../components/evaluation/EvaluationReportList.vue'),
      meta: { title: '评测报告', requiresAuth: true }
    },
    {
      path: 'reports/:id',
      name: 'EvaluationReportDetail',
      component: () => import('../components/evaluation/EvaluationReport.vue'),
      props: true,
      meta: { title: '评测报告详情', requiresAuth: true }
    }
  ]
}

// 添加API连接器路由
const apiConnectorRoutes = {
  path: 'api-connector',
  component: ApiConnector,
  meta: { title: 'API连接服务', requiresAuth: true }
}

const routes = [
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '仪表盘', requiresAuth: true }
      },
      dataRoutes,
      trainingRoutes,
      appRoutes,
      evaluationRoutes,
      apiConnectorRoutes
    ]
  },
  // 重定向路由
  {
    path: '/data-center',
    redirect: '/data-center/datasets'
  },
  {
    path: '/training-center',
    redirect: '/training-center/models'
  },
  {
    path: '/app-center',
    redirect: '/app-center/applications'
  },
  {
    path: '/evaluation-center',
    redirect: '/evaluation-center/tasks'
  },
  {
    path: '/api-connector',
    redirect: '/api-connector'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: '注册', requiresAuth: false }
  },
  {
    path: '*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: '页面不存在', requiresAuth: false }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: '/',
  routes
})

// 防止重复导航到同一路由引起的错误
const originalPush = VueRouter.prototype.push
const originalReplace = VueRouter.prototype.replace
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => {
    if (err.name !== 'NavigationDuplicated' && err.name !== 'NavigationCancelled') {
      console.warn('Navigation error:', err)
    }
  })
}
VueRouter.prototype.replace = function replace(location) {
  return originalReplace.call(this, location).catch(err => {
    if (err.name !== 'NavigationDuplicated' && err.name !== 'NavigationCancelled') {
      console.warn('Navigation error:', err)
    }
  })
}

// 上次认证检查时间
let lastAuthCheck = 0;
// 最小检查间隔（毫秒）
const AUTH_CHECK_INTERVAL = 2000;

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 大模型构建管理平台` : '大模型构建管理平台'
  
  // 如果是从登录页重定向过来的，直接通过
  if (from.path === '/login' && to.path === '/' && from.query && from.query.redirect) {
    next()
    return
  }
  
  // 检查是否需要登录
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const token = localStorage.getItem('token')
  
  // 防止频繁检查token导致的无限循环跳转
  const now = Date.now();
  if (now - lastAuthCheck < AUTH_CHECK_INTERVAL && to.path !== '/login' && from.path === '/login') {
    console.warn('认证检查过于频繁，延迟执行');
    setTimeout(() => {
      next()
    }, 200)
    return
  }
  
  lastAuthCheck = now;
  
  // 如果需要认证但没有token，则重定向到登录页
  if (requiresAuth && !token) {
    // 记录用户想要访问的页面，以便登录后重定向回去
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } 
  // 如果已登录且尝试访问登录或注册页面，则重定向到首页
  else if ((to.path === '/login' || to.path === '/register') && token) {
    // 如果登录页面有重定向查询参数，则重定向到该路径
    if (to.query && to.query.redirect) {
      next(to.query.redirect)
    } else {
      next('/')
    }
  } else {
    next()
  }
})

export default router 