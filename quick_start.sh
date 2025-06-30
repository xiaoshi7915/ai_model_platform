#!/bin/bash

# 快速启动脚本 - 处理所有初始化步骤

# 设置颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 打印带颜色的信息
info() {
    echo -e "${GREEN}[INFO] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARN] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# 创建必要的目录
create_directories() {
    info "创建必要的目录..."
    mkdir -p backend/logs
    mkdir -p backend/media
    mkdir -p backend/static
    info "目录创建完成"
}

# 检查Redis是否运行
check_redis() {
    info "检查Redis服务..."
    if command -v redis-cli >/dev/null 2>&1; then
        if redis-cli ping >/dev/null 2>&1; then
            info "Redis服务运行正常"
            return 0
        else
            warn "Redis服务未运行，尝试启动..."
            if command -v systemctl >/dev/null 2>&1; then
                sudo systemctl start redis
            elif command -v service >/dev/null 2>&1; then
                sudo service redis-server start
            else
                error "无法自动启动Redis，请手动启动Redis服务"
                return 1
            fi
        fi
    else
        error "未检测到redis-cli，请确保Redis已安装"
        return 1
    fi
}

# 安装后端依赖
install_backend_deps() {
    info "安装后端依赖..."
    cd backend || { error "无法进入backend目录"; exit 1; }
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        error "安装后端依赖失败"
        exit 1
    fi
    info "后端依赖安装完成"
    cd ..
}

# 安装前端依赖
install_frontend_deps() {
    info "安装前端依赖..."
    cd frontend || { error "无法进入frontend目录"; exit 1; }
    npm install
    if [ $? -ne 0 ]; then
        error "安装前端依赖失败，尝试使用cnpm..."
        if command -v cnpm >/dev/null 2>&1; then
            cnpm install
            if [ $? -ne 0 ]; then
                error "使用cnpm安装前端依赖失败"
                exit 1
            fi
        else
            error "无法安装前端依赖，请检查Node.js环境"
            exit 1
        fi
    fi
    info "前端依赖安装完成"
    cd ..
}

# 初始化数据库
init_db() {
    info "初始化数据库..."
    cd backend || { error "无法进入backend目录"; exit 1; }
    python manage.py makemigrations
    python manage.py migrate
    python init_db.py
    if [ $? -ne 0 ]; then
        error "数据库初始化失败"
        exit 1
    fi
    info "数据库初始化完成"
    cd ..
}

# 收集静态文件
collect_static() {
    info "收集静态文件..."
    cd backend || { error "无法进入backend目录"; exit 1; }
    python manage.py collectstatic --noinput
    if [ $? -ne 0 ]; then
        error "静态文件收集失败"
        exit 1
    fi
    info "静态文件收集完成"
    cd ..
}

# 检查环境
check_environment() {
    info "检查环境..."
    cd backend || { error "无法进入backend目录"; exit 1; }
    python check_env.py
    cd ..
}

# 启动后端
start_backend() {
    info "启动后端服务..."
    cd backend || { error "无法进入backend目录"; exit 1; }
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    export DJANGO_SETTINGS_MODULE=big_model_app.settings
    python manage.py runserver 0.0.0.0:5688 &
    BACKEND_PID=$!
    info "后端服务启动成功 (PID: $BACKEND_PID)"
    
    # 启动Celery Worker（如果Redis可用）
    if redis-cli ping >/dev/null 2>&1; then
        info "启动Celery Worker..."
        celery -A big_model_app worker --loglevel=info &
        CELERY_PID=$!
        info "Celery Worker启动成功 (PID: $CELERY_PID)"
    else
        warn "Redis未运行，跳过启动Celery"
    fi
    
    cd ..
}

# 启动前端
start_frontend() {
    info "启动前端服务..."
    cd frontend || { error "无法进入frontend目录"; exit 1; }
    npm run serve &
    FRONTEND_PID=$!
    info "前端服务启动成功 (PID: $FRONTEND_PID)"
    cd ..
}

# 显示访问信息
show_access_info() {
    echo ""
    info "===== 服务启动成功 ====="
    info "前端访问地址: http://localhost:5588"
    info "后端API地址: http://localhost:5688/api/v1"
    info "管理员账号: admin"
    info "管理员密码: admin123456@"
    echo ""
    info "按 Ctrl+C 停止服务"
}

# 清理函数
cleanup() {
    info "正在停止服务..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$CELERY_PID" ]; then
        kill $CELERY_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    info "服务已停止"
    exit 0
}

# 主函数
main() {
    info "开始启动大型模型构建管理平台..."
    
    # 注册退出处理函数
    trap cleanup SIGINT SIGTERM
    
    create_directories
    check_redis
    install_backend_deps
    install_frontend_deps
    init_db
    collect_static
    check_environment
    start_backend
    start_frontend
    show_access_info
    
    # 保持脚本运行
    wait
}

# 执行主函数
main 