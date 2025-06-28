from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, extract, case
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from . import models, schemas
from collections import defaultdict

# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: str, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        update_data = user.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Home CRUD operations
def create_home(db: Session, home: schemas.HomeCreate):
    db_home = models.Home(**home.dict())
    db.add(db_home)
    db.commit()
    db.refresh(db_home)
    return db_home

def get_home(db: Session, home_id: str):
    return db.query(models.Home).filter(models.Home.home_id == home_id).first()

def get_homes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Home).offset(skip).limit(limit).all()

def update_home(db: Session, home_id: str, home: schemas.HomeUpdate):
    db_home = db.query(models.Home).filter(models.Home.home_id == home_id).first()
    if db_home:
        update_data = home.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_home, field, value)
        db.commit()
        db.refresh(db_home)
    return db_home

def delete_home(db: Session, home_id: str):
    db_home = db.query(models.Home).filter(models.Home.home_id == home_id).first()
    if db_home:
        db.delete(db_home)
        db.commit()
    return db_home

# User-Home Relation CRUD operations
def create_user_home_relation(db: Session, relation: schemas.UserHomeRelationCreate):
    db_relation = models.UserHomeRelation(**relation.dict())
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation

def get_user_home_relation(db: Session, user_id: str, home_id: str):
    return db.query(models.UserHomeRelation).filter(
        and_(models.UserHomeRelation.user_id == user_id, models.UserHomeRelation.home_id == home_id)
    ).first()

def update_user_home_relation(db: Session, user_id: str, home_id: str, relation: schemas.UserHomeRelationUpdate):
    db_relation = get_user_home_relation(db, user_id, home_id)
    if db_relation:
        update_data = relation.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_relation, field, value)
        db.commit()
        db.refresh(db_relation)
    return db_relation

def delete_user_home_relation(db: Session, user_id: str, home_id: str):
    db_relation = get_user_home_relation(db, user_id, home_id)
    if db_relation:
        db.delete(db_relation)
        db.commit()
    return db_relation

# Device CRUD operations
def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_home_devices(db: Session, home_id: str):
    """获取房屋中的所有设备"""
    try:
        devices = db.query(models.Device).filter(models.Device.home_id == home_id).all()
        return devices
    except Exception as e:
        print(f"数据库查询设备时发生错误: {e}")
        raise

def get_device(db: Session, device_id: str):
    return db.query(models.Device).filter(models.Device.device_id == device_id).first()

def get_devices(db: Session, home_id: str = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Device)
    if home_id:
        query = query.filter(models.Device.home_id == home_id)
    return query.offset(skip).limit(limit).all()

def update_device(db: Session, device_id: str, device: schemas.DeviceUpdate):
    db_device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if db_device:
        update_data = device.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_device, field, value)
        db.commit()
        db.refresh(db_device)
    return db_device

def delete_device(db: Session, device_id: str):
    db_device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if db_device:
        db.delete(db_device)
        db.commit()
    return db_device

# Device Usage Log CRUD operations
def create_device_usage_log(db: Session, usage_log: schemas.DeviceUsageLogCreate):
    db_usage_log = models.DeviceUsageLog(**usage_log.dict())
    db.add(db_usage_log)
    db.commit()
    db.refresh(db_usage_log)
    return db_usage_log

def get_device_usage_log(db: Session, usage_id: str):
    return db.query(models.DeviceUsageLog).filter(models.DeviceUsageLog.usage_id == usage_id).first()

def get_device_usage_logs(db: Session, device_id: str = None, skip: int = 0, limit: int = 100):
    query = db.query(models.DeviceUsageLog)
    if device_id:
        query = query.filter(models.DeviceUsageLog.device_id == device_id)
    return query.offset(skip).limit(limit).all()

def update_device_usage_log(db: Session, usage_id: str, usage_log: schemas.DeviceUsageLogUpdate):
    db_usage_log = db.query(models.DeviceUsageLog).filter(models.DeviceUsageLog.usage_id == usage_id).first()
    if db_usage_log:
        update_data = usage_log.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_usage_log, field, value)
        db.commit()
        db.refresh(db_usage_log)
    return db_usage_log

def delete_device_usage_log(db: Session, usage_id: str):
    db_usage_log = db.query(models.DeviceUsageLog).filter(models.DeviceUsageLog.usage_id == usage_id).first()
    if db_usage_log:
        db.delete(db_usage_log)
        db.commit()
    return db_usage_log

# Device Feedback CRUD operations
def create_device_feedback(db: Session, feedback: schemas.DeviceFeedbackCreate):
    db_feedback = models.DeviceFeedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_device_feedback(db: Session, feedback_id: str):
    return db.query(models.DeviceFeedback).filter(models.DeviceFeedback.feedback_id == feedback_id).first()

def get_device_feedbacks(db: Session, device_id: str = None, user_id: str = None, skip: int = 0, limit: int = 100):
    query = db.query(models.DeviceFeedback)
    if device_id:
        query = query.filter(models.DeviceFeedback.device_id == device_id)
    if user_id:
        query = query.filter(models.DeviceFeedback.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def update_device_feedback(db: Session, feedback_id: str, feedback: schemas.DeviceFeedbackUpdate):
    db_feedback = db.query(models.DeviceFeedback).filter(models.DeviceFeedback.feedback_id == feedback_id).first()
    if db_feedback:
        update_data = feedback.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_feedback, field, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

def delete_device_feedback(db: Session, feedback_id: str):
    db_feedback = db.query(models.DeviceFeedback).filter(models.DeviceFeedback.feedback_id == feedback_id).first()
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
    return db_feedback

# Security Event CRUD operations
def create_security_event(db: Session, event: schemas.SecurityEventCreate):
    db_event = models.SecurityEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_security_event(db: Session, event_id: str):
    return db.query(models.SecurityEvent).filter(models.SecurityEvent.event_id == event_id).first()

def get_security_events(db: Session, home_id: str = None, device_id: str = None, skip: int = 0, limit: int = 100):
    query = db.query(models.SecurityEvent)
    if home_id:
        query = query.filter(models.SecurityEvent.home_id == home_id)
    if device_id:
        query = query.filter(models.SecurityEvent.device_id == device_id)
    return query.offset(skip).limit(limit).all()

def update_security_event(db: Session, event_id: str, event: schemas.SecurityEventUpdate):
    db_event = db.query(models.SecurityEvent).filter(models.SecurityEvent.event_id == event_id).first()
    if db_event:
        update_data = event.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event, field, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_security_event(db: Session, event_id: str):
    db_event = db.query(models.SecurityEvent).filter(models.SecurityEvent.event_id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event

# Analytics functions
# def get_user_homes(db: Session, user_id: str):
#    """获取用户关联的所有房屋"""
#    relations = db.query(models.UserHomeRelation).filter(models.UserHomeRelation.user_id == user_id).all()
#    homes = []
#    for relation in relations:
#        home = db.query(models.Home).filter(models.Home.home_id == relation.home_id).first()
#        if home:
#            homes.append(home)
#    return homes, relations

def get_home_users(db: Session, home_id: str):
    """获取房屋关联的所有用户"""
    relations = db.query(models.UserHomeRelation).filter(models.UserHomeRelation.home_id == home_id).all()
    users = []
    for relation in relations:
        user = db.query(models.User).filter(models.User.user_id == relation.user_id).first()
        if user:
            users.append(user)
    return users, relations

def get_device_usage_stats(db: Session, home_id: str, device_id: str, period: str):
    """获取设备使用统计（日、周、月、年）"""
    device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not device or device.home_id != home_id:
        return None
    
    now = datetime.now()
    if period == "day":
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start_time = now - timedelta(days=7)
    elif period == "month":
        start_time = now - timedelta(days=30)
    elif period == "year":
        start_time = now - timedelta(days=365)
    else:
        return None
    
    total_duration = db.query(func.sum(models.DeviceUsageLog.duration_seconds)).filter(
        and_(
            models.DeviceUsageLog.device_id == device_id,
            models.DeviceUsageLog.start_time >= start_time
        )
    ).scalar() or 0
    
    return {
        "device_id": device_id,
        "device_name": device.name,
        "total_duration": float(total_duration),
        "period": period
    }

def get_device_time_slot_usage(db: Session, home_id: str, device_id: str):
    """获取设备使用时间段分布（每2小时一个时间段）"""
    device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not device or device.home_id != home_id:
        return []
    
    # 获取最近30天的数据
    start_time = datetime.now() - timedelta(days=30)
    
    usage_logs = db.query(models.DeviceUsageLog).filter(
        and_(
            models.DeviceUsageLog.device_id == device_id,
            models.DeviceUsageLog.start_time >= start_time
        )
    ).all()
    
    time_slots = defaultdict(lambda: {"count": 0, "total_duration": 0})
    
    for log in usage_logs:
        hour = log.start_time.hour
        slot = f"{hour//2*2:02d}:00-{(hour//2*2+2)%24:02d}:00"
        time_slots[slot]["count"] += 1
        time_slots[slot]["total_duration"] += float(log.duration_seconds)
    
    return [
        {
            "time_slot": slot,
            "usage_count": data["count"],
            "total_duration": data["total_duration"]
        }
        for slot, data in sorted(time_slots.items())
    ]

def get_device_correlation(db: Session, home_id: str):
    """获取设备使用关联性"""
    # 获取房屋中的所有设备
    devices = db.query(models.Device).filter(models.Device.home_id == home_id).all()
    device_ids = [d.device_id for d in devices]
    
    # 获取最近30天的使用记录
    start_time = datetime.now() - timedelta(days=30)
    usage_logs = db.query(models.DeviceUsageLog).filter(
        and_(
            models.DeviceUsageLog.device_id.in_(device_ids),
            models.DeviceUsageLog.start_time >= start_time
        )
    ).all()
    
    # 按时间窗口分组（30分钟窗口）
    time_windows = defaultdict(set)
    for log in usage_logs:
        window = log.start_time.replace(minute=log.start_time.minute//30*30, second=0, microsecond=0)
        time_windows[window].add(log.device_id)
    
    # 计算设备共现概率
    correlations = []
    for i, device1 in enumerate(devices):
        for device2 in devices[i+1:]:
            together_count = 0
            device1_count = 0
            
            for window_devices in time_windows.values():
                if device1.device_id in window_devices:
                    device1_count += 1
                    if device2.device_id in window_devices:
                        together_count += 1
            
            if device1_count > 0:
                probability = together_count / device1_count
                correlations.append({
                    "device1": device1.name,
                    "device2": device2.name,
                    "correlation_probability": probability
                })
    
    return correlations

def get_area_usage_correlation(db: Session, device_type: str):
    """分析房屋面积对设备使用行为的影响"""
    # 获取最近30天的数据
    start_time = datetime.now() - timedelta(days=30)
    
    results = db.query(
        models.Home.area_sqm,
        func.avg(models.DeviceUsageLog.duration_seconds).label('avg_daily_usage')
    ).join(
        models.Device, models.Home.home_id == models.Device.home_id
    ).join(
        models.DeviceUsageLog, models.Device.device_id == models.DeviceUsageLog.device_id
    ).filter(
        and_(
            models.Device.device_type == device_type,
            models.DeviceUsageLog.start_time >= start_time
        )
    ).group_by(models.Home.home_id, models.Home.area_sqm).all()
    
    return [
        {
            "area_sqm": float(result.area_sqm),
            "avg_daily_usage": float(result.avg_daily_usage) / 86400,  # 转换为天
            "device_type": device_type
        }
        for result in results
    ]

def get_alert_distribution(db: Session, home_id: str = None):
    """获取警报类型分布"""
    query = db.query(
        models.Device.device_type,
        func.count(models.SecurityEvent.event_id).label('count')
    ).join(
        models.SecurityEvent, models.Device.device_id == models.SecurityEvent.device_id
    )
    
    if home_id:
        query = query.filter(models.SecurityEvent.home_id == home_id)
    
    results = query.group_by(models.Device.device_type).all()
    
    total_count = sum(result.count for result in results)
    
    return [
        {
            "device_type": result.device_type,
            "count": result.count,
            "percentage": (result.count / total_count * 100) if total_count > 0 else 0
        }
        for result in results
    ]

def get_feedback_distribution(db: Session):
    """获取用户反馈的设备类型分布"""
    results = db.query(
        models.Device.device_type,
        func.count(models.DeviceFeedback.feedback_id).label('total_feedback'),
        func.sum(case([(models.DeviceFeedback.resolved == True, 1)], else_=0)).label('resolved_count')
    ).join(
        models.DeviceFeedback, models.Device.device_id == models.DeviceFeedback.device_id
    ).group_by(models.Device.device_type).all()
    
    return [
        {
            "device_type": result.device_type,
            "total_feedback": result.total_feedback,
            "resolved_count": result.resolved_count or 0,
            "unresolved_count": result.total_feedback - (result.resolved_count or 0),
            "resolved_percentage": ((result.resolved_count or 0) / result.total_feedback * 100) if result.total_feedback > 0 else 0
        }
        for result in results
    ]

def get_user_homes(db: Session, user_id: str):
    """获取用户的房屋列表"""
    try:
        # 如果有关系表
        relations = db.query(models.HomeUserRelation).filter(
            models.HomeUserRelation.user_id == user_id
        ).all()
        
        homes = []
        for relation in relations:
            home = get_home(db, relation.home_id)
            if home:
                homes.append(home)
        return homes
    except:
        # 如果没有关系表，返回空列表
        return []