# Git安装指南

## 方法一：使用winget安装（推荐）

在PowerShell中运行（管理员权限）：

```powershell
winget install --id Git.Git -e --source winget
```

## 方法二：手动下载安装

1. 访问：https://git-scm.com/download/win
2. 下载Git for Windows
3. 运行安装程序
4. 安装时选择：
   - ✅ 添加到PATH环境变量
   - ✅ 使用Git Bash和Git GUI
   - ✅ 默认编辑器选择你喜欢的

## 安装后验证

关闭并重新打开PowerShell，然后运行：

```powershell
git --version
```

如果显示版本号，说明安装成功！

## 配置Git（首次使用）

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

