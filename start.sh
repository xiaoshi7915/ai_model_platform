#!/bin/bash
# 启动脚本

# 设置环境变量
export PYTHONPATH=$PYTHONPATH:$(pwd)
export DJANGO_SETTINGS_MODULE=big_model_app.settings

# 安装依赖
echo "安装后端依赖..."
pip install -r backend/requirements.txt

# 初始化数据库
echo "初始化数据库..."
cd backend
python manage.py makemigrations
python manage.py migrate
python init_db.py

# 启动后端服务
echo "启动后端服务..."
python manage.py runserver 0.0.0.0:5688 &
BACKEND_PID=$!

# 启动Celery
echo "启动Celery..."
celery -A big_model_app worker --loglevel=info &
CELERY_PID=$!

# 安装前端依赖
echo "安装前端依赖..."
cd ../frontend
npm install

# 启动前端服务
echo "启动前端服务..."
npm run serve &
FRONTEND_PID=$!

# 注册退出处理函数
function cleanup {
    echo "停止服务..."
    kill $BACKEND_PID
    kill $CELERY_PID
    kill $FRONTEND_PID
    exit 0
}

# 捕获SIGINT和SIGTERM信号
trap cleanup SIGINT SIGTERM

# 等待用户按下Ctrl+C
echo "服务已启动，按Ctrl+C停止"
wait 