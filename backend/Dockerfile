FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 创建日志目录
RUN mkdir -p logs

# 创建媒体和静态文件目录
RUN mkdir -p media static

# 暴露端口
EXPOSE 5688

# 设置启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5688", "--workers", "4", "--timeout", "120", "big_model_app.wsgi:application"] 