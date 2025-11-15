# Git安装后操作指南

## ✅ Git已成功安装！

但是PowerShell需要重新加载环境变量才能识别git命令。

---

## 解决方法

### 方法1：关闭并重新打开PowerShell（推荐）

1. **完全关闭当前的PowerShell窗口**
2. **重新打开一个新的PowerShell窗口**
3. 运行 `git --version` 验证

这是最简单可靠的方法！

---

### 方法2：刷新环境变量（当前窗口）

在当前PowerShell窗口运行：

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

然后运行：
```powershell
git --version
```

---

## 验证安装

运行以下命令验证：

```powershell
git --version
```

应该显示：`git version 2.51.2.windows.1` 或类似版本号

---

## 下一步：安装Git LFS

Git安装成功后，安装Git LFS（用于大文件）：

```powershell
winget install --id Git.Git-LFS -e --source winget
```

安装后同样需要**关闭并重新打开PowerShell**。

---

## 然后配置Git

```powershell
git config --global user.name "Chen-barber"
git config --global user.email "你的GitHub邮箱"
```

---

## 最后上传代码

```powershell
cd F:\Data_Analysis\meeting
git init
git lfs install
git lfs track "*.pkl"
git add .
git commit -m "Initial commit - Pressure Injuries in Sepsis Calculator"
git remote add origin https://github.com/Chen-barber/pressure-injuries-in-sepsis.git
git branch -M main
git push -u origin main
```

---

## 重要提示

每次安装新软件后，如果命令无法识别：
1. **关闭并重新打开PowerShell**
2. 或使用上面的刷新命令

这是Windows环境变量的特性，需要重新加载才能生效。

