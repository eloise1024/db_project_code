from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import crud
from ..schemas import schemas

router = APIRouter()

@router.post("/", response_model=schemas.SecurityEvent)
def create_security_event(security_event: schemas.SecurityEventCreate, db: Session = Depends(get_db)):
    return crud.security_event.create(db=db, obj_in=security_event)

@router.get("/{event_id}", response_model=schemas.SecurityEvent)
def read_security_event(event_id: str, db: Session = Depends(get_db)):
    db_event = crud.security_event.get(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Security event not found")
    return db_event

@router.get("/", response_model=List[schemas.SecurityEvent])
def read_security_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.security_event.get_multi(db, skip=skip, limit=limit)
    return events

@router.get("/home/{home_id}", response_model=List[schemas.SecurityEvent])
def read_security_events_by_home(home_id: str, db: Session = Depends(get_db)):
    events = crud.security_event.get_by_home(db, home_id=home_id)
    return events

@router.delete("/{event_id}")
def delete_security_event(event_id: str, db: Session = Depends(get_db)):
    db_event = crud.security_event.remove(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Security event not found")
    return {"message": "Security event deleted successfully"}
