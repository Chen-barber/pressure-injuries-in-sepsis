@echo off
chcp 65001 >nul
echo ========================================
echo   Pressure Injuries in Sepsis 部署
echo ========================================
echo.

echo [步骤1] 检查Git安装...
git --version
if %errorlevel% neq 0 (
    echo Git未安装或未在PATH中
    echo 请关闭并重新打开PowerShell
    pause
    exit /b 1
)
echo ✓ Git已安装
echo.

echo [步骤2] 检查Git LFS...
git lfs version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git LFS未安装，正在安装...
    winget install --id Git.Git-LFS -e --source winget
    echo 请关闭并重新打开PowerShell后继续
    pause
    exit /b 1
)
echo ✓ Git LFS已安装
echo.

echo [步骤3] 配置Git（首次使用需要）...
echo 请输入你的GitHub用户名（直接回车使用: Chen-barber）
set /p GIT_USER="用户名: "
if "%GIT_USER%"=="" set GIT_USER=Chen-barber

echo 请输入你的GitHub邮箱:
set /p GIT_EMAIL="邮箱: "

if not "%GIT_EMAIL%"=="" (
    git config --global user.name "%GIT_USER%"
    git config --global user.email "%GIT_EMAIL%"
    echo ✓ Git已配置
) else (
    echo ⚠ 跳过配置（可以稍后手动配置）
)
echo.

echo [步骤4] 初始化Git仓库...
if exist .git (
    echo ✓ Git仓库已存在
) else (
    git init
    echo ✓ Git仓库已初始化
)
echo.

echo [步骤5] 配置Git LFS...
git lfs install
git lfs track "*.pkl"
echo ✓ Git LFS已配置
echo.

echo [步骤6] 添加文件...
git add .gitattributes
git add .
echo ✓ 文件已添加
echo.

echo [步骤7] 检查是否有未提交的更改...
git status --porcelain >nul
if %errorlevel% equ 0 (
    echo 发现未提交的更改
    echo.
    echo 是否现在提交? (Y/N)
    set /p COMMIT="请输入: "
    if /i "%COMMIT%"=="Y" (
        git commit -m "Initial commit - Pressure Injuries in Sepsis Calculator"
        echo ✓ 已提交
    ) else (
        echo ⚠ 已跳过提交
    )
) else (
    echo ✓ 没有需要提交的更改
)
echo.

echo [步骤8] 连接到GitHub仓库...
git remote -v >nul 2>&1
if %errorlevel% neq 0 (
    git remote add origin https://github.com/Chen-barber/pressure-injuries-in-sepsis.git
    echo ✓ 已连接到GitHub仓库
) else (
    echo ✓ GitHub仓库已连接
)
echo.

echo ========================================
echo   准备完成！
echo ========================================
echo.
echo 下一步操作：
echo.
echo 1. 创建Personal Access Token:
echo    https://github.com/settings/tokens
echo.
echo 2. 推送到GitHub:
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. 部署到Railway:
echo    https://railway.app
echo.
echo ========================================
pause

