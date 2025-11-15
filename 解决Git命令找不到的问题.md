# 解决Git命令找不到的问题

## 问题原因
Git已安装，但PowerShell还没有加载新的环境变量。

## 解决方法

### 方法1：关闭并重新打开PowerShell（推荐）

1. **完全关闭当前的PowerShell窗口**
2. **重新打开一个新的PowerShell窗口**
3. **运行验证：**
   ```powershell
   git --version
   ```

### 方法2：刷新环境变量（当前窗口）

在当前PowerShell窗口运行：

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
git --version
```

### 方法3：手动添加到PATH（如果还不行）

1. 找到Git安装路径（通常在）：
   - `C:\Program Files\Git\cmd`
   - 或 `C:\Program Files (x86)\Git\cmd`

2. 添加到系统PATH：
   - 右键"此电脑" → 属性
   - 高级系统设置 → 环境变量
   - 系统变量 → Path → 编辑
   - 新建 → 添加Git路径
   - 确定保存

3. 重新打开PowerShell

---

## 验证安装

运行以下命令验证：

```powershell
git --version
git lfs version
```

如果都显示版本号，说明安装成功！

---

## 下一步

Git安装成功后，继续：
1. 配置Git用户信息
2. 上传代码到GitHub
3. 部署到Railway

详细步骤请查看：`完整部署步骤.md`

