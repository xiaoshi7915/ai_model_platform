#!/bin/bash

# 大型模型构建管理平台生产环境部署脚本 - 源码启动版本
# 此脚本用于在生产环境中通过源码方式启动项目

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

# 检查Python环境
check_python() {
    info "检查Python环境..."
    if ! command -v python3 &> /dev/null; then
        error "Python 3未安装，请先安装Python 3.8或更高版本"
        exit 1
    fi
    
    python_version=$(python3 --version | awk '{print $2}')
    python_major=$(echo $python_version | cut -d. -f1)
    python_minor=$(echo $python_version | cut -d. -f2)
    
    if [[ $python_major -lt 3 || ($python_major -eq 3 && $python_minor -lt 8) ]]; then
        error "Python版本过低，需要Python 3.8或更高版本，当前版本为$python_version"
        exit 1
    fi
    
    if ! command -v pip3 &> /dev/null; then
        error "pip3未安装，请先安装pip3"
        exit 1
    fi
    
    info "Python环境检查通过: $python_version"
}

# 检查Node.js环境
check_nodejs() {
    info "检查Node.js环境..."
    if ! command -v node &> /dev/null; then
        error "Node.js未安装，请先安装Node.js"
        exit 1
    fi
    
    node_version=$(node --version)
    node_major=$(echo $node_version | cut -d. -f1 | tr -d 'v')
    
    if [[ $node_major -lt 14 ]]; then
        error "Node.js版本过低，需要Node.js 14或更高版本，当前版本为$node_version"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        error "npm未安装，请先安装npm"
        exit 1
    fi
    
    info "Node.js环境检查通过: $node_version"
}

# 检查Redis服务
check_redis() {
    info "检查Redis服务..."
    if ! command -v redis-cli &> /dev/null; then
        warn "Redis客户端未安装，请确保Redis服务已安装"
    else
        if redis-cli ping > /dev/null 2>&1; then
            info "Redis服务正常运行"
        else
            warn "Redis服务未运行，尝试启动..."
            
            if command -v systemctl &> /dev/null; then
                sudo systemctl start redis
            elif command -v service &> /dev/null; then
                sudo service redis-server start
            else
                warn "无法自动启动Redis服务，请手动启动"
            fi
        fi
    fi
}

# 检查PostgreSQL服务
check_postgresql() {
    info "检查PostgreSQL服务..."
    
    # 从.env文件读取数据库配置
    DB_HOST=$(grep DB_HOST backend/.env | cut -d= -f2)
    DB_PORT=$(grep DB_PORT backend/.env | cut -d= -f2)
    DB_NAME=$(grep DB_NAME backend/.env | cut -d= -f2)
    DB_USER=$(grep DB_USER backend/.env | cut -d= -f2)
    DB_PASSWORD=$(grep DB_PASSWORD backend/.env | cut -d= -f2)
    
    # 如果为本地主机，尝试检查服务状态
    if [[ "$DB_HOST" == "localhost" || "$DB_HOST" == "127.0.0.1" ]]; then
        if command -v pg_isready &> /dev/null; then
            pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                info "PostgreSQL服务正常运行"
            else
                warn "PostgreSQL服务未运行，请确保PostgreSQL服务已启动"
            fi
        else
            warn "未找到pg_isready命令，无法检查PostgreSQL服务状态"
        fi
    else
        # 对于远程数据库，尝试连接测试
        if command -v psql &> /dev/null; then
            export PGPASSWORD=$DB_PASSWORD
            psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1" > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                info "可以连接到远程PostgreSQL服务"
            else
                warn "无法连接到远程PostgreSQL服务，请检查连接配置和防火墙设置"
            fi
            unset PGPASSWORD
        else
            warn "未找到psql命令，无法测试数据库连接"
        fi
    fi
}

# 安装虚拟环境
setup_venv() {
    info "设置Python虚拟环境..."
    if ! command -v python3 -m venv &> /dev/null; then
        pip3 install virtualenv
    fi
    
    if [ ! -d .venv ]; then
        python3 -m venv .venv
    fi
    
    # 激活虚拟环境
    source .venv/bin/activate
    
    # 检查虚拟环境是否激活
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        error "虚拟环境激活失败"
        exit 1
    fi
    
    info "Python虚拟环境设置完成"
}

# 安装后端依赖
install_backend_deps() {
    info "安装后端依赖..."
    
    # 进入后端目录
    cd backend || { error "无法进入backend目录"; exit 1; }
    
    # 安装依赖
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        error "安装后端依赖失败"
        cd ..
        exit 1
    fi
    
    info "后端依赖安装完成"
    cd ..
}

# 构建前端
build_frontend() {
    info "构建前端..."
    
    # 进入前端目录
    cd frontend || { error "无法进入frontend目录"; exit 1; }
    
    # 安装依赖
    npm install --production
    if [ $? -ne 0 ]; then
        error "安装前端依赖失败"
        cd ..
        exit 1
    fi
    
    # 构建生产版本
    npm run build
    if [ $? -ne 0 ]; then
        error "构建前端失败"
        cd ..
        exit 1
    fi
    
    info "前端构建完成"
    cd ..
}

# 创建必要的目录
create_directories() {
    info "创建必要的目录..."
    mkdir -p backend/logs
    mkdir -p backend/media
    mkdir -p backend/static
    info "目录创建完成"
}

# 更新环境配置
update_env_config() {
    info "更新环境配置..."
    
    # 检查backend/.env文件是否存在
    if [ ! -f backend/.env ]; then
        warn "未找到backend/.env文件，使用示例配置..."
        cp backend/.env.example backend/.env 2>/dev/null || warn "未找到示例配置文件"
    fi
    
    # 设置生产环境变量
    sed -i 's/DEBUG=True/DEBUG=False/g' backend/.env 2>/dev/null
    
    # 配置Redis连接（使用本地）
    sed -i 's@redis://redis:6379/0@redis://localhost:6379/0@g' backend/.env 2>/dev/null
    
    info "环境配置更新完成"
}

# 执行数据库迁移
run_migrations() {
    info "执行数据库迁移..."
    
    cd backend || { error "无法进入backend目录"; exit 1; }
    
    # 检查是否已经安装了pgvector扩展
    if grep -q "postgresql" .env; then
        DB_HOST=$(grep DB_HOST .env | cut -d= -f2)
        DB_PORT=$(grep DB_PORT .env | cut -d= -f2)
        DB_NAME=$(grep DB_NAME .env | cut -d= -f2)
        DB_USER=$(grep DB_USER .env | cut -d= -f2)
        DB_PASSWORD=$(grep DB_PASSWORD .env | cut -d= -f2)
        
        warn "如果使用PostgreSQL，请确保数据库中已安装pgvector扩展"
        warn "可通过以下SQL在PostgreSQL中安装: CREATE EXTENSION IF NOT EXISTS vector;"
    fi
    
    # 生成迁移文件
    python manage.py makemigrations
    if [ $? -ne 0 ]; then
        error "生成迁移文件失败"
        cd ..
        exit 1
    fi
    
    # 执行迁移
    python manage.py migrate
    if [ $? -ne 0 ]; then
        error "执行数据库迁移失败"
        cd ..
        exit 1
    fi
    
    info "数据库迁移完成"
    cd ..
}

# 收集静态文件
collect_static() {
    info "收集静态文件..."
    
    cd backend || { error "无法进入backend目录"; exit 1; }
    
    python manage.py collectstatic --noinput
    if [ $? -ne 0 ]; then
        error "收集静态文件失败"
        cd ..
        exit 1
    fi
    
    info "静态文件收集完成"
    cd ..
}

# 初始化数据库
init_db() {
    info "初始化数据库..."
    
    cd backend || { error "无法进入backend目录"; exit 1; }
    
    # 检查init_db.py是否存在
    if [ -f init_db.py ]; then
        python init_db.py
        if [ $? -ne 0 ]; then
            warn "数据库初始化脚本执行出错，尝试创建超级用户..."
            python manage.py createsuperuser --noinput --username admin --email admin@example.com
        fi
    else
        warn "未找到init_db.py脚本，创建默认超级用户..."
        # 创建超级用户
        DJANGO_SUPERUSER_PASSWORD=admin123456@ python manage.py createsuperuser --noinput --username admin --email admin@example.com
    fi
    
    info "数据库初始化完成"
    cd ..
}

# 启动Gunicorn (生产环境Web服务器)
start_gunicorn() {
    info "启动Gunicorn..."
    
    cd backend || { error "无法进入backend目录"; exit 1; }
    
    # 检查Gunicorn是否安装
    if ! python -c "import gunicorn" > /dev/null 2>&1; then
        warn "Gunicorn未安装，正在安装..."
        pip install gunicorn
    fi
    
    # 获取CPU核心数
    CORES=$(nproc 2>/dev/null || echo 4)
    WORKERS=$((CORES * 2 + 1))
    
    # 启动Gunicorn
    gunicorn big_model_app.wsgi:application --bind 0.0.0.0:5688 --workers $WORKERS --access-logfile logs/access.log --error-logfile logs/error.log --daemon
    if [ $? -ne 0 ]; then
        error "启动Gunicorn失败"
        cd ..
        exit 1
    fi
    
    info "Gunicorn已启动 (端口: 5688, 工作进程: $WORKERS)"
    cd ..
}

# 启动Celery
start_celery() {
    info "启动Celery..."
    
    cd backend || { error "无法进入backend目录"; exit 1; }
    
    # 启动Celery Worker
    celery -A big_model_app worker --loglevel=info --logfile=logs/celery.log --pidfile=logs/celery.pid --detach
    if [ $? -ne 0 ]; then
        warn "启动Celery Worker失败，异步任务可能无法正常工作"
    else
        info "Celery Worker已启动"
    fi
    
    # 启动Celery Beat
    celery -A big_model_app beat --loglevel=info --logfile=logs/celerybeat.log --pidfile=logs/celerybeat.pid --detach
    if [ $? -ne 0 ]; then
        warn "启动Celery Beat失败，定时任务可能无法正常工作"
    else
        info "Celery Beat已启动"
    fi
    
    cd ..
}

# 配置Nginx
setup_nginx() {
    info "配置Nginx..."
    
    # 检查Nginx是否安装
    if ! command -v nginx &> /dev/null; then
        warn "Nginx未安装，请手动安装和配置Nginx"
        return
    fi
    
    # 创建Nginx配置文件
    cat > nginx.conf << EOF
server {
    listen 80;
    server_name _;  # 替换为您的域名
    
    client_max_body_size 100M;
    
    # 前端静态文件
    location / {
        root $(pwd)/frontend/dist;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }
    
    # 后端API
    location /api {
        proxy_pass http://127.0.0.1:5688;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # 静态文件
    location /static/ {
        alias $(pwd)/backend/static/;
    }
    
    # 媒体文件
    location /media/ {
        alias $(pwd)/backend/media/;
    }
    
    # 管理员界面
    location /admin {
        proxy_pass http://127.0.0.1:5688;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF
    
    # 检查配置文件
    sudo nginx -t -c $(pwd)/nginx.conf
    if [ $? -ne 0 ]; then
        warn "Nginx配置文件有误，请手动检查和修复"
    else
        info "Nginx配置文件已创建: $(pwd)/nginx.conf"
        info "可通过以下命令使用此配置启动Nginx:"
        info "sudo nginx -c $(pwd)/nginx.conf"
    fi
}

# 显示部署信息
show_deployment_info() {
    echo ""
    info "===== 大型模型构建管理平台部署完成 ====="
    info "后端API地址: http://localhost:5688/api/v1"
    
    if command -v nginx &> /dev/null; then
        info "前端访问地址: http://localhost/  (需启动Nginx)"
    else
        info "前端文件位置: $(pwd)/frontend/dist (请配置Web服务器指向此目录)"
    fi
    
    info "管理员账号: admin"
    info "管理员密码: admin123456@"
    echo ""
    info "后端日志位置: $(pwd)/backend/logs/"
    info "关闭服务: bash production_stop.sh"
}

# 主函数
main() {
    info "开始部署大型模型构建管理平台到生产环境..."
    
    check_python
    check_nodejs
    check_redis
    check_postgresql
    create_directories
    setup_venv
    install_backend_deps
    update_env_config
    run_migrations
    init_db
    collect_static
    build_frontend
    start_gunicorn
    start_celery
    setup_nginx
    show_deployment_info
}

# 执行主函数
main 