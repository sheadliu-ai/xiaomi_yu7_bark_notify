# 构建阶段
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 最终阶段
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
# 复制 yu7_notify.py
COPY yu7_notify.py .

# 复制 configBAK.toml 并重命名为 config.toml
COPY configBAK.toml config.toml

# 安装 cron
RUN apt-get update && apt-get install -y cron

# 添加 cron 规则
RUN echo "*/5 * * * * python /app/yu7_notify.py >> /var/log/cron.log 2>&1" >> /etc/crontab

# 启动 cron 服务
CMD ["cron", "-f"]