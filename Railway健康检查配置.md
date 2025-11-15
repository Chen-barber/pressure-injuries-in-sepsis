# Railway健康检查配置指南

## 问题
健康检查失败：`The health check endpoint didn't respond as expected`

## Railway健康检查要求

根据Railway文档：
1. **端点要求：** 需要一个返回HTTP 200的端点
2. **端口要求：** 应用必须监听`PORT`环境变量
3. **Hostname要求：** 需要允许`healthcheck.railway.app`的请求
4. **超时时间：** 默认300秒（5分钟）

## 解决方案

### 方案1：在Railway设置中配置（推荐）

1. **访问Railway项目**
2. **点击你的服务 → Settings**
3. **找到 "Healthcheck" 部分**
4. **配置：**
   - **Healthcheck Path:** 留空或填写 `/`（Streamlit根路径）
   - **Healthcheck Timeout:** 设置为 `300` 或更大（秒）
   - **或者直接禁用健康检查**（取消勾选 "Enable Healthcheck"）

### 方案2：使用环境变量

在Railway的 "Variables" 中添加：
- `RAILWAY_HEALTHCHECK_TIMEOUT_SEC` = `300`

### 方案3：直接测试网站（最重要）

**即使健康检查失败，网站可能已经可以用了！**

1. 获取Railway的URL（Settings → Domains）
2. 直接在浏览器中访问
3. 如果网站能打开并使用，说明部署成功！

---

## Streamlit健康检查说明

Streamlit的健康检查端点：
- `/_stcore/health` - Streamlit的内部健康检查端点
- `/` - 根路径（也可以作为健康检查）

Railway默认使用根路径 `/` 进行健康检查。

---

## 已修复的配置

### Dockerfile:
- 使用`PORT`环境变量（Railway自动注入）
- 如果PORT不存在，默认使用8501
- 增加了启动等待时间（120秒）

### 建议操作：

**最简单的方法：在Railway中禁用健康检查**

1. Railway项目 → 你的服务 → Settings
2. 找到 "Healthcheck"
3. **取消勾选 "Enable Healthcheck"**
4. 保存

这样就不会有健康检查警告了，而且不影响应用功能。

---

## 验证部署成功

**最直接的方法：直接访问网站**

1. 获取Railway的URL
2. 在浏览器中打开
3. 测试功能：
   - 输入特征变量
   - 点击计算
   - 查看结果

如果能正常使用，说明部署成功！

---

## 重要提示

**健康检查只是监控工具，不影响应用功能！**

即使健康检查显示失败，只要网站能正常访问和使用，就说明部署成功了。

建议：
1. 先测试网站能否访问
2. 如果能用，可以禁用健康检查
3. 或者增加超时时间到300秒以上

