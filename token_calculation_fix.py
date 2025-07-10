#!/usr/bin/env python3
"""
更准确的Token计算示例
"""

import tiktoken
import os

def initialize_token_encoder():
    """初始化token编码器"""
    return tiktoken.encoding_for_model("gpt-4o-mini")

def calculate_complete_tokens(system_prompt, user_prompt, response_text):
    """计算完整的token数量（包括系统提示词）"""
    token_encoder = initialize_token_encoder()
    
    # 计算输入tokens（系统提示词 + 用户问题）
    input_tokens = len(token_encoder.encode(system_prompt)) + len(token_encoder.encode(user_prompt))
    
    # 计算输出tokens
    output_tokens = len(token_encoder.encode(response_text))
    
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens
    }

def calculate_accurate_cost(input_tokens, output_tokens, embedding_tokens=0):
    """使用最新价格计算成本"""
    # 2024年最新价格（建议定期更新）
    COST_CONFIG = {
        "gpt-4o-mini": {
            "input_cost_per_1k_tokens": 0.00015,  # $0.00015 per 1K input tokens
            "output_cost_per_1k_tokens": 0.0006,  # $0.0006 per 1K output tokens
        },
        "text-embedding-3-small": {
            "cost_per_1k_tokens": 0.00002,  # $0.00002 per 1K tokens (新价格)
        }
    }
    
    # 计算LLM成本
    llm_input_cost = (input_tokens / 1000) * COST_CONFIG["gpt-4o-mini"]["input_cost_per_1k_tokens"]
    llm_output_cost = (output_tokens / 1000) * COST_CONFIG["gpt-4o-mini"]["output_cost_per_1k_tokens"]
    
    # 计算embedding成本
    embedding_cost = (embedding_tokens / 1000) * COST_CONFIG["text-embedding-3-small"]["cost_per_1k_tokens"]
    
    total_cost = llm_input_cost + llm_output_cost + embedding_cost
    
    return {
        "llm_input_cost": llm_input_cost,
        "llm_output_cost": llm_output_cost,
        "embedding_cost": embedding_cost,
        "total_cost": total_cost,
        "breakdown": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "embedding_tokens": embedding_tokens
        }
    }

# 测试示例
if __name__ == "__main__":
    system_prompt = "你是一个专业的利益相关者管理顾问。基于提供的文档信息，请诚实、准确地回答用户问题。"
    user_prompt = "请介绍一下这个项目的主要利益相关者。"
    response = "根据文档分析，这个项目的主要利益相关者包括..."
    
    tokens = calculate_complete_tokens(system_prompt, user_prompt, response)
    cost = calculate_accurate_cost(tokens["input_tokens"], tokens["output_tokens"])
    
    print("Token计算示例：")
    print(f"输入tokens: {tokens['input_tokens']}")
    print(f"输出tokens: {tokens['output_tokens']}")
    print(f"总tokens: {tokens['total_tokens']}")
    print(f"总成本: ${cost['total_cost']:.6f}") 