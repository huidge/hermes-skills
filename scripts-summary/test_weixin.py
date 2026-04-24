#!/usr/bin/env python3
"""
测试微信通知功能
"""
import json
import os
import sys
from pathlib import Path

# 添加 hermes 模块路径
sys.path.insert(0, str(Path.home() / '.hermes' / 'hermes-agent'))

def test_weixin_config():
    """测试微信配置"""
    env_file = Path.home() / '.hermes' / '.env'
    
    if not env_file.exists():
        print("❌ 配置文件不存在")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    required_keys = ['WEIXIN_ACCOUNT_ID', 'WEIXIN_TOKEN', 'WEIXIN_BASE_URL']
    
    for key in required_keys:
        if key not in content:
            print(f"❌ 缺少配置: {key}")
            return False
    
    print("✅ 微信配置检查通过")
    return True

def main():
    """主函数"""
    print("测试微信通知功能配置")
    print("=" * 50)
    
    # 检查配置
    if not test_weixin_config():
        print("\n❌ 配置检查失败")
        return
    
    print("\n✅ 配置检查通过")
    print("\n📋 当前配置:")
    print("  - 微信账号: 18e6ee1b970f@im.bot")
    print("  - 目标用户: o9cq80w94I2T7Bk4HCevUEWyCibc@im.wechat")
    print("  - API地址: https://ilinkai.weixin.qq.com")
    
    print("\n💡 测试建议:")
    print("  1. 检查网络连接")
    print("  2. 验证 API 服务是否可用")
    print("  3. 确认用户 ID 是否正确")
    
    print("\n🔧 手动测试方法:")
    print("  1. 使用 hermes 命令发送测试消息")
    print("  2. 检查系统日志中的错误信息")
    print("  3. 验证微信服务是否正常运行")

if __name__ == '__main__':
    main()
