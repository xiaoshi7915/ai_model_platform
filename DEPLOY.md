# 大型模型构建管理平台 - 详细部署指南

## 系统要求

### 最低配置
- **CPU**: 4核心
- **内存**: 8GB RAM
- **存储**: 20GB可用空间
- **操作系统**: Ubuntu 20.04/22.04、CentOS 8、Debian 11或更高版本
- **网络**: 可访问互联网以下载依赖

### 推荐配置
- **CPU**: 8核心或更高
- **内存**: 16GB RAM或更高
- **存储**: 100GB SSD
- **GPU**: NVIDIA GPU (适用于模型训练)
- **操作系统**: Ubuntu 22.04 LTS

## 软件环境要求

### 后端环境
- Python 3.9或更高版本
- Redis 6.0或更高版本
- PostgreSQL 14.0或更高版本 (可选，默认使用SQLite)

### 前端环境
- Node.js 16.x或更高版本
- npm 8.x或更高版本

## 部署方式

本文档提供三种部署方式：
1. **快速启动**: 适用于开发和测试环境
2. **生产部署**: 适用于正式环境
3. **Docker部署**: 适用于容器化环境

## 1. 快速启动（开发环境）

适合快速体验系统功能或进行开发调试。

### 步骤1：克隆代码仓库
```bash
git clone <项目仓库URL>
cd 项目目录
```

### 步骤2：修复常见问题
```bash
# 给脚本添加执行权限
chmod +x fix_problems.sh

# 运行修复脚本
./fix_problems.sh
```

### 步骤3：启动开发环境
```bash
# 给启动脚本添加执行权限
chmod +x quick_start.sh

# 运行启动脚本
./quick_start.sh
```

### 步骤4：访问系统
- 前端访问地址：http://localhost:5588/
- 后端API地址：http://localhost:5688/api/v1/
- 管理员账号：admin
- 管理员密码：admin123456@

## 2. 生产部署

适合正式环境使用，提供更好的性能和安全性。

### 步骤1：安装系统依赖
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nodejs npm redis-server nginx

# CentOS/RHEL
sudo yum update
sudo yum install -y python39 nodejs npm redis nginx
```

### 步骤2：安装PostgreSQL（推荐）
```bash
# Ubuntu/Debian
sudo apt install -y postgresql postgresql-contrib libpq-dev

# CentOS/RHEL
sudo yum install -y postgresql postgresql-server postgresql-contrib postgresql-devel
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 步骤3：配置PostgreSQL（可选）
```bash
# 切换到postgres用户
sudo -u postgres psql

# 创建数据库用户和数据库
CREATE USER bigmodel WITH PASSWORD 'your_password';
CREATE DATABASE bigmodeldb WITH OWNER bigmodel;
\q

# 安装pgvector扩展（如果需要向量搜索功能）
sudo apt install postgresql-server-dev-14  # 根据PostgreSQL版本调整
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
cd ..

# 启用pgvector扩展
sudo -u postgres psql -d bigmodeldb -c 'CREATE EXTENSION IF NOT EXISTS vector;'
```

### 步骤4：修改环境配置
```bash
# 编辑环境配置文件
cd backend
cp .env.example .env  # 如果存在示例配置文件
nano .env  # 或者使用其他编辑器

# 配置数据库连接（使用PostgreSQL）
# 将以下内容添加到.env文件
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=bigmodeldb
DATABASE_USER=bigmodel
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 步骤5：执行生产部署脚本
```bash
# 回到项目根目录
cd ..

# 给脚本添加执行权限
chmod +x production_deploy.sh

# 运行部署脚本
./production_deploy.sh
```

### 步骤6：配置Nginx（推荐）
```bash
# 创建Nginx配置文件
sudo nano /etc/nginx/sites-available/bigmodel

# 添加以下配置
server {
    listen 80;
    server_name your_domain_or_ip;

    location /api/ {
        proxy_pass http://127.0.0.1:5688;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/project/backend/static/;
    }

    location /media/ {
        alias /path/to/project/backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:5588;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 启用站点配置
sudo ln -s /etc/nginx/sites-available/bigmodel /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 步骤7：访问系统
- Web访问地址：http://your_domain_or_ip/
- 管理员账号：admin
- 管理员密码：admin123456@

## 3. Docker部署

适合容器化环境，简化部署流程，无需担心依赖问题。

### 步骤1：安装Docker和Docker Compose
```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh

# 启动Docker服务
sudo systemctl enable docker
sudo systemctl start docker

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 步骤2：克隆代码仓库
```bash
git clone <项目仓库URL>
cd 项目目录
```

### 步骤3：修改环境配置
```bash
# 编辑环境配置文件
cd backend
cp .env.example .env  # 如果存在示例配置文件
nano .env  # 或者使用其他编辑器

# 修改Redis连接配置
REDIS_URL=redis://redis:6379/0

# 如果使用Docker内置PostgreSQL
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
```

### 步骤4：编辑docker-compose.yml
```bash
# 回到项目根目录
cd ..

# 确保docker-compose.yml包含所有必要服务
nano docker-compose.yml
```

确保docker-compose.yml包含以下服务：
- backend（Django API服务）
- celery（异步任务处理）
- frontend（Vue.js前端）
- redis（消息队列和缓存）
- db（PostgreSQL数据库，可选）

### 步骤5：构建和启动容器
```bash
# 构建并启动所有服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps
```

### 步骤6：初始化数据库（首次部署）
```bash
# 执行数据库迁移
docker-compose exec backend python manage.py migrate

# 初始化默认数据
docker-compose exec backend python init_db.py
```

### 步骤7：访问系统
- Web访问地址：http://your_domain_or_ip:5588/
- 管理员账号：admin
- 管理员密码：admin123456@

## 常见问题排查指南

### 1. 前端启动失败

#### 症状：
- `npm run serve` 命令失败
- 浏览器无法访问前端页面

#### 排查步骤：
1. **检查Node.js环境**：
   ```bash
   node -v
   npm -v
   ```
   确保Node.js版本≥16.x，npm版本≥8.x

2. **检查前端依赖**：
   ```bash
   cd frontend
   npm install --legacy-peer-deps
   ```

3. **检查vue-cli-service**：
   ```bash
   cd frontend
   # 安装@vue/cli-service
   npm install @vue/cli-service@~5.0.8 --legacy-peer-deps
   ```

4. **创建软链接**：
   ```bash
   cd frontend
   mkdir -p node_modules/.bin
   ln -sf ../node_modules/@vue/cli-service/bin/vue-cli-service.js node_modules/.bin/vue-cli-service
   chmod +x node_modules/.bin/vue-cli-service
   ```

5. **使用修复脚本**：
   ```bash
   ./fix_problems.sh
   ```

### 2. 后端启动失败

#### 症状：
- `python manage.py runserver` 命令失败
- API请求返回连接错误

#### 排查步骤：
1. **检查Python环境**：
   ```bash
   python --version
   ```
   确保Python版本≥3.9

2. **检查虚拟环境**：
   ```bash
   # 创建新的虚拟环境
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # 或
   .venv\Scripts\activate  # Windows
   ```

3. **检查依赖安装**：
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **检查环境配置**：
   ```bash
   cd backend
   # 确保.env文件存在
   cp .env.example .env  # 如果需要
   ```

5. **数据库迁移问题**：
   ```bash
   cd backend
   python manage.py makemigrations
   python manage.py migrate
   ```

### 3. Redis连接问题

#### 症状：
- Celery任务无法执行
- 应用报Redis连接错误

#### 排查步骤：
1. **检查Redis服务状态**：
   ```bash
   sudo systemctl status redis
   # 或
   sudo service redis-server status
   ```

2. **启动Redis服务**：
   ```bash
   sudo systemctl start redis
   # 或
   sudo service redis-server start
   ```

3. **测试Redis连接**：
   ```bash
   redis-cli ping
   # 应返回PONG
   ```

4. **检查.env配置**：
   ```bash
   cd backend
   # 确认REDIS_URL配置正确
   # 本地运行应为: redis://localhost:6379/0
   # Docker环境应为: redis://redis:6379/0
   ```

### 4. PostgreSQL连接问题

#### 症状：
- 数据库迁移失败
- 应用报数据库连接错误

#### 排查步骤：
1. **检查PostgreSQL服务状态**：
   ```bash
   sudo systemctl status postgresql
   ```

2. **启动PostgreSQL服务**：
   ```bash
   sudo systemctl start postgresql
   ```

3. **检查数据库用户和权限**：
   ```bash
   sudo -u postgres psql
   \du  # 列出所有用户
   \l   # 列出所有数据库
   ```

4. **检查.env配置**：
   ```bash
   cd backend
   # 确认数据库连接配置正确
   ```

5. **手动测试连接**：
   ```bash
   psql -U your_db_user -h localhost -d your_db_name
   # 输入密码后应能连接成功
   ```

## 升级指南

### 升级代码

1. **更新代码仓库**：
   ```bash
   git pull origin main  # 或其他分支
   ```

2. **更新依赖**：
   ```bash
   # 后端依赖
   cd backend
   pip install -r requirements.txt --upgrade
   
   # 前端依赖
   cd ../frontend
   npm update
   ```

3. **执行数据库迁移**：
   ```bash
   cd ../backend
   python manage.py migrate
   ```

4. **重启服务**：
   ```bash
   # 如果使用标准部署
   ./production_deploy.sh
   
   # 如果使用Docker
   docker-compose down
   docker-compose up -d --build
   ```

## 备份与恢复

### 数据库备份

#### SQLite备份：
```bash
# 进入backend目录
cd backend

# 备份数据库文件
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)
```

#### PostgreSQL备份：
```bash
# 导出数据库
pg_dump -U your_db_user -h localhost your_db_name > backup_$(date +%Y%m%d).sql
```

### 恢复备份

#### SQLite恢复：
```bash
# 进入backend目录
cd backend

# 恢复数据库文件
cp db.sqlite3.backup your_backup_file db.sqlite3
```

#### PostgreSQL恢复：
```bash
# 恢复数据库
psql -U your_db_user -h localhost your_db_name < your_backup_file.sql
```

## 系统管理

### 日志管理

#### 查看日志：
```bash
# 后端日志
cat backend/logs/django.log

# Celery日志
cat backend/logs/celery.log

# Nginx日志
cat /var/log/nginx/access.log
cat /var/log/nginx/error.log
```

#### 清理日志：
```bash
# 压缩旧日志
cd backend/logs
find . -name "*.log" -mtime +7 -exec gzip {} \;

# 删除超过30天的压缩日志
find . -name "*.gz" -mtime +30 -delete
```

### 性能监控

#### 资源使用情况：
```bash
# 查看CPU和内存使用
htop

# 查看磁盘使用
df -h

# 查看特定目录大小
du -sh backend/media/
```

#### 数据库优化：
```bash
# PostgreSQL性能分析
cd backend
python manage.py analyze_db
```

## 结语

恭喜！您已经成功部署了大型模型构建管理平台。如果在部署过程中遇到任何问题，请查阅上面的故障排除指南或联系技术支持团队。

祝您使用愉快！ 