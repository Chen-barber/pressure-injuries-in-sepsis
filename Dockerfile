# 使用Python 3.11作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
# 注意：PORT环境变量由Railway在运行时注入，不要在这里设置
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用文件
COPY app.py .
COPY rf_model.pkl .
COPY shap_explainer.pkl .
COPY feature_info.pkl .

# 暴露端口（Railway会注入PORT环境变量，通常是8080）
# 注意：EXPOSE只是文档说明，实际端口由Railway的PORT变量决定
EXPOSE 8080

# 健康检查（增加启动等待时间，Streamlit需要时间加载模型）
# 注意：Railway使用自己的健康检查，这个可能不会被使用
HEALTHCHECK --interval=30s --timeout=15s --start-period=120s --retries=5 \
    CMD sh -c "curl --fail http://localhost:${PORT:-8080}/ || exit 1"

# 启动Streamlit应用
# Railway会注入PORT环境变量（通常是8080），必须使用它
# 使用shell格式以支持环境变量
CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true"]

