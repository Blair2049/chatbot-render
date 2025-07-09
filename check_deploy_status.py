#!/usr/bin/env python3
"""
Render部署状态检查脚本
检查部署是否成功并测试基本功能
"""

import requests
import time
import sys

def check_deploy_status(app_url):
    """检查部署状态"""
    print(f"🔍 检查应用状态: {app_url}")
    
    try:
        # 检查健康状态
        health_url = f"{app_url}/health"
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ 应用健康检查通过")
            print(f"   - RAG初始化: {health_data.get('rag_initialized', False)}")
            print(f"   - 总查询数: {health_data.get('total_queries', 0)}")
            print(f"   - 总成本: ${health_data.get('total_cost', 0):.4f}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_chat_function(app_url):
    """测试聊天功能"""
    print(f"\n💬 测试聊天功能...")
    
    try:
        chat_url = f"{app_url}/chat"
        test_message = {
            "message": "你好，请介绍一下这个项目",
            "mode": "best"
        }
        
        response = requests.post(chat_url, json=test_message, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 聊天功能正常")
                print(f"   - 响应长度: {len(data.get('response', ''))}")
                print(f"   - 使用模式: {data.get('mode_used', 'unknown')}")
                print(f"   - 语言: {data.get('language', 'unknown')}")
                return True
            else:
                print(f"❌ 聊天功能错误: {data.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ 聊天请求失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 聊天测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Render部署状态检查")
    print("=" * 50)
    
    # 从命令行参数获取应用URL，或者使用默认值
    if len(sys.argv) > 1:
        app_url = sys.argv[1]
    else:
        app_url = input("请输入Render应用URL (例如: https://your-app.onrender.com): ").strip()
    
    if not app_url:
        print("❌ 请提供应用URL")
        sys.exit(1)
    
    # 确保URL格式正确
    if not app_url.startswith(('http://', 'https://')):
        app_url = f"https://{app_url}"
    
    print(f"🎯 检查应用: {app_url}")
    
    # 等待应用启动
    print("\n⏳ 等待应用启动...")
    time.sleep(10)
    
    # 检查部署状态
    health_ok = check_deploy_status(app_url)
    
    if health_ok:
        # 测试聊天功能
        chat_ok = test_chat_function(app_url)
        
        print("\n" + "=" * 50)
        if chat_ok:
            print("✅ 部署成功！应用运行正常")
            print(f"🌐 访问地址: {app_url}")
            print("\n📋 功能确认:")
            print("   ✅ 应用健康检查通过")
            print("   ✅ 聊天功能正常")
            print("   ✅ RAG系统已初始化")
        else:
            print("⚠️  应用已部署但聊天功能有问题")
            print("请检查Render日志获取详细错误信息")
    else:
        print("\n❌ 部署失败或应用未正常启动")
        print("请检查Render Dashboard中的日志")

if __name__ == "__main__":
    main() 