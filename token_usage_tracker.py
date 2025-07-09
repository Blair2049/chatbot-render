import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class TokenUsageTracker:
    """
    Token使用情况跟踪器
    用于记录和管理OpenAI API的token使用情况
    """
    
    def __init__(self, storage_file: str = "token_usage.json"):
        self.storage_file = storage_file
        # 在Render环境中，使用内存存储而不是文件存储
        self.use_memory_storage = os.getenv('RENDER', False)  # 检测是否在Render环境
        self.usage_data = self._load_usage_data()
    
    def _load_usage_data(self) -> Dict:
        """加载现有的使用数据"""
        # 在Render环境中使用内存存储
        if self.use_memory_storage:
            return self._get_default_structure()
        
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"无法加载token使用数据: {e}")
                return self._get_default_structure()
        return self._get_default_structure()
    
    def _get_default_structure(self) -> Dict:
        """获取默认的数据结构"""
        return {
            "total_usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "estimated_cost": 0.0
            },
            "daily_usage": {},
            "model_usage": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_usage_data(self):
        """保存使用数据到文件"""
        # 在Render环境中只更新内存数据，不写入文件
        if self.use_memory_storage:
            self.usage_data["last_updated"] = datetime.now().isoformat()
            return
        
        try:
            self.usage_data["last_updated"] = datetime.now().isoformat()
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.usage_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            logger.error(f"无法保存token使用数据: {e}")
    
    def record_usage(self, usage_info: Dict):
        """
        记录一次token使用情况
        
        Args:
            usage_info: 包含token使用信息的字典
                {
                    "prompt_tokens": int,
                    "completion_tokens": int,
                    "total_tokens": int,
                    "model": str,
                    "timestamp": str
                }
        """
        if not usage_info:
            return
        
        # 更新总使用量
        total_usage = self.usage_data["total_usage"]
        total_usage["prompt_tokens"] += usage_info.get("prompt_tokens", 0)
        total_usage["completion_tokens"] += usage_info.get("completion_tokens", 0)
        total_usage["total_tokens"] += usage_info.get("total_tokens", 0)
        
        # 计算并更新估算成本
        model = usage_info.get("model", "gpt-4o-mini")
        estimated_cost = self._calculate_cost(
            usage_info.get("prompt_tokens", 0),
            usage_info.get("completion_tokens", 0),
            model
        )
        total_usage["estimated_cost"] += estimated_cost
        
        # 更新每日使用量
        timestamp = usage_info.get("timestamp", datetime.now().isoformat())
        date_key = self._get_date_key(timestamp)
        
        if date_key not in self.usage_data["daily_usage"]:
            self.usage_data["daily_usage"][date_key] = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "requests": 0
            }
        
        daily = self.usage_data["daily_usage"][date_key]
        daily["prompt_tokens"] += usage_info.get("prompt_tokens", 0)
        daily["completion_tokens"] += usage_info.get("completion_tokens", 0)
        daily["total_tokens"] += usage_info.get("total_tokens", 0)
        daily["estimated_cost"] += estimated_cost
        daily["requests"] += 1
        
        # 更新模型使用量
        if model not in self.usage_data["model_usage"]:
            self.usage_data["model_usage"][model] = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "requests": 0
            }
        
        model_usage = self.usage_data["model_usage"][model]
        model_usage["prompt_tokens"] += usage_info.get("prompt_tokens", 0)
        model_usage["completion_tokens"] += usage_info.get("completion_tokens", 0)
        model_usage["total_tokens"] += usage_info.get("total_tokens", 0)
        model_usage["estimated_cost"] += estimated_cost
        model_usage["requests"] += 1
        
        # 保存数据
        self._save_usage_data()
        
        logger.info(f"记录token使用: {usage_info.get('total_tokens', 0)} tokens, 模型: {model}")
    
    def _get_date_key(self, timestamp: str) -> str:
        """从时间戳获取日期键"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d")
        except:
            return datetime.now().strftime("%Y-%m-%d")
    
    def _calculate_cost(self, prompt_tokens: int, completion_tokens: int, model: str) -> float:
        """
        计算token成本
        
        Args:
            prompt_tokens: 输入token数量
            completion_tokens: 输出token数量
            model: 模型名称
            
        Returns:
            估算成本（美元）
        """
        # 2024年最新费率 (每1000 tokens)
        rates = {
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
        }
        
        # 获取模型费率，默认使用gpt-4o-mini
        model_rates = rates.get(model, rates["gpt-4o-mini"])
        
        input_cost = (prompt_tokens / 1000) * model_rates["input"]
        output_cost = (completion_tokens / 1000) * model_rates["output"]
        
        return input_cost + output_cost
    
    def get_total_usage(self) -> Dict:
        """获取总使用情况"""
        return self.usage_data["total_usage"]
    
    def get_daily_usage(self, days: int = 30) -> List[Dict]:
        """
        获取指定天数的每日使用情况
        
        Args:
            days: 要获取的天数
            
        Returns:
            每日使用情况列表，按日期排序
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        daily_usage = []
        current_date = start_date
        
        while current_date <= end_date:
            date_key = current_date.strftime("%Y-%m-%d")
            usage = self.usage_data["daily_usage"].get(date_key, {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "requests": 0
            })
            
            daily_usage.append({
                "date": date_key,
                **usage
            })
            
            current_date += timedelta(days=1)
        
        return daily_usage
    
    def get_model_usage(self) -> Dict:
        """获取各模型使用情况"""
        return self.usage_data["model_usage"]
    
    def get_usage_summary(self) -> Dict:
        """获取使用情况摘要"""
        total = self.get_total_usage()
        daily = self.get_daily_usage(7)  # 最近7天
        models = self.get_model_usage()
        
        return {
            "total": total,
            "recent_daily": daily,
            "models": models,
            "last_updated": self.usage_data["last_updated"]
        }
    
    def reset_usage(self):
        """重置所有使用数据"""
        self.usage_data = self._get_default_structure()
        self._save_usage_data()
        logger.info("已重置所有token使用数据")

# 全局实例
token_tracker = TokenUsageTracker() 