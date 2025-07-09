# Render 部署指南

## 🚀 快速部署到 Render

### 第一步：准备代码仓库

1. **确保代码已上传到GitHub**
   ```bash
   git add .
   git commit -m "准备Render部署"
   git push origin main
   ```

### 第二步：在Render上创建服务

1. **访问 Render Dashboard**
   - 打开 https://dashboard.render.com/
   - 使用GitHub账号登录

2. **创建新的Web Service**
   - 点击 "New +" → "Web Service"
   - 连接你的GitHub仓库
   - 选择包含聊天机器人代码的仓库

3. **配置服务设置**
   ```
   Name: stakeholder-chatbot
   Environment: Python
   Build Command: pip install -r requirements.txt
   Start Command: python chatbot_web.py
   ```

### 第三步：设置环境变量

在Render Dashboard中设置以下环境变量：

1. **OPENAI_API_KEY** (必需)
   - 类型：Secret
   - 值：你的OpenAI API密钥

2. **PORT** (可选)
   - 类型：Plain Text
   - 值：8081

### 第四步：部署配置

1. **自动部署**
   - Render会自动检测代码变更
   - 每次推送到main分支都会触发重新部署

2. **手动部署**
   - 在Dashboard中点击"Manual Deploy"
   - 选择"Deploy latest commit"

### 第五步：访问应用

部署完成后，Render会提供一个URL：
- 格式：`https://your-app-name.onrender.com`
- 可以直接访问聊天机器人界面

## 🔧 故障排除

### 常见问题

1. **构建失败**
   - 检查requirements.txt是否完整
   - 确认Python版本兼容性

2. **运行时错误**
   - 检查环境变量是否正确设置
   - 查看Render日志获取详细错误信息

3. **API调用失败**
   - 确认OPENAI_API_KEY有效
   - 检查网络连接和API配额

### 查看日志

在Render Dashboard中：
1. 点击你的服务
2. 进入"Logs"标签
3. 查看实时日志和错误信息

## 📊 监控和维护

1. **性能监控**
   - Render提供基本的性能指标
   - 监控响应时间和错误率

2. **自动重启**
   - Render会自动重启崩溃的应用
   - 设置健康检查确保服务稳定

3. **扩展性**
   - 免费计划适合开发和测试
   - 生产环境建议升级到付费计划

## 🔒 安全注意事项

1. **API密钥保护**
   - 使用Render的Secret环境变量
   - 不要在代码中硬编码密钥

2. **访问控制**
   - 考虑添加身份验证
   - 限制API调用频率

## 📞 支持

如果遇到问题：
1. 查看Render文档：https://render.com/docs
2. 检查项目日志
3. 确认所有依赖都已正确安装

---

**部署完成后，你的聊天机器人将在公网上可用！** 🎉 