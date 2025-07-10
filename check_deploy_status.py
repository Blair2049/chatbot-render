#!/usr/bin/env python3
"""
部署状态检查脚本
检查所有必要的文件和配置是否正确
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - 文件不存在")
        return False

def check_environment_variables():
    """检查环境变量"""
    print("\n🔧 检查环境变量...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OPENAI_API_KEY: {'*' * 10}{api_key[-4:]}")
    else:
        print("❌ OPENAI_API_KEY: 未设置")
        return False
    
    return True

def check_python_dependencies():
    """检查Python依赖"""
    print("\n📦 检查Python依赖...")
    
    required_packages = [
        'flask', 'numpy', 'tiktoken', 'openai', 'networkx',
        'scikit-learn', 'pandas', 'requests', 'python-dotenv',
        'asyncio', 'nest-asyncio', 'setuptools', 'aioboto3',
        'aiohttp', 'ollama', 'torch', 'pydantic', 'tenacity',
        'transformers', 'nano-vectordb'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  缺少依赖包: {', '.join(missing_packages)}")
        return False
    
    return True

def check_data_files():
    """检查数据文件"""
    print("\n📁 检查数据文件...")
    
    rag_dir = "stakeholder_management_rag_sync"
    if os.path.exists(rag_dir):
        print(f"✅ RAG数据目录: {rag_dir}")
        
        # 检查关键文件
        key_files = [
            "graph_chunk_entity_relation.graphml",
            "kv_store_full_docs.json",
            "kv_store_text_chunks.json",
            "vdb_chunks.json"
        ]
        
        for file in key_files:
            file_path = os.path.join(rag_dir, file)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"  ✅ {file} ({size:,} bytes)")
            else:
                print(f"  ❌ {file} - 文件不存在")
                return False
    else:
        print(f"❌ RAG数据目录不存在: {rag_dir}")
        return False
    
    return True

def check_lightrag_module():
    """检查LightRAG模块"""
    print("\n🔍 检查LightRAG模块...")
    
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from lightrag import LightRAG, QueryParam
        from lightrag.llm import openai_complete_if_cache, openai_embedding
        from lightrag.utils import EmbeddingFunc
        print("✅ LightRAG模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ LightRAG模块导入失败: {e}")
        return False

def check_token_tracker():
    """检查Token跟踪器"""
    print("\n📊 检查Token跟踪器...")
    
    try:
        from token_usage_tracker import TokenUsageTracker
        tracker = TokenUsageTracker()
        print("✅ Token跟踪器初始化成功")
        return True
    except Exception as e:
        print(f"❌ Token跟踪器初始化失败: {e}")
        return False

def main():
    """主检查函数"""
    print("🚀 开始部署状态检查...\n")
    
    checks = [
        ("环境变量", check_environment_variables),
        ("Python依赖", check_python_dependencies),
        ("数据文件", check_data_files),
        ("LightRAG模块", check_lightrag_module),
        ("Token跟踪器", check_token_tracker)
    ]
    
    all_passed = True
    for name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {name}检查失败: {e}")
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 所有检查通过！部署准备就绪")
        print("\n📋 部署步骤:")
        print("1. 确保OPENAI_API_KEY已在Render中设置")
        print("2. 推送代码到GitHub")
        print("3. Render将自动构建和部署")
        print("4. 访问部署URL测试功能")
    else:
        print("⚠️  部分检查失败，请修复问题后重新部署")
    
    return all_passed

if __name__ == "__main__":
    main() 