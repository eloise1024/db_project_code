from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import crud
from ..schemas import schemas

router = APIRouter()

@router.post("/", response_model=schemas.DeviceUsageLog)
def create_usage_log(usage_log: schemas.DeviceUsageLogCreate, db: Session = Depends(get_db)):
    return crud.device_usage_log.create(db=db, obj_in=usage_log)

@router.get("/{usage_id}", response_model=schemas.DeviceUsageLog)
def read_usage_log(usage_id: str, db: Session = Depends(get_db)):
    db_usage_log = crud.device_usage_log.get(db, usage_id=usage_id)
    if db_usage_log is None:
        raise HTTPException(status_code=404, detail="Usage log not found")
    return db_usage_log

@router.get("/", response_model=List[schemas.DeviceUsageLog])
def read_usage_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usage_logs = crud.device_usage_log.get_multi(db, skip=skip, limit=limit)
    return usage_logs

@router.get("/device/{device_id}", response_model=List[schemas.DeviceUsageLog])
def read_usage_logs_by_device(device_id: str, db: Session = Depends(get_db)):
    usage_logs = crud.device_usage_log.get_by_device(db, device_id=device_id)
    return usage_logs

@router.delete("/{usage_id}")
def delete_usage_log(usage_id: str, db: Session = Depends(get_db)):
    db_usage_log = crud.device_usage_log.remove(db, usage_id=usage_id)
    if db_usage_log is None:
        raise HTTPException(status_code=404, detail="Usage log not found")
    return {"message": "Usage log deleted successfully"}