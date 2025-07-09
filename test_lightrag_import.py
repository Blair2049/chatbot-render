#!/usr/bin/env python3
"""
测试LightRAG模块导入
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_lightrag_import():
    """测试LightRAG模块导入"""
    try:
        print("🔍 测试LightRAG模块导入...")
        
        # 测试基本导入
        from lightrag import QueryParam, LightRAG
        print("✅ QueryParam 和 LightRAG 导入成功")
        
        # 测试LLM模块导入
        from lightrag.llm import openai_complete_if_cache, openai_embedding
        print("✅ LLM模块导入成功")
        
        # 测试utils模块导入
        from lightrag.utils import EmbeddingFunc
        print("✅ Utils模块导入成功")
        
        # 测试其他必要模块
        from lightrag.base import DocStatus
        print("✅ Base模块导入成功")
        
        print("✅ 所有LightRAG模块导入成功！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    success = test_lightrag_import()
    sys.exit(0 if success else 1) 