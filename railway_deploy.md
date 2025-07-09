# Railway部署指南

## 平台优势
- ✅ 更稳定的Python支持
- ✅ 更好的环境变量管理
- ✅ 免费额度充足
- ✅ 部署简单快速

## 部署步骤

### 1. 注册Railway账户
1. 访问 [https://railway.app](https://railway.app)
2. 使用GitHub账户登录

### 2. 创建新项目
1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择你的GitHub仓库

### 3. 配置环境变量
在Railway控制台：
1. 进入项目设置
2. 点击 "Variables" 标签
3. 添加环境变量：
   ```
   OPENAI_API_KEY = your_openai_api_key
   PORT = 8081
   ```

### 4. 部署配置
Railway会自动检测：
- `Procfile` - 启动命令
- `requirements.txt` - Python依赖
- `railway.json` - 部署配置

### 5. 获取域名
部署成功后，Railway会提供一个域名：
- 格式：`https://your-project-name.railway.app`
- 可以直接分享给其他人使用

## 文件说明

### 核心文件
- `chatbot_web.py` - 主应用文件
- `requirements.txt` - Python依赖
- `Procfile` - 启动命令
- `railway.json` - Railway配置

### 数据文件
- `stakeholder_management_rag_sync/` - RAG数据
- `templates/index.html` - 前端界面

## 优势对比

| 特性 | Vercel | Railway |
|------|--------|---------|
| Python支持 | ⚠️ 有限 | ✅ 完整 |
| 环境变量 | ✅ 好 | ✅ 很好 |
| 部署速度 | ✅ 快 | ✅ 快 |
| 稳定性 | ⚠️ 一般 | ✅ 很好 |
| 免费额度 | ✅ 充足 | ✅ 充足 |

## 故障排除

### 常见问题
1. **环境变量未设置** - 检查Railway控制台
2. **依赖安装失败** - 检查requirements.txt
3. **端口冲突** - 确保PORT=8081

### 查看日志
1. 在Railway控制台点击项目
2. 查看 "Deployments" 标签
3. 点击最新部署查看日志

## 更新部署
每次推送到GitHub main分支，Railway会自动重新部署。 