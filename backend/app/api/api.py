from fastapi import APIRouter

from app.api.endpoints import (
    auth,
    users,
    datasets,
    models,
    training_jobs,
    applications,
    evaluation_tasks,
    docker_images
)

api_router = APIRouter()

# 认证相关路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])

# 用户相关路由
api_router.include_router(users.router, prefix="/users", tags=["用户"])

# 数据中心相关路由
api_router.include_router(datasets.router, prefix="/datasets", tags=["数据集"])

# 训练中心相关路由
api_router.include_router(models.router, prefix="/models", tags=["模型"])
api_router.include_router(training_jobs.router, prefix="/training-jobs", tags=["训练任务"])
api_router.include_router(docker_images.router, prefix="/docker-images", tags=["Docker镜像"])

# 应用中心相关路由
api_router.include_router(applications.router, prefix="/applications", tags=["应用"])

# 评估中心相关路由
api_router.include_router(evaluation_tasks.router, prefix="/evaluation-tasks", tags=["评估任务"]) 