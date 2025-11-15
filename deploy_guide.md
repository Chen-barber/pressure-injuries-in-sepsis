# 部署指南 - Pressure Injuries in Sepsis 计算器

## 🚀 快速部署选项

### 选项1：Railway（推荐 - 最简单）

1. **在 [Railway.app](https://railway.app) 注册账号**
2. **创建新项目**
3. **从GitHub部署:**
   - 连接你的GitHub仓库
   - Railway会自动检测Dockerfile
   - 自动部署

4. **或从Dockerfile部署:**
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 选择你的仓库
   - Railway会构建并部署

5. **设置自定义域名:**
   - 前往 Settings → Domains
   - 添加自定义域名：`pressure-injuries-in-sepsis.railway.app`（或你自己的域名）

**Railway提供:**
- 免费套餐，每月$5额度
- 自动HTTPS
- 自定义域名
- 从Git自动部署

---

### 选项2：Render

1. **在 [Render.com](https://render.com) 注册账号**
2. **创建新的Web服务**
3. **连接GitHub仓库**
4. **配置:**
   - **名称:** `pressure-injuries-in-sepsis`
   - **环境:** Docker
   - **构建命令:** (自动检测)
   - **启动命令:** (自动检测)
   - **端口:** 8501

5. **部署**

**Render提供:**
- 有免费套餐
- 自动HTTPS
- 自定义域名
- 自动部署

---

### 选项3：Fly.io

1. **安装Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **登录:**
   ```bash
   fly auth login
   ```

3. **创建应用:**
   ```bash
   fly launch --name pressure-injuries-in-sepsis
   ```

4. **部署:**
   ```bash
   fly deploy
   ```

5. **设置自定义域名:**
   ```bash
   fly domains add pressure-injuries-in-sepsis.fly.dev
   ```

---

### 选项4：Google Cloud Run

1. **安装gcloud CLI**
2. **构建并推送:**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/sepsis-calculator
   gcloud run deploy pressure-injuries-in-sepsis \
     --image gcr.io/YOUR_PROJECT/sepsis-calculator \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8501
   ```

---

### 选项5：AWS App Runner / ECS

1. **构建Docker镜像:**
   ```bash
   docker build -t sepsis-calculator .
   ```

2. **推送到ECR:**
   ```bash
   aws ecr create-repository --repository-name sepsis-calculator
   docker tag sepsis-calculator:latest YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/sepsis-calculator:latest
   docker push YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/sepsis-calculator:latest
   ```

3. **使用App Runner或ECS Fargate部署**

---

## 📋 部署前检查清单

部署前确保：

- [ ] 所有模型文件都在仓库中：
  - `rf_model.pkl`
  - `shap_explainer.pkl`
  - `feature_info.pkl`

- [ ] `requirements.txt` 是最新的

- [ ] `Dockerfile` 是正确的

- [ ] 本地测试：
  ```bash
  docker build -t sepsis-calculator .
  docker run -p 8501:8501 sepsis-calculator
  ```

---

## 🔧 本地Docker测试

### 构建并本地运行：

```bash
# 构建镜像
docker build -t pressure-injuries-in-sepsis .

# 运行容器
docker run -d -p 8501:8501 --name sepsis-app pressure-injuries-in-sepsis

# 或使用docker-compose
docker-compose up -d
```

### 访问:
- 本地: http://localhost:8501

---

## 🌐 自定义域名设置

### Railway:
1. 前往 Settings → Domains
2. 添加自定义域名
3. 按照指示更新DNS记录

### Render:
1. 前往 Settings → Custom Domains
2. 添加你的域名
3. 更新DNS记录

### 推荐域名:
- `pressure-injuries-in-sepsis.com`
- `sepsis-calculator.com`
- `pressure-injuries-sepsis.app`

---

## 📝 环境变量

如果需要，可以在平台上设置这些：

```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

---

## 🆘 问题排查

### 端口问题:
- 确保Dockerfile中暴露了端口8501
- 检查平台端口配置

### 模型文件缺失:
- 确保`.pkl`文件在仓库中（不在.gitignore中）
- 或使用生产环境的卷挂载

### 构建失败:
- 检查Python版本兼容性
- 验证requirements.txt中的所有依赖

---

## 💰 费用估算

- **Railway:** 免费套餐 + 使用费用（约$5-20/月）
- **Render:** 有免费套餐，付费从$7/月起
- **Fly.io:** 有免费套餐，付费从约$5/月起
- **Google Cloud Run:** 按使用付费，非常便宜
- **AWS:** 按使用付费，费用不定

---

## 🔗 快速链接

- [Railway](https://railway.app)
- [Render](https://render.com)
- [Fly.io](https://fly.io)
- [Google Cloud Run](https://cloud.google.com/run)
- [AWS App Runner](https://aws.amazon.com/apprunner/)

---

## 📧 支持

如需部署帮助，请查看平台文档或联系支持。
