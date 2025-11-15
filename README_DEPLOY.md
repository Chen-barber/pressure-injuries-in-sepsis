# 🚀 部署指南 - Pressure Injuries in Sepsis 计算器

## 快速开始（Railway - 推荐）

### 步骤1：准备代码仓库
1. 确保所有文件已提交到Git：
   ```bash
   git add .
   git commit -m "准备部署"
   git push
   ```

### 步骤2：在Railway上部署
1. 访问 [railway.app](https://railway.app)
2. 使用GitHub账号登录/注册
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. Railway会自动：
   - 检测到Dockerfile
   - 构建镜像
   - 部署应用

### 步骤3：获取链接
- Railway会提供一个URL，格式：`https://your-app-name.up.railway.app`
- 可以在 Settings → Domains 中自定义域名

### 步骤4：分享
将链接分享给其他人：`https://pressure-injuries-in-sepsis.up.railway.app`

---

## 其他选项：Render.com

1. 访问 [render.com](https://render.com)
2. 使用GitHub登录
3. New → Web Service
4. 连接你的仓库
5. 配置：
   - **名称:** `pressure-injuries-in-sepsis`
   - **环境:** Docker
   - **端口:** 8501
6. 部署

---

## 部署前本地测试

```bash
# 构建Docker镜像
docker build -t sepsis-calculator .

# 本地运行
docker run -p 8501:8501 sepsis-calculator

# 测试地址 http://localhost:8501
```

---

## 部署必需文件

✅ **必需文件:**
- `Dockerfile` - 容器配置
- `app.py` - 主应用程序
- `rf_model.pkl` - 训练好的模型
- `shap_explainer.pkl` - SHAP解释器
- `feature_info.pkl` - 特征信息
- `requirements.txt` - Python依赖包

✅ **可选但有用的文件:**
- `docker-compose.yml` - 用于本地测试
- `railway.json` - Railway配置
- `render.yaml` - Render配置
- `fly.toml` - Fly.io配置

---

## 自定义域名设置

部署后可以添加自定义域名：

**Railway:**
- Settings → Domains → Add Domain
- 按照指示更新DNS记录

**Render:**
- Settings → Custom Domains
- 添加你的域名

**建议域名:** `pressure-injuries-in-sepsis.com`

---

## 问题排查

**构建失败:**
- 检查所有`.pkl`文件是否在仓库中
- 确认`requirements.txt`完整

**应用无法启动:**
- 查看平台日志
- 确认端口8501已暴露

**模型文件缺失:**
- 确保`.pkl`文件已提交（不在.gitignore中）

---

## 费用

大多数平台提供免费套餐：
- **Railway:** 每月$5免费额度
- **Render:** 有免费套餐
- **Fly.io:** 有免费套餐

---

## 支持

如需部署帮助，请查看：
- 平台文档
- `deploy_guide.md` 获取详细说明
