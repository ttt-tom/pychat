FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制应用代码和数据文件
COPY ./app /app
COPY ./faq_data.json /app/faq_data.json

# 安装依赖
RUN pip install --no-cache-dir -r /app/requirements.txt


# EXPOSE 8000

# 启动服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
