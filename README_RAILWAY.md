# Stakeholder Management Chatbot - Railway部署版

## 项目概述
这是一个基于LightRAG框架开发的利益相关者管理聊天机器人，专门为Railway平台优化部署。

## 部署平台
- **平台**: Railway
- **优势**: 更好的Python支持、稳定的环境变量管理
- **域名**: `https://your-project-name.railway.app`

## 快速部署

### 1. 创建GitHub仓库
```bash
git init
git add .
git commit -m "Initial commit: Railway deployment"
git remote add origin https://github.com/你的用户名/chatbot-railway.git
git push -u origin main
```

### 2. Railway部署
1. 访问 [https://railway.app](https://railway.app)
2. 使用GitHub登录
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择你的仓库

### 3. 设置环境变量
在Railway控制台：
- `OPENAI_API_KEY` = 你的OpenAI API密钥
- `PORT` = 8081

## 文件结构
```
chatbot_railway_deploy/
├── chatbot_web.py              # 主应用文件
├── requirements.txt            # Python依赖
├── Procfile                   # Railway启动命令
├── railway.json               # Railway配置
├── templates/
│   └── index.html             # 前端界面
├── stakeholder_management_rag_sync/  # RAG数据
└── README_RAILWAY.md          # 本文件
```

## 功能特性
- ✅ 智能问答系统
- ✅ 多模式查询
- ✅ 实时评分
- ✅ 成本统计
- ✅ 现代化Web界面

## 技术栈
- **后端**: Flask + LightRAG
- **前端**: HTML5 + CSS3 + JavaScript
- **AI**: OpenAI GPT-4 + Embeddings
- **部署**: Railway

## 优势对比
| 特性 | Vercel | Railway |
|------|--------|---------|
| Python支持 | ⚠️ 有限 | ✅ 完整 |
| 环境变量 | ✅ 好 | ✅ 很好 |
| 部署速度 | ✅ 快 | ✅ 快 |
| 稳定性 | ⚠️ 一般 | ✅ 很好 |

## 维护
- 代码更新会自动触发重新部署
- 在Railway控制台查看日志和监控
- 支持自定义域名

---
*这是一个专门为Railway平台优化的聊天机器人部署版本。* 