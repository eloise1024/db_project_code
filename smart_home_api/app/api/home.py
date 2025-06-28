from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import text 
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/homes",
    tags=["homes"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Home)
def create_home(home: schemas.HomeCreate, db: Session = Depends(get_db)):
    """创建新房屋"""
    db_home = crud.get_home(db, home_id=home.home_id)
    if db_home:
        raise HTTPException(status_code=400, detail="Home already exists")
    return crud.create_home(db=db, home=home)

@router.get("/", response_model=List[schemas.Home])
def read_homes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取房屋列表"""
    homes = crud.get_homes(db, skip=skip, limit=limit)
    return homes

@router.get("/{home_id}", response_model=schemas.Home)
def read_home(home_id: str, db: Session = Depends(get_db)):
    """获取单个房屋信息"""
    db_home = crud.get_home(db, home_id=home_id)
    if db_home is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return db_home

@router.put("/{home_id}", response_model=schemas.Home)
def update_home(home_id: str, home: schemas.HomeUpdate, db: Session = Depends(get_db)):
    """更新房屋信息"""
    db_home = crud.update_home(db, home_id=home_id, home=home)
    if db_home is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return db_home

@router.delete("/{home_id}", response_model=schemas.Home)
def delete_home(home_id: str, db: Session = Depends(get_db)):
    """删除房屋"""
    db_home = crud.delete_home(db, home_id=home_id)
    if db_home is None:
        raise HTTPException(status_code=404, detail="Home not found")
    return db_home

@router.get("/{home_id}/users", response_model=schemas.HomeUsersResponse)
def get_home_users(home_id: str, db: Session = Depends(get_db)):
    """获取房屋关联的所有用户"""
    home = crud.get_home(db, home_id=home_id)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    
    users, relations = crud.get_home_users(db, home_id=home_id)
    
    return schemas.HomeUsersResponse(
        home=home,
        users=users,
        relations=relations
    )

####################################
@router.get("/{home_id}/devices")
def get_home_devices_simple(home_id: str, db: Session = Depends(get_db)):
    """简化版获取房屋设备"""
    from .. import models
    try:
        # 直接查询，不使用response_model
        devices = db.query(models.Device).filter(models.Device.home_id == home_id).all()
        
        # 手动构建响应
        result = []
        for device in devices:
            device_dict = {
                "device_id": device.device_id,
                "name": device.name,
                "device_type": device.device_type,
                "room_name": device.room_name,
                "home_id": device.home_id,
                "status": getattr(device, 'status', 'unknown'),
                "last_activity": getattr(device, 'last_activity', None)
            }
            result.append(device_dict)
        
        return result
        
    except Exception as e:
        print(f"查询设备错误: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")
#######################################

@router.get("/{home_id}/devices/{device_id}/usage-stats")
def get_device_usage_stats(
    home_id: str, 
    device_id: str, 
    period: str,
    db: Session = Depends(get_db)
):
    """获取设备使用统计（日、周、月、年）"""
    if period not in ["day", "week", "month", "year"]:
        raise HTTPException(status_code=400, detail="Invalid period. Must be one of: day, week, month, year")
    
    stats = crud.get_device_usage_stats(db, home_id=home_id, device_id=device_id, period=period)
    if not stats:
        raise HTTPException(status_code=404, detail="Device not found or not in this home")
    
    return stats

@router.get("/{home_id}/devices/{device_id}/usage-stats/chart")
def get_device_usage_chart(
    home_id: str, 
    device_id: str,
    db: Session = Depends(get_db)
):
    """获取设备使用统计的条形图数据"""
    periods = ["day", "week", "month", "year"]
    labels = []
    data = []
    
    for period in periods:
        stats = crud.get_device_usage_stats(db, home_id=home_id, device_id=device_id, period=period)
        if stats:
            labels.append(period.capitalize())
            data.append(stats["total_duration"] / 3600)  # 转换为小时
    
    if not data:
        raise HTTPException(status_code=404, detail="Device not found or no usage data")
    
    return schemas.ChartData(
        labels=labels,
        data=data,
        chart_type="bar",
        title=f"Device Usage Statistics"
    )

@router.get("/{home_id}/devices/{device_id}/time-slot-usage")
def get_device_time_slot_usage(home_id: str, device_id: str, db: Session = Depends(get_db)):
    """获取设备使用时间段分布"""
    usage_data = crud.get_device_time_slot_usage(db, home_id=home_id, device_id=device_id)
    if not usage_data:
        raise HTTPException(status_code=404, detail="Device not found or not in this home")
    
    return usage_data

@router.get("/{home_id}/devices/{device_id}/time-slot-usage/chart")
def get_device_time_slot_chart(home_id: str, device_id: str, db: Session = Depends(get_db)):
    """获取设备使用时间段分布的条形图数据"""
    usage_data = crud.get_device_time_slot_usage(db, home_id=home_id, device_id=device_id)
    if not usage_data:
        raise HTTPException(status_code=404, detail="Device not found or no usage data")
    
    labels = [item["time_slot"] for item in usage_data]
    data = [item["usage_count"] for item in usage_data]
    
    return schemas.ChartData(
        labels=labels,
        data=data,
        chart_type="bar",
        title="Device Usage Distribution by Time Slot"
    )

@router.get("/{home_id}/device-correlation")
def get_home_device_correlation(home_id: str, db: Session = Depends(get_db)):
    """获取房屋设备使用关联性"""
    home = crud.get_home(db, home_id=home_id)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    
    correlations = crud.get_device_correlation(db, home_id=home_id)
    return correlations

@router.get("/{home_id}/device-correlation/chart")
def get_home_device_correlation_chart(home_id: str, db: Session = Depends(get_db)):
    """获取房屋设备使用关联性的琴弦图数据"""
    home = crud.get_home(db, home_id=home_id)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    
    correlations = crud.get_device_correlation(db, home_id=home_id)
    
    # 构建节点和连接数据
    devices = set()
    for corr in correlations:
        devices.add(corr["device1"])
        devices.add(corr["device2"])
    
    nodes = [{"id": device, "name": device} for device in devices]
    links = [
        {
            "source": corr["device1"],
            "target": corr["device2"],
            "value": corr["correlation_probability"]
        }
        for corr in correlations if corr["correlation_probability"] > 0.1  # 只显示相关性大于10%的
    ]
    
    return schemas.CorrelationChartData(
        nodes=nodes,
        links=links,
        title="Device Usage Correlation"
    )

@router.get("/{home_id}/alerts", response_model=List[schemas.SecurityEvent])
def get_home_alerts(home_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取房屋的所有警报事件"""
    home = crud.get_home(db, home_id=home_id)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    
    alerts = crud.get_security_events(db, home_id=home_id, skip=skip, limit=limit)
    return alerts

@router.get("/{home_id}/alerts/distribution")
def get_home_alert_distribution(home_id: str, db: Session = Depends(get_db)):
    """获取单个房屋发出的警报的类型分布"""
    home = crud.get_home(db, home_id=home_id)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    
    distribution = crud.get_alert_distribution(db, home_id=home_id)
    return distribution

@router.get("/{home_id}/alerts/distribution/chart")
def get_home_alert_distribution_chart(home_id: str, db: Session = Depends(get_db)):
    """获取单个房屋警报类型分布的饼图数据"""
    home = crud.get_home(db, home_id=home_id)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    
    distribution = crud.get_alert_distribution(db, home_id=home_id)
    
    if not distribution:
        raise HTTPException(status_code=404, detail="No alert data found")
    
    labels = [item["device_type"] for item in distribution]
    data = [item["count"] for item in distribution]
    
    return schemas.ChartData(
        labels=labels,
        data=data,
        chart_type="pie",
        title=f"Alert Distribution for Home {home_id}"
    )



#######################
@router.get("/{home_id}/devices-debug")
def debug_home_devices(home_id: str, db: Session = Depends(get_db)):
    """调试版本的获取房屋设备"""
    from .. import models
    try:
        print(f"=== 调试开始: 查询房屋 {home_id} 的设备 ===")
        
        # 检查数据库连接
        try:
            db.execute("SELECT 1")
            print("✅ 数据库连接正常")
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            return {"error": "数据库连接失败", "detail": str(e)}
        
        # 检查房屋是否存在
        try:
            home = db.query(models.Home).filter(models.Home.home_id == home_id).first()
            if home:
                print(f"✅ 房屋存在: {home.address}")
            else:
                print(f"❌ 房屋不存在: {home_id}")
                return {"error": "房屋不存在", "home_id": home_id}
        except Exception as e:
            print(f"❌ 查询房屋失败: {e}")
            return {"error": "查询房屋失败", "detail": str(e)}
        
        # 尝试查询设备
        try:
            devices = db.query(models.Device).filter(models.Device.home_id == home_id).all()
            print(f"✅ 查询成功，找到 {len(devices)} 个设备")
            
            device_info = []
            for device in devices:
                device_dict = {
                    "device_id": device.device_id,
                    "name": device.name,
                    "device_type": device.device_type,
                    "room_name": device.room_name,
                    "home_id": device.home_id
                }
                device_info.append(device_dict)
            
            return {
                "success": True,
                "home_id": home_id,
                "device_count": len(devices),
                "devices": device_info
            }
            
        except Exception as e:
            print(f"❌ 查询设备失败: {e}")
            import traceback
            traceback.print_exc()
            return {"error": "查询设备失败", "detail": str(e)}
            
    except Exception as e:
        print(f"❌ 总体调试失败: {e}")
        import traceback
        traceback.print_exc()
        return {"error": "调试失败", "detail": str(e)}