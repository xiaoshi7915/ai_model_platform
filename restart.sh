#!/bin/bash

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

# 检查正在运行的服务并停止
stop_services() {
    info "停止正在运行的服务..."
    
    # 查找并停止前端服务
    FE_PID=$(ps aux | grep "npm run serve" | grep -v grep | awk '{print $2}')
    if [ ! -z "$FE_PID" ]; then
        warn "发现正在运行的前端服务 (PID: $FE_PID)，停止中..."
        kill $FE_PID 2>/dev/null
        sleep 2
    fi
    
    # 查找并停止后端服务
    BE_PID=$(ps aux | grep "python manage.py runserver" | grep -v grep | awk '{print $2}')
    if [ ! -z "$BE_PID" ]; then
        warn "发现正在运行的后端服务 (PID: $BE_PID)，停止中..."
        kill $BE_PID 2>/dev/null
        sleep 2
    fi
    
    # 查找并停止celery服务
    CELERY_PID=$(ps aux | grep "celery -A" | grep -v grep | awk '{print $2}')
    if [ ! -z "$CELERY_PID" ]; then
        warn "发现正在运行的Celery服务 (PID: $CELERY_PID)，停止中..."
        kill $CELERY_PID 2>/dev/null
        sleep 2
    fi
    
    # 确认是否还有服务在运行
    if ps aux | grep -E "npm run serve|python manage.py runserver|celery -A" | grep -v grep | awk '{print $2}' | grep -q .; then
        error "仍有服务在运行，将强制停止..."
        ps aux | grep -E "npm run serve|python manage.py runserver|celery -A" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null
        sleep 1
    fi
    
    info "所有服务已停止"
}

# 检查所需权限并修复
fix_permissions() {
    info "修复文件权限..."
    
    # 给所有脚本添加执行权限
    chmod +x *.sh
    
    # 确保目录存在且有正确权限
    mkdir -p backend/logs backend/media backend/static logs
    chmod -R 755 backend/logs backend/media backend/static logs
    
    info "权限修复完成"
}

# 运行通用修复脚本
run_fix_scripts() {
    info "运行修复脚本..."
    
    # 运行通用修复脚本
    if [ -f "fix_problems.sh" ]; then
        info "运行fix_problems.sh..."
        ./fix_problems.sh
    else
        warn "未找到fix_problems.sh脚本，跳过"
    fi
    
    # 运行前端修复脚本
    if [ -f "frontend_fix.sh" ]; then
        info "运行frontend_fix.sh..."
        ./frontend_fix.sh
    else
        warn "未找到frontend_fix.sh脚本，跳过"
    fi
    
    info "修复脚本运行完成"
}

# 启动所有服务
start_services() {
    info "启动所有服务..."
    
    # 使用快速启动脚本启动服务
    if [ -f "quick_start.sh" ]; then
        info "通过quick_start.sh启动服务..."
        ./quick_start.sh
    else
        warn "未找到quick_start.sh脚本，尝试手动启动服务..."
        
        # 手动启动后端
        info "启动后端服务..."
        cd backend || { error "无法进入backend目录"; exit 1; }
        
        # 激活虚拟环境（如果存在）
        if [ -d "../.venv" ]; then
            source ../.venv/bin/activate
        fi
        
        # 启动后端
        export PYTHONPATH=$PYTHONPATH:$(pwd)
        export DJANGO_SETTINGS_MODULE=big_model_app.settings
        python manage.py runserver 0.0.0.0:5688 &
        BACKEND_PID=$!
        info "后端服务启动成功 (PID: $BACKEND_PID)"
        
        # 启动Celery Worker（如果Redis可用）
        if command -v redis-cli >/dev/null 2>&1 && redis-cli ping >/dev/null 2>&1; then
            info "启动Celery Worker..."
            celery -A big_model_app worker --loglevel=info &
            CELERY_PID=$!
            info "Celery Worker启动成功 (PID: $CELERY_PID)"
        else
            warn "Redis未运行，跳过启动Celery"
        fi
        
        cd ..
        
        # 启动前端
        info "启动前端服务..."
        cd frontend || { error "无法进入frontend目录"; exit 1; }
        npm run serve &
        FRONTEND_PID=$!
        info "前端服务启动成功 (PID: $FRONTEND_PID)"
        cd ..
    fi
}

# 显示访问信息
show_access_info() {
    echo ""
    info "===== 服务已重启成功 ====="
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
    stop_services
    info "服务已停止"
    exit 0
}

# 主函数
main() {
    info "===== 开始重启大型模型构建管理平台 ====="
    
    # 注册退出处理函数
    trap cleanup SIGINT SIGTERM
    
    # 停止正在运行的服务
    stop_services
    
    # 修复权限
    fix_permissions
    
    # 运行修复脚本
    run_fix_scripts
    
    # 启动所有服务
    start_services
    
    # 显示访问信息
    show_access_info
    
    # 保持脚本运行
    wait
}

# 执行主函数
main 