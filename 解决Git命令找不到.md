# 解决Git命令找不到的问题

## 问题
Git已安装，但PowerShell无法识别`git`命令。

## 解决方法

### 方法1：关闭并重新打开PowerShell（最简单）

1. **完全关闭当前的PowerShell窗口**
2. **重新打开一个新的PowerShell窗口**
3. 运行：`git --version`

这应该就能工作了！

---

### 方法2：刷新环境变量（不关闭窗口）

在当前PowerShell中运行：

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
git --version
```

---

### 方法3：手动添加到PATH（如果前两种方法都不行）

1. 检查Git安装路径：
   ```powershell
   Test-Path "C:\Program Files\Git\bin\git.exe"
   ```

2. 如果返回True，手动添加到PATH：
   - 按 `Win + R`
   - 输入：`sysdm.cpl` 回车
   - 点击"高级"标签
   - 点击"环境变量"
   - 在"系统变量"中找到"Path"
   - 点击"编辑"
   - 点击"新建"
   - 添加：`C:\Program Files\Git\bin`
   - 确定保存
   - **重新打开PowerShell**

---

## 验证安装

重新打开PowerShell后，运行：

```powershell
git --version
```

应该显示：`git version 2.51.2` 或类似版本号

---

## 下一步：安装Git LFS

Git安装成功后，安装Git LFS：

```powershell
winget install --id Git.Git-LFS -e --source winget
```

安装后同样需要**重新打开PowerShell**才能使用。

---

## 然后就可以上传代码了！

Git和Git LFS都安装好后，就可以按照`完整部署步骤.md`中的说明上传代码了。

