#!/usr/bin/env python3
"""
改进的Token计算：使用OpenAI API返回的usage信息
"""

import asyncio
from openai import AsyncOpenAI
import os

async def openai_complete_with_usage(
    prompt,
    system_prompt=None,
    history_messages=[],
    model="gpt-4o-mini",
    api_key=None,
    **kwargs
):
    """使用OpenAI API并返回usage信息"""
    
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    client = AsyncOpenAI(api_key=api_key)
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})
    
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        **kwargs
    )
    
    # 获取usage信息
    usage = response.usage
    content = response.choices[0].message.content
    
    return {
        "content": content,
        "usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens
        }
    }

def calculate_cost_from_usage(usage_info):
    """根据usage信息计算成本"""
    COST_CONFIG = {
        "gpt-4o-mini": {
            "input_cost_per_1k_tokens": 0.00015,  # $0.00015 per 1K input tokens
            "output_cost_per_1k_tokens": 0.0006,  # $0.0006 per 1K output tokens
        }
    }
    
    prompt_tokens = usage_info["prompt_tokens"]
    completion_tokens = usage_info["completion_tokens"]
    
    # 计算成本
    input_cost = (prompt_tokens / 1000) * COST_CONFIG["gpt-4o-mini"]["input_cost_per_1k_tokens"]
    output_cost = (completion_tokens / 1000) * COST_CONFIG["gpt-4o-mini"]["output_cost_per_1k_tokens"]
    total_cost = input_cost + output_cost
    
    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "usage": usage_info
    }

# 测试示例
async def test_usage_calculation():
    """测试使用API usage信息的计算"""
    
    system_prompt = "你是一个专业的利益相关者管理顾问。"
    user_prompt = "请介绍一下这个项目的主要利益相关者。"
    
    try:
        result = await openai_complete_with_usage(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=200
        )
        
        cost = calculate_cost_from_usage(result["usage"])
        
        print("=== 使用API usage信息的Token计算 ===")
        print(f"回答内容: {result['content'][:100]}...")
        print(f"输入tokens: {result['usage']['prompt_tokens']}")
        print(f"输出tokens: {result['usage']['completion_tokens']}")
        print(f"总tokens: {result['usage']['total_tokens']}")
        print(f"输入成本: ${cost['input_cost']:.6f}")
        print(f"输出成本: ${cost['output_cost']:.6f}")
        print(f"总成本: ${cost['total_cost']:.6f}")
        
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_usage_calculation()) 