# 上传代码到GitHub - 详细步骤

## 你的GitHub仓库
https://github.com/Chen-barber/pressure-injuries-in-sepsis

---

## 步骤1：安装Git

### 方法A：使用winget（最简单）

1. 以管理员身份打开PowerShell
2. 运行：
   ```powershell
   winget install --id Git.Git -e --source winget
   ```
3. 等待安装完成
4. **关闭并重新打开PowerShell**

### 方法B：手动下载

1. 访问：https://git-scm.com/download/win
2. 下载并安装
3. 安装时确保勾选"添加到PATH"

### 验证安装

重新打开PowerShell，运行：
```powershell
git --version
```

如果显示版本号（如 `git version 2.xx.x`），说明安装成功！

---

## 步骤2：配置Git（首次使用）

```powershell
git config --global user.name "Chen-barber"
git config --global user.email "你的邮箱@example.com"
```

---

## 步骤3：上传代码到GitHub

在项目目录（F:\Data_Analysis\meeting）运行：

```powershell
# 1. 初始化Git仓库
git init

# 2. 安装Git LFS（用于大文件，.pkl文件很大）
git lfs install

# 3. 跟踪.pkl文件
git lfs track "*.pkl"

# 4. 添加所有文件
git add .

# 5. 提交
git commit -m "Initial commit - Pressure Injuries in Sepsis Calculator"

# 6. 连接到你的GitHub仓库
git remote add origin https://github.com/Chen-barber/pressure-injuries-in-sepsis.git

# 7. 设置主分支
git branch -M main

# 8. 推送到GitHub
git push -u origin main
```

**注意：** 第8步会要求输入GitHub用户名和密码（或Personal Access Token）

---

## 步骤4：如果遇到认证问题

GitHub不再支持密码登录，需要使用Personal Access Token：

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置：
   - Note: `Deploy Pressure Injuries in Sepsis`
   - Expiration: 选择期限（或No expiration）
   - 勾选权限：`repo`（全部）
4. 点击 "Generate token"
5. **复制token**（只显示一次！）
6. 推送时，密码处输入这个token

---

## 步骤5：验证上传

访问你的仓库：
https://github.com/Chen-barber/pressure-injuries-in-sepsis

应该能看到所有文件了！

---

## 常见问题

### 问题1：git lfs未安装

安装Git LFS：
```powershell
winget install --id Git.Git-LFS -e --source winget
```

或访问：https://git-lfs.github.com/

### 问题2：推送失败（文件太大）

确保使用了Git LFS：
```powershell
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git add .
git commit -m "Add LFS tracking"
git push
```

### 问题3：认证失败

使用Personal Access Token代替密码（见步骤4）

---

## 下一步：部署到Railway

代码上传成功后，就可以部署了！

1. 访问：https://railway.app
2. 用GitHub登录
3. New Project → Deploy from GitHub repo
4. 选择：Chen-barber/pressure-injuries-in-sepsis
5. 等待自动部署

