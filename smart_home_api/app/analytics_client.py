# app/analytics_client.py - 完整版本

import requests
import base64
from io import BytesIO

# 处理可选依赖
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️ matplotlib未安装，图表功能将受限")

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("⚠️ PIL/Pillow未安装，图表显示功能将受限")

# API配置
API_BASE = "http://127.0.0.1:8000/api/v1/analytics"

def test_connection():
    """测试API连接"""
    print("🔗 测试API连接...")
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ API服务器连接正常")
            return True
        else:
            print(f"⚠️ API服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器")
        print("💡 请确保运行: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def _make_request(endpoint, params=None):
    """统一的API请求处理"""
    try:
        url = f"{API_BASE}{endpoint}"
        print(f"🔗 请求: {url}")
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败：请确保API服务器正在运行")
        return None
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

def _show_chart(chart_data):
    """显示图表"""
    if not HAS_MATPLOTLIB or not HAS_PIL:
        print("⚠️ 无法显示图表：缺少matplotlib或PIL")
        return chart_data
        
    if 'chart' in chart_data and chart_data['chart']:
        try:
            # 解码base64图片
            image_data = base64.b64decode(chart_data['chart'].split(',')[1])
            image = Image.open(BytesIO(image_data))
            
            # 显示图片
            plt.figure(figsize=(12, 8))
            plt.imshow(image)
            plt.axis('off')
            plt.title('分析结果图表')
            plt.show()
        except Exception as e:
            print(f"⚠️ 图表显示失败: {e}")
    return chart_data

def user_homes(user_id):
    """查看某账户关联的所有房屋"""
    print(f"🔍 查询用户 {user_id} 的房屋信息...")
    result = _make_request(f"/user/{user_id}/homes")
    
    if result:
        print(f"\n👤 用户: {result['user_info']['name']} ({result['user_info']['user_id']})")
        print(f"📱 电话: {result['user_info']['number']}")
        print(f"🏠 关联房屋数量: {result['total_homes']} 个")
        print("-" * 50)
        
        for i, home in enumerate(result['homes'], 1):
            print(f"{i}. {home['address']}")
            print(f"   房屋ID: {home['home_id']}")
            print(f"   面积: {home['area_sqm']} ㎡")
            print(f"   关系: {home['relation']}")
            print()
    return result

def home_users(home_id):
    """查看某房屋关联的所有账户"""
    print(f"🔍 查询房屋 {home_id} 的用户信息...")
    result = _make_request(f"/home/{home_id}/users")
    
    if result:
        print(f"\n🏠 房屋: {result['home_info']['address']}")
        print(f"📏 面积: {result['home_info']['area_sqm']} ㎡")
        print(f"👥 关联用户数量: {result['total_users']} 个")
        print("-" * 50)
        
        for i, user in enumerate(result['users'], 1):
            print(f"{i}. {user['name']} ({user['relation']})")
            print(f"   用户ID: {user['user_id']}")
            print(f"   电话: {user['number']}")
            print(f"   注册时间: {user['register_time']}")
            print()
    return result

def device_weekly(home_id, device_name):
    """设备过去7天和7周使用时长可视化"""
    print(f"🔍 分析设备 {device_name} 的使用情况...")
    result = _make_request(f"/home/{home_id}/device/{device_name}/weekly-usage")
    
    if result:
        device = result['device_info']
        print(f"\n🔧 设备: {device['name']} ({device['device_type']})")
        print(f"📍 位置: {device['room_name']}")
        print(f"📊 日均使用时长: {result['daily_avg']} 小时")
        print(f"📊 周均使用时长: {result['weekly_avg']} 小时")
        print("-" * 50)
        
        print("📅 过去7天使用时长:")
        for date, hours in zip(result['daily_labels'], result['daily_data']):
            print(f"   {date}: {hours:.1f} 小时")
        
        print(f"\n📅 过去7周使用时长:")
        for i, (week, hours) in enumerate(zip(result['weekly_labels'], result['weekly_data'])):
            print(f"   第{7-i}周 ({week.split('~')[0]}): {hours:.1f} 小时")
        
        _show_chart(result)
    return result

def device_hourly(home_id, device_name):
    """设备使用时间段分布(每2小时一个时间段)"""
    print(f"🔍 分析设备 {device_name} 的时间段分布...")
    result = _make_request(f"/home/{home_id}/device/{device_name}/hourly-usage")
    
    if result:
        device = result['device_info']
        print(f"\n🔧 设备: {device['name']} ({device['device_type']})")
        print(f"📍 位置: {device['room_name']}")
        print(f"⏰ 使用高峰时段: {result['peak_slot']}")
        print(f"📊 总使用时长: {result['total_usage']} 小时")
        print("-" * 50)
        
        print("⏰ 时间段使用分布:")
        for slot, hours in zip(result['time_slots'], result['usage_hours']):
            print(f"   {slot}: {hours:.1f} 小时")
        
        _show_chart(result)
    return result

def device_correlation(home_id):
    """房屋设备使用关联分析"""
    print(f"🔍 分析房屋 {home_id} 的设备使用关联...")
    result = _make_request(f"/home/{home_id}/device-correlation")
    
    if result:
        print(f"\n🔗 设备使用关联分析")
        print(f"🏠 房屋ID: {result['home_id']}")
        print(f"🔧 设备数量: {len(result['devices'])} 个")
        print("-" * 50)
        
        print("📊 设备关联度TOP5:")
        for i, corr in enumerate(result['top_correlations'], 1):
            print(f"{i}. {corr['device1']} ↔ {corr['device2']}: {corr['correlation']}%")
        
        _show_chart(result)
    return result

def area_ac_analysis():
    """所有房屋面积与空调使用关系散点图"""
    print("🔍 分析房屋面积与空调使用关系...")
    result = _make_request("/system/area-ac-correlation")
    
    if result:
        print(f"\n📈 房屋面积与空调使用关系分析")
        print(f"🏠 分析房屋数量: {result['total_homes']} 个")
        print(f"📊 相关系数: {result['correlation_coefficient']}")
        print(f"📈 趋势分析: {result['trend_analysis']}")
        print(f"📏 面积范围: {result['area_range']['min']} - {result['area_range']['max']} ㎡")
        print(f"⏰ 使用时长范围: {result['usage_range']['min']} - {result['usage_range']['max']} 小时")
        
        _show_chart(result)
    return result

def system_alerts():
    """系统警报类型分布饼图"""
    print("🔍 分析系统警报分布...")
    result = _make_request("/system/alert-distribution")
    
    if result:
        print(f"\n🚨 系统警报分析")
        print(f"📊 总警报数量: {result['total_alerts']} 个")
        print(f"⚠️ 最常见警报: {result['most_common']}")
        print("-" * 50)
        
        print("📊 警报类型分布:")
        for alert_type, count, percentage in zip(result['alert_types'], 
                                                result['alert_counts'], 
                                                result['percentages']):
            print(f"   {alert_type}: {count} 个 ({percentage}%)")
        
        _show_chart(result)
    return result

def home_alerts(home_id):
    """某房屋警报类型分布"""
    print(f"🔍 分析房屋 {home_id} 的警报...")
    result = _make_request(f"/home/{home_id}/alert-distribution")
    
    if result:
        if result.get('total_alerts', 0) == 0:
            print(f"\n✅ 房屋暂无警报记录")
        else:
            print(f"\n🚨 房屋警报分析: {result.get('home_address', home_id)}")
            print(f"📊 总警报数量: {result['total_alerts']} 个")
            print("-" * 50)
            
            print("📊 警报类型分布:")
            for alert_type, count in zip(result['alert_types'], result['alert_counts']):
                percentage = count / result['total_alerts'] * 100
                print(f"   {alert_type}: {count} 个 ({percentage:.1f}%)")
            
            _show_chart(result)
    return result

def feedback_devices():
    """用户反馈设备类型分布"""
    print("🔍 分析用户反馈设备分布...")
    result = _make_request("/system/feedback-device-distribution")
    
    if result:
        print(f"\n💬 用户反馈设备类型分析")
        print(f"📊 总反馈数量: {result['total_feedbacks']} 个")
        print(f"🔧 反馈最多设备: {result['most_reported']}")
        print("-" * 50)
        
        print("📊 设备反馈分布:")
        for device_type, count, percentage in zip(result['device_types'], 
                                                 result['feedback_counts'], 
                                                 result['percentages']):
            print(f"   {device_type}: {count} 个 ({percentage}%)")
        
        _show_chart(result)
    return result

def feedback_resolution():
    """反馈解决状态百分比堆积条形图"""
    print("🔍 分析反馈解决状态...")
    result = _make_request("/system/feedback-resolution-status")
    
    if result:
        print(f"\n✅ 反馈解决状态分析")
        print(f"📊 总反馈数量: {result['total_feedbacks']} 个")
        print(f"📈 总体解决率: {result['overall_resolution_rate']}%")
        print(f"🏆 解决率最高设备: {result['best_resolution_device']}")
        print(f"⚠️ 解决率最低设备: {result['worst_resolution_device']}")
        print("-" * 50)
        
        print("📊 各设备解决状态:")
        for i, device_type in enumerate(result['device_types']):
            resolved = result['resolved_percentages'][i]
            unresolved = result['unresolved_percentages'][i]
            total = result['total_counts'][i]
            print(f"   {device_type}: {resolved:.1f}%已解决, {unresolved:.1f}%未解决 (总计{total}个)")
        
        _show_chart(result)
    return result

def show_help():
    """显示使用帮助"""
    print("🚀 Analytics Client 使用指南")
    print("=" * 50)
    print("1. 用户房屋关联:")
    print("   user_homes('user123')           # 查看用户房屋")
    print("   home_users('home001')           # 查看房屋用户")
    print()
    print("2. 设备分析:")
    print("   device_weekly('home001', '空调')  # 7天/7周使用分析")
    print("   device_hourly('home001', '空调')  # 时间段分布")
    print("   device_correlation('home001')    # 设备关联分析")
    print()
    print("3. 系统分析:")
    print("   area_ac_analysis()              # 面积空调关系")
    print("   system_alerts()                 # 系统警报分析")
    print("   home_alerts('home001')          # 房屋警报分析")
    print("   feedback_devices()              # 反馈设备分布")
    print("   feedback_resolution()           # 反馈解决状态")
    print()
    print("💡 使用 test_connection() 测试API连接")

# 简洁别名
uh = user_homes
hu = home_users
dw = device_weekly
dh = device_hourly
dc = device_correlation
aac = area_ac_analysis
sa = system_alerts
ha = home_alerts
fd = feedback_devices
fr = feedback_resolution

if __name__ == "__main__":
    print("Analytics Client 已加载")
    print("使用 show_help() 查看帮助")
    test_connection()