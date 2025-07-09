#!/usr/bin/env bash
# Render构建脚本

echo "🚀 开始构建 Stakeholder Management Chatbot..."

# 安装Python依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 检查数据文件
echo "📁 检查数据文件..."
if [ -d "stakeholder_management_rag_sync" ]; then
    echo "✅ RAG数据文件夹存在"
    ls -la stakeholder_management_rag_sync/
else
    echo "❌ RAG数据文件夹不存在"
    exit 1
fi

# 检查环境变量
echo "🔧 检查环境变量..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY 未设置"
else
    echo "✅ OPENAI_API_KEY 已设置"
fi

echo "✅ 构建完成！" 