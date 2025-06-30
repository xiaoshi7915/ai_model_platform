#!/bin/bash

# 大型模型构建管理平台初始化脚本

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

# 检查操作系统
check_os() {
    info "检查操作系统..."
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        info "检测到操作系统: $OS $VER"
    else
        error "无法检测操作系统类型"
        OS="Unknown"
    fi
}

# 创建Python虚拟环境
create_venv() {
    info "创建Python虚拟环境..."
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        info "虚拟环境创建成功"
    else
        info "虚拟环境已存在"
    fi
    
    # 激活虚拟环境
    source .venv/bin/activate
    
    # 升级pip
    pip install --upgrade pip
    
    info "Python虚拟环境准备完成"
}

# 设置数据库
setup_database() {
    info "设置数据库..."
    cd backend || { error "无法进入backend目录"; exit 1; }
    
    # 检查.env文件
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            info "从.env.example创建了.env文件"
        else
            warn "未找到.env.example文件，创建默认.env文件..."
            cat > .env << EOF
# Django配置
SECRET_KEY=django-insecure-default-key
DEBUG=True

# 数据库配置
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=

# 服务配置
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://localhost:5588

# Redis配置
REDIS_URL=redis://localhost:6379/0

# Celery配置
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF
            info ".env文件创建成功"
        fi
    fi
    
    # 数据库初始化
    info "初始化数据库..."
    python manage.py makemigrations
    python manage.py migrate
    
    # 创建超级用户
    info "创建超级用户..."
    if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0) if User.objects.filter(username='admin').exists() else exit(1)"; then
        python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123456@')"
        info "超级用户创建成功 (用户名: admin, 密码: admin123456@)"
    else
        info "超级用户已存在"
    fi
    
    # 运行初始化脚本
    info "运行数据库初始化脚本..."
    python init_db.py
    
    # 初始化各模块测试数据
    info "初始化测试数据..."
    
    # 应用中心测试数据
    if [ -f "app_center/init_applications.py" ]; then
        info "初始化应用中心测试数据..."
        python app_center/init_applications.py
    else
        warn "未找到应用中心初始化脚本"
    fi
    
    # 数据中心测试数据
    if [ -f "data_center/init_datasets.py" ]; then
        info "初始化数据中心测试数据..."
        python data_center/init_datasets.py
    else
        warn "未找到数据中心初始化脚本"
    fi
    
    # 数据中心知识库测试数据
    if [ -f "data_center/init_knowledge_base.py" ]; then
        info "初始化知识库测试数据..."
        python data_center/init_knowledge_base.py
    else
        warn "未找到知识库初始化脚本"
    fi
    
    # 训练中心测试数据
    if [ -f "training_center/init_training.py" ]; then
        info "初始化训练中心测试数据..."
        python training_center/init_training.py
    else
        warn "未找到训练中心初始化脚本"
    fi
    
    # 训练任务测试数据
    if [ -f "training_center/init_training_jobs.py" ]; then
        info "初始化训练任务测试数据..."
        python training_center/init_training_jobs.py
    else
        warn "未找到训练任务初始化脚本"
    fi
    
    
    cd ..
    info "数据库设置完成"
}

# 修复文件权限
fix_permissions() {
    info "修复文件权限..."
    
    # 修复脚本权限
    chmod +x *.sh
    
    # 确保目录存在且有正确权限
    mkdir -p backend/logs backend/media backend/static logs
    chmod -R 755 backend/logs backend/media backend/static logs
    
    # 确保backend/manage.py可执行
    chmod +x backend/manage.py
    
    info "权限修复完成"
}

# 安装前端依赖
setup_frontend() {
    info "设置前端环境..."
    cd frontend || { error "无法进入frontend目录"; exit 1; }
    
    # 安装依赖
    npm install --legacy-peer-deps
    
    # 检查@vue/cli-service是否存在
    if [ ! -f "node_modules/.bin/vue-cli-service" ]; then
        warn "@vue/cli-service不存在，安装@vue/cli-service..."
        npm install @vue/cli-service@~5.0.8 --legacy-peer-deps
    fi
    
    # 添加软链接确保命令可用
    if [ ! -f "node_modules/.bin/vue-cli-service" ]; then
        warn "创建vue-cli-service软链接..."
        mkdir -p node_modules/.bin
        ln -sf ../node_modules/@vue/cli-service/bin/vue-cli-service.js node_modules/.bin/vue-cli-service
        chmod +x node_modules/.bin/vue-cli-service
    fi
    
    cd ..
    info "前端环境设置完成"
}

# 运行修复脚本
run_fix_scripts() {
    info "运行修复脚本..."
    
    # 运行通用修复脚本
    if [ -f "fix_problems.sh" ]; then
        info "运行fix_problems.sh..."
        ./fix_problems.sh
    fi
    
    # 运行前端修复脚本
    if [ -f "frontend_fix.sh" ]; then
        info "运行frontend_fix.sh..."
        ./frontend_fix.sh
    fi
    
    info "修复脚本运行完成"
}

# 显示完成信息
show_completion_info() {
    echo ""
    info "===== 初始化完成 ====="
    info "可以通过以下命令启动应用:"
    echo "  ./restart.sh    # 启动并监控应用，显示访问信息"
    echo "  ./quick_start.sh # 快速启动应用并监控"
    echo ""
    info "访问信息:"
    info "前端访问地址: http://localhost:5588"
    info "后端API地址: http://localhost:5688/api/v1"
    info "管理员账号: admin"
    info "管理员密码: admin123456@"
    echo ""
}

# 主函数
main() {
    info "===== 开始初始化大型模型构建管理平台 ====="
    
    check_os
    # 跳过系统依赖安装
    # install_system_deps
    create_venv
    fix_permissions
    
    # 安装后端依赖
    info "安装后端依赖..."
    source .venv/bin/activate
    cd backend || { error "无法进入backend目录"; exit 1; }
    pip install -r requirements.txt
    cd ..
    
    setup_database
    setup_frontend
    run_fix_scripts
    
    # 确保后端静态文件收集
    info "收集静态文件..."
    cd backend || { error "无法进入backend目录"; exit 1; }
    python manage.py collectstatic --noinput
    cd ..
    
    show_completion_info
    
    info "===== 初始化脚本执行完毕 ====="
}

# 执行主函数
main 