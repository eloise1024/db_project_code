# debug_user_homes.py - 诊断用户房屋关系

import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# 数据库连接（根据你的配置调整）
DATABASE_URL = "sqlite:///./smart_home.db"  # 或者你的实际数据库URL

def check_database_relations():
    """检查数据库中的用户房屋关系"""
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        print("🔍 数据库关系表诊断")
        print("=" * 50)
        
        # 1. 检查用户是否存在
        user_result = db.execute(text("SELECT * FROM users WHERE user_id = 'u223301'"))
        user = user_result.fetchone()
        
        if user:
            print(f"✅ 用户存在: {user}")
        else:
            print("❌ 用户不存在")
            return
        
        # 2. 检查所有表
        print("\n📋 检查数据库表:")
        tables_result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in tables_result.fetchall()]
        
        for table in tables:
            print(f"   - {table}")
        
        # 3. 检查可能的关系表
        relation_tables = [t for t in tables if 'relation' in t.lower() or 'user' in t.lower() and 'home' in t.lower()]
        print(f"\n🔗 可能的关系表: {relation_tables}")
        
        # 4. 检查homes表中是否有用户相关数据
        print(f"\n🏠 检查homes表:")
        try:
            homes_result = db.execute(text("SELECT * FROM homes LIMIT 5"))
            homes = homes_result.fetchall()
            print(f"   homes表样本数据: {len(homes)} 条")
            for home in homes[:3]:
                print(f"     {home}")
        except Exception as e:
            print(f"   ❌ homes表查询失败: {e}")
        
        # 5. 尝试查找用户关联的房屋的多种方式
        print(f"\n🔍 尝试不同的关联查询:")
        
        # 方式1: 检查是否有home_user_relations表
        try:
            relation_result = db.execute(text("SELECT * FROM home_user_relations WHERE user_id = 'u223301'"))
            relations = relation_result.fetchall()
            print(f"   home_user_relations表: {len(relations)} 条记录")
            for rel in relations:
                print(f"     {rel}")
        except Exception as e:
            print(f"   ❌ home_user_relations表不存在或查询失败: {e}")
        
        # 方式2: 检查homes表是否直接包含user_id字段
        try:
            homes_with_user = db.execute(text("SELECT * FROM homes WHERE user_id = 'u223301' OR owner_id = 'u223301'"))
            homes = homes_with_user.fetchall()
            print(f"   homes表直接关联: {len(homes)} 条记录")
            for home in homes:
                print(f"     {home}")
        except Exception as e:
            print(f"   ❌ homes表直接关联查询失败: {e}")
        
        # 方式3: 检查其他可能的关系表
        for table in relation_tables:
            try:
                result = db.execute(text(f"SELECT * FROM {table} WHERE user_id = 'u223301'"))
                records = result.fetchall()
                print(f"   {table}表: {len(records)} 条记录")
                for record in records[:3]:
                    print(f"     {record}")
            except Exception as e:
                print(f"   ❌ {table}表查询失败: {e}")
        
        # 6. 显示所有包含u223301的记录
        print(f"\n🔍 搜索所有包含用户ID的记录:")
        for table in tables:
            try:
                # 获取表结构
                columns_result = db.execute(text(f"PRAGMA table_info({table})"))
                columns = [col[1] for col in columns_result.fetchall()]
                
                # 在所有字符串列中搜索用户ID
                for col in columns:
                    try:
                        search_result = db.execute(text(f"SELECT * FROM {table} WHERE {col} = 'u223301'"))
                        records = search_result.fetchall()
                        if records:
                            print(f"   ✅ {table}.{col}: {len(records)} 条记录")
                            for record in records[:2]:
                                print(f"       {record}")
                    except:
                        pass
            except Exception as e:
                print(f"   ❌ 搜索{table}表失败: {e}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 数据库诊断失败: {e}")

def check_api_endpoints():
    """检查相关API端点"""
    print(f"\n🔗 API端点测试")
    print("=" * 50)
    
    # 测试基础用户API
    try:
        response = requests.get("http://127.0.0.1:8000/api/v1/users/u223301")
        print(f"用户API: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"   用户数据: {user_data}")
    except Exception as e:
        print(f"   ❌ 用户API失败: {e}")
    
    # 测试房屋API
    try:
        response = requests.get("http://127.0.0.1:8000/api/v1/homes/")
        print(f"房屋列表API: {response.status_code}")
        if response.status_code == 200:
            homes_data = response.json()
            print(f"   房屋数量: {len(homes_data)}")
            # 查找包含用户的房屋
            user_homes = [h for h in homes_data if 'u223301' in str(h)]
            print(f"   包含用户的房屋: {len(user_homes)}")
            for home in user_homes:
                print(f"     {home}")
    except Exception as e:
        print(f"   ❌ 房屋API失败: {e}")

def suggest_fixes():
    """提供修复建议"""
    print(f"\n🛠️ 修复建议")
    print("=" * 50)
    print("1. 检查数据库表结构，确认用户房屋关系如何存储")
    print("2. 确认关系表名称（可能是 home_user_relations, user_homes, 等）")
    print("3. 检查关系数据是否正确插入")
    print("4. 修复analytics.py中的查询逻辑")
    print()
    print("💡 临时解决方案：")
    print("如果关系表有问题，可以在analytics.py中使用直接查询:")
    print("例如：查询homes表中owner_id或user_id字段")

if __name__ == "__main__":
    print("🚀 用户房屋关系诊断工具")
    print("=" * 60)
    
    check_database_relations()
    check_api_endpoints()
    suggest_fixes()