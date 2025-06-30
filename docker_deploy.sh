#!/bin/bash

# 大型模型构建管理平台Docker部署脚本
# 此脚本用于在生产环境中通过Docker方式部署项目

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

# 检查Docker环境
check_docker() {
    info "检查Docker环境..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker未安装，请先安装Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    fi
    
    # 检查Docker服务状态
    if ! docker info &> /dev/null; then
        error "Docker服务未启动或当前用户没有权限访问Docker"
        exit 1
    fi
    
    info "Docker环境检查通过"
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
    
    # 配置Redis连接（使用Docker服务名）
    sed -i 's@redis://localhost:6379/0@redis://redis:6379/0@g' backend/.env 2>/dev/null
    
    # 设置静态文件路径
    sed -i 's@STATIC_ROOT=./static@STATIC_ROOT=/app/static@g' backend/.env 2>/dev/null
    sed -i 's@MEDIA_ROOT=./media@MEDIA_ROOT=/app/media@g' backend/.env 2>/dev/null
    
    info "环境配置更新完成"
}

# 创建必要的目录
create_directories() {
    info "创建必要的目录..."
    mkdir -p logs
    mkdir -p backend/logs
    mkdir -p backend/media
    mkdir -p backend/static
    info "目录创建完成"
}

# 修改Docker Compose文件
update_docker_compose() {
    info "更新Docker Compose配置..."
    
    # 检查docker-compose.yml文件是否存在
    if [ ! -f docker-compose.yml ]; then
        error "未找到docker-compose.yml文件"
        exit 1
    fi
    
    # 为PostgreSQL添加配置（如果需要）
    if grep -q "DB_ENGINE=django.db.backends.postgresql" backend/.env; then
        if ! grep -q "postgres:" docker-compose.yml; then
            warn "Docker Compose配置中未找到PostgreSQL服务，将添加PostgreSQL配置..."
            
            # 从.env文件读取数据库配置
            DB_NAME=$(grep DB_NAME backend/.env | cut -d= -f2)
            DB_USER=$(grep DB_USER backend/.env | cut -d= -f2)
            DB_PASSWORD=$(grep DB_PASSWORD backend/.env | cut -d= -f2)
            
            # 创建临时文件
            TEMP_FILE=$(mktemp)
            
            # 复制原文件到临时文件
            cp docker-compose.yml $TEMP_FILE
            
            # 在redis服务后添加postgres服务
            sed '/redis:/i\
  # PostgreSQL数据库\
  postgres:\
    image: postgis/postgis:15-3.4\
    container_name: big_model_app_postgres\
    restart: always\
    environment:\
      - POSTGRES_DB='$DB_NAME'\
      - POSTGRES_USER='$DB_USER'\
      - POSTGRES_PASSWORD='$DB_PASSWORD'\
    volumes:\
      - postgres_data:/var/lib/postgresql/data\
    ports:\
      - "5433:5432"\
    healthcheck:\
      test: ["CMD-SHELL", "pg_isready -U '$DB_USER'
' $TEMP_FILE > docker-compose.yml
            
            # 在volumes部分添加postgres_data
            sed '/volumes:/a\
  postgres_data:' docker-compose.yml > $TEMP_FILE
            mv $TEMP_FILE docker-compose.yml
            
            # 修改后端服务依赖
            sed -i 's/depends_on:/depends_on:\n      - postgres/g' docker-compose.yml
            
            info "已添加PostgreSQL配置到Docker Compose文件"
        fi
    fi
    
    # 如果使用自定义端口，更新前端服务端口配置
    BACKEND_PORT=$(grep BACKEND_PORT backend/.env | cut -d= -f2 2>/dev/null)
    if [ ! -z "$BACKEND_PORT" ] && [ "$BACKEND_PORT" != "8000" ]; then
        sed -i "s/command: gunicorn.*/command: gunicorn big_model_app.wsgi:application --bind 0.0.0.0:$BACKEND_PORT/g" docker-compose.yml
        info "已更新后端服务端口为 $BACKEND_PORT"
    fi
    
    info "Docker Compose配置更新完成"
}

# 构建和启动Docker容器
start_containers() {
    info "构建并启动Docker容器..."
    
    # 拉取基础镜像
    info "拉取基础镜像..."
    docker-compose pull
    
    # 构建镜像
    info "构建应用镜像..."
    docker-compose build
    
    # 启动容器
    info "启动容器..."
    docker-compose up -d
    
    # 检查容器状态
    sleep 5
    CONTAINERS=$(docker-compose ps -q)
    if [ -z "$CONTAINERS" ]; then
        error "容器启动失败"
        exit 1
    fi
    
    # 检查每个容器的状态
    for container in $CONTAINERS; do
        STATUS=$(docker inspect -f '{{.State.Status}}' $container)
        if [ "$STATUS" != "running" ]; then
            NAME=$(docker inspect -f '{{.Name}}' $container | sed 's/^\///')
            error "容器 $NAME 启动失败，状态为: $STATUS"
            warn "请使用 'docker logs $NAME' 查看错误日志"
        fi
    done
    
    info "Docker容器启动完成"
}

# 初始化数据库
init_database() {
    info "初始化数据库..."
    
    # 等待数据库准备就绪
    info "等待数据库准备就绪..."
    sleep 10
    
    # 执行数据库迁移
    info "执行数据库迁移..."
    docker-compose exec -T backend python manage.py makemigrations
    docker-compose exec -T backend python manage.py migrate
    
    # 初始化数据
    info "初始化数据..."
    docker-compose exec -T backend python init_db.py || {
        warn "初始化数据脚本执行失败，尝试创建默认管理员用户..."
        docker-compose exec -T backend python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123456@')
    print('创建管理员用户成功')
else:
    print('管理员用户已存在')
"
    }
    
    # 收集静态文件
    info "收集静态文件..."
    docker-compose exec -T backend python manage.py collectstatic --noinput
    
    info "数据库初始化完成"
}

# 检查服务健康状态
check_service_health() {
    info "检查服务健康状态..."
    
    # 获取前端容器IP
    FRONTEND_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' big_model_app_frontend)
    
    # 等待服务启动
    info "等待服务完全启动..."
    sleep 10
    
    # 检查前端服务
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:5588/ | grep -q "200\|301\|302"; then
        info "前端服务正常运行"
    else
        warn "前端服务可能未正常运行，请手动检查"
    fi
    
    # 检查后端API
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:5588/api/v1/ | grep -q "200\|401\|403"; then
        info "后端API服务正常运行"
    else
        warn "后端API服务可能未正常运行，请手动检查"
    fi
    
    info "服务健康检查完成"
}

# 显示部署信息
show_deployment_info() {
    echo ""
    info "===== 大型模型构建管理平台Docker部署完成 ====="
    info "前端访问地址: http://localhost:5588"
    info "后端API地址: http://localhost:5588/api/v1"
    info "管理员账号: admin"
    info "管理员密码: admin123456@"
    echo ""
    info "Docker服务状态:"
    docker-compose ps
    echo ""
    info "查看容器日志: docker-compose logs -f [服务名]"
    info "停止服务: bash docker_stop.sh"
    info "重启服务: docker-compose restart"
}

# 主函数
main() {
    info "开始Docker部署大型模型构建管理平台..."
    
    check_docker
    update_env_config
    create_directories
    update_docker_compose
    start_containers
    init_database
    check_service_health
    show_deployment_info
}

# 执行主函数
main 