from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """创建新设备"""
    # 检查房屋是否存在
    home = crud.get_home(db, home_id=device.home_id)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    
    db_device = crud.get_device(db, device_id=device.device_id)
    if db_device:
        raise HTTPException(status_code=400, detail="Device already exists")
    return crud.create_device(db=db, device=device)

@router.get("/", response_model=List[schemas.Device])
def read_devices(home_id: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取设备列表"""
    devices = crud.get_devices(db, home_id=home_id, skip=skip, limit=limit)
    return devices

@router.get("/{device_id}", response_model=schemas.Device)
def read_device(device_id: str, db: Session = Depends(get_db)):
    """获取单个设备信息"""
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.put("/{device_id}", response_model=schemas.Device)
def update_device(device_id: str, device: schemas.DeviceUpdate, db: Session = Depends(get_db)):
    """更新设备信息"""
    db_device = crud.update_device(db, device_id=device_id, device=device)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.delete("/{device_id}", response_model=schemas.Device)
def delete_device(device_id: str, db: Session = Depends(get_db)):
    """删除设备"""
    db_device = crud.delete_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.get("/{device_id}/usage-logs", response_model=List[schemas.DeviceUsageLog])
def get_device_usage_logs(device_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取设备使用记录"""
    device = crud.get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    usage_logs = crud.get_device_usage_logs(db, device_id=device_id, skip=skip, limit=limit)
    return usage_logs

@router.post("/{device_id}/usage-logs", response_model=schemas.DeviceUsageLog)
def create_device_usage_log(
    device_id: str, 
    usage_log: schemas.DeviceUsageLogBase, 
    db: Session = Depends(get_db)
):
    """创建设备使用记录"""
    device = crud.get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # 生成usage_id
    import uuid
    usage_id = str(uuid.uuid4())
    
    usage_log_create = schemas.DeviceUsageLogCreate(
        usage_id=usage_id,
        device_id=device_id,
        **usage_log.dict()
    )
    
    return crud.create_device_usage_log(db=db, usage_log=usage_log_create)

@router.get("/{device_id}/feedbacks", response_model=List[schemas.DeviceFeedback])
def get_device_feedbacks(device_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取设备反馈"""
    device = crud.get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    feedbacks = crud.get_device_feedbacks(db, device_id=device_id, skip=skip, limit=limit)
    return feedbacks

@router.post("/{device_id}/feedbacks", response_model=schemas.DeviceFeedback)
def create_device_feedback(
    device_id: str, 
    feedback: schemas.DeviceFeedbackBase,
    user_id: str,
    db: Session = Depends(get_db)
):
    """创建设备反馈"""
    device = crud.get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 生成feedback_id
    import uuid
    feedback_id = str(uuid.uuid4())
    
    feedback_create = schemas.DeviceFeedbackCreate(
        feedback_id=feedback_id,
        device_id=device_id,
        user_id=user_id,
        **feedback.dict()
    )
    
    return crud.create_device_feedback(db=db, feedback=feedback_create)

@router.get("/{device_id}/security-events", response_model=List[schemas.SecurityEvent])
def get_device_security_events(device_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取设备安全事件"""
    device = crud.get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    events = crud.get_security_events(db, device_id=device_id, skip=skip, limit=limit)
    return events

@router.post("/{device_id}/security-events", response_model=schemas.SecurityEvent)
def create_device_security_event(
    device_id: str, 
    event: schemas.SecurityEventBase,
    db: Session = Depends(get_db)
):
    """创建设备安全事件"""
    device = crud.get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # 生成event_id
    import uuid
    event_id = str(uuid.uuid4())
    
    event_create = schemas.SecurityEventCreate(
        event_id=event_id,
        home_id=device.home_id,
        device_id=device_id,
        **event.dict()
    )
    
    return crud.create_security_event(db=db, event=event_create)