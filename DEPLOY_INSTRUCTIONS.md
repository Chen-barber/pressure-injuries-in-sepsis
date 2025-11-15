# 🚀 部署指南 - Pressure Injuries in Sepsis

## 最简单的方法：Railway（推荐）

### 步骤1：准备代码
确保所有文件已提交到Git：
```bash
git add .
git commit -m "Ready for deployment"
git push
```

### 步骤2：部署到Railway

1. **访问 [railway.app](https://railway.app)**
2. **使用GitHub账号登录**
3. **创建新项目：**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库

4. **Railway会自动：**
   - 检测到Dockerfile
   - 构建Docker镜像
   - 部署应用

5. **获取链接：**
   - 部署完成后，Railway会提供一个URL
   - 格式：`https://your-app-name.up.railway.app`
   - 可以在Settings → Domains中自定义域名

### 步骤3：分享链接
将链接分享给其他人即可访问！

---

## 其他部署选项

### Render.com
1. 访问 [render.com](https://render.com)
2. 使用GitHub登录
3. New → Web Service
4. 连接仓库
5. 配置：
   - Name: `pressure-injuries-in-sepsis`
   - Environment: Docker
   - Port: 8501
6. 部署

### Fly.io
```bash
# 安装Fly CLI
curl -L https://fly.io/install.sh | sh

# 登录
fly auth login

# 部署
fly launch --name pressure-injuries-in-sepsis
fly deploy
```

---

## 本地测试（部署前）

```bash
# 构建Docker镜像
docker build -t pressure-injuries-in-sepsis .

# 运行容器
docker run -p 8501:8501 pressure-injuries-in-sepsis

# 访问 http://localhost:8501
```

---

## 必需文件检查清单

确保以下文件在仓库中：
- ✅ `Dockerfile`
- ✅ `app.py`
- ✅ `rf_model.pkl`
- ✅ `shap_explainer.pkl`
- ✅ `feature_info.pkl`
- ✅ `requirements.txt`

---

## 自定义域名

部署后可以添加自定义域名：
- **Railway:** Settings → Domains
- **Render:** Settings → Custom Domains

建议域名：`pressure-injuries-in-sepsis.com`

---

## 费用

- **Railway:** 免费额度 $5/月
- **Render:** 有免费套餐
- **Fly.io:** 有免费套餐

---

## 问题排查

**构建失败？**
- 检查所有.pkl文件是否在仓库中
- 确认requirements.txt完整

**应用无法启动？**
- 查看平台日志
- 确认端口8501已暴露

---

## 快速链接

- [Railway部署](https://railway.app)
- [Render部署](https://render.com)
- [Fly.io部署](https://fly.io)

