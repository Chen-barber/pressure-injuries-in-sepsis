# PowerShell 一键部署脚本
# 用于检查文件并准备Git提交

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Pressure Injuries in Sepsis 部署准备" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查必需文件
Write-Host "[1/4] 检查必需文件..." -ForegroundColor Yellow

$requiredFiles = @(
    "Dockerfile",
    "app.py",
    "requirements.txt",
    "rf_model.pkl",
    "shap_explainer.pkl",
    "feature_info.pkl"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length / 1MB
        Write-Host "  ✓ $file ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (缺失)" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "警告: 以下文件缺失:" -ForegroundColor Red
    foreach ($file in $missingFiles) {
        Write-Host "  - $file" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "请先运行: python train_model.py" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[2/4] 检查Git状态..." -ForegroundColor Yellow

# 检查是否已初始化Git
if (-not (Test-Path ".git")) {
    Write-Host "  初始化Git仓库..." -ForegroundColor Yellow
    git init
    Write-Host "  ✓ Git仓库已初始化" -ForegroundColor Green
} else {
    Write-Host "  ✓ Git仓库已存在" -ForegroundColor Green
}

Write-Host ""
Write-Host "[3/4] 检查Git LFS（用于大文件）..." -ForegroundColor Yellow

# 检查Git LFS
$lfsInstalled = git lfs version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Git LFS已安装" -ForegroundColor Green
    
    # 检查是否已跟踪.pkl文件
    if (-not (Test-Path ".gitattributes")) {
        Write-Host "  配置Git LFS跟踪.pkl文件..." -ForegroundColor Yellow
        git lfs install
        git lfs track "*.pkl"
        git add .gitattributes
        Write-Host "  ✓ Git LFS已配置" -ForegroundColor Green
    } else {
        Write-Host "  ✓ Git LFS已配置" -ForegroundColor Green
    }
} else {
    Write-Host "  ⚠ Git LFS未安装（可选，用于大文件）" -ForegroundColor Yellow
    Write-Host "    安装方法: winget install Git.Git-LFS" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/4] 准备提交..." -ForegroundColor Yellow

# 添加所有文件
git add .
Write-Host "  ✓ 文件已添加到暂存区" -ForegroundColor Green

# 检查是否有更改
$status = git status --porcelain
if ($status) {
    Write-Host ""
    Write-Host "准备提交以下文件:" -ForegroundColor Cyan
    git status --short
    
    Write-Host ""
    $commit = Read-Host "是否现在提交? (y/n)"
    if ($commit -eq "y" -or $commit -eq "Y") {
        $message = Read-Host "输入提交信息 (直接回车使用默认)"
        if ([string]::IsNullOrWhiteSpace($message)) {
            $message = "Deploy Pressure Injuries in Sepsis Calculator"
        }
        git commit -m $message
        Write-Host "  ✓ 已提交" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "  下一步操作:" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. 如果还没有GitHub仓库，请先创建:" -ForegroundColor Yellow
        Write-Host "   - 访问 https://github.com" -ForegroundColor White
        Write-Host "   - 创建新仓库" -ForegroundColor White
        Write-Host ""
        Write-Host "2. 连接到GitHub仓库:" -ForegroundColor Yellow
        Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor White
        Write-Host ""
        Write-Host "3. 推送到GitHub:" -ForegroundColor Yellow
        Write-Host "   git branch -M main" -ForegroundColor White
        Write-Host "   git push -u origin main" -ForegroundColor White
        Write-Host ""
        Write-Host "4. 在Railway或Render上部署" -ForegroundColor Yellow
        Write-Host "   详细步骤请查看: 详细部署教程.md" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "  已取消提交" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✓ 没有需要提交的更改" -ForegroundColor Green
}

Write-Host ""
Write-Host "完成！" -ForegroundColor Green

