#!/usr/bin/env python3
"""
Render部署前检查脚本
检查所有必要的文件和配置是否正确
"""

import os
import sys
import json
from pathlib import Path

def check_files():
    """检查必要文件是否存在"""
    print("🔍 检查必要文件...")
    
    required_files = [
        "chatbot_web.py",
        "requirements.txt", 
        "render.yaml",
        "build.sh",
        "templates/index.html"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    else:
        print("✅ 所有必要文件都存在")
        return True

def check_data_directory():
    """检查RAG数据目录"""
    print("\n📁 检查RAG数据目录...")
    
    data_dir = "stakeholder_management_rag_sync"
    if not os.path.exists(data_dir):
        print(f"❌ 数据目录 {data_dir} 不存在")
        return False
    
    required_data_files = [
        "graph_chunk_entity_relation.graphml",
        "kv_store_doc_status.json",
        "kv_store_full_docs.json",
        "kv_store_llm_response_cache.json",
        "kv_store_text_chunks.json",
        "vdb_chunks.json",
        "vdb_entities.json",
        "vdb_relationships.json"
    ]
    
    missing_data = []
    for file in required_data_files:
        file_path = os.path.join(data_dir, file)
        if not os.path.exists(file_path):
            missing_data.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_data:
        print(f"❌ 缺少数据文件: {missing_data}")
        return False
    else:
        print("✅ 所有数据文件都存在")
        return True

def check_requirements():
    """检查requirements.txt"""
    print("\n📦 检查requirements.txt...")
    
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read().strip().split("\n")
        
        if not requirements:
            print("❌ requirements.txt为空")
            return False
        
        print(f"✅ 找到 {len(requirements)} 个依赖项")
        for req in requirements:
            if req.strip():
                print(f"  - {req.strip()}")
        
        return True
    except Exception as e:
        print(f"❌ 读取requirements.txt失败: {e}")
        return False

def check_render_config():
    """检查render.yaml配置"""
    print("\n⚙️ 检查render.yaml配置...")
    
    try:
        with open("render.yaml", "r") as f:
            config = f.read()
        
        if "stakeholder-chatbot" in config and "python" in config:
            print("✅ render.yaml配置正确")
            return True
        else:
            print("❌ render.yaml配置不正确")
            return False
    except Exception as e:
        print(f"❌ 读取render.yaml失败: {e}")
        return False

def check_environment():
    """检查环境变量"""
    print("\n🔧 检查环境变量...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OPENAI_API_KEY已设置")
        return True
    else:
        print("⚠️  OPENAI_API_KEY未设置（部署时需要在Render中设置）")
        return True  # 这不是错误，因为部署时会在Render中设置

def main():
    """主检查函数"""
    print("🚀 Render部署前检查")
    print("=" * 50)
    
    checks = [
        check_files(),
        check_data_directory(),
        check_requirements(),
        check_render_config(),
        check_environment()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("✅ 所有检查通过！可以开始Render部署")
        print("\n📋 下一步：")
        print("1. 确保代码已上传到GitHub")
        print("2. 访问 https://dashboard.render.com/")
        print("3. 创建新的Web Service")
        print("4. 连接GitHub仓库")
        print("5. 设置环境变量OPENAI_API_KEY")
        print("6. 部署应用")
    else:
        print("❌ 部分检查失败，请修复问题后重试")
        sys.exit(1)

if __name__ == "__main__":
    main() 