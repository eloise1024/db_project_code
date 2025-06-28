# import_test.py - 测试导入问题

import sys
import os

print("🔍 当前Python环境:")
print(f"工作目录: {os.getcwd()}")
print(f"Python路径: {sys.executable}")

print("\n📁 检查文件存在:")
print(f"app目录: {os.path.exists('app')}")
print(f"app/__init__.py: {os.path.exists('app/__init__.py')}")
print(f"app/analytics_client.py: {os.path.exists('app/analytics_client.py')}")

print("\n🧪 测试不同导入方式:")

# 测试1：导入app模块
try:
    import app
    print("✅ import app - 成功")
except Exception as e:
    print(f"❌ import app - 失败: {e}")

# 测试2：导入analytics_client模块
try:
    from app import analytics_client
    print("✅ from app import analytics_client - 成功")
except Exception as e:
    print(f"❌ from app import analytics_client - 失败: {e}")

# 测试3：导入具体函数
try:
    from app.analytics_client import test_connection
    print("✅ from app.analytics_client import test_connection - 成功")
except Exception as e:
    print(f"❌ from app.analytics_client import test_connection - 失败: {e}")

# 测试4：通配符导入
try:
    from app.analytics_client import *
    print("✅ from app.analytics_client import * - 成功")
    print(f"   可用函数示例: {[name for name in globals() if not name.startswith('_')][:5]}")
except Exception as e:
    print(f"❌ from app.analytics_client import * - 失败: {e}")

# 测试5：如果通配符导入成功，测试API连接
if 'test_connection' in globals():
    print("\n🔗 测试API连接:")
    try:
        result = test_connection()
        if result:
            print("✅ API连接测试成功")
        else:
            print("⚠️ API连接失败，但函数运行正常")
    except Exception as e:
        print(f"❌ API连接测试失败: {e}")

print("\n📋 当前globals()中的函数:")
analytics_functions = [name for name in globals() if not name.startswith('_') and callable(globals().get(name))]
if analytics_functions:
    print("可用的analytics函数:")
    for func in analytics_functions:
        print(f"   - {func}")
else:
    print("❌ 没有找到analytics函数")