from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import crud
from ..schemas import schemas

router = APIRouter()

@router.post("/", response_model=schemas.DeviceFeedback)
def create_feedback(feedback: schemas.DeviceFeedbackCreate, db: Session = Depends(get_db)):
    return crud.device_feedback.create(db=db, obj_in=feedback)

@router.get("/{feedback_id}", response_model=schemas.DeviceFeedback)
def read_feedback(feedback_id: str, db: Session = Depends(get_db)):
    db_feedback = crud.device_feedback.get(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return db_feedback

@router.get("/", response_model=List[schemas.DeviceFeedback])
def read_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feedbacks = crud.device_feedback.get_multi(db, skip=skip, limit=limit)
    return feedbacks

@router.put("/{feedback_id}", response_model=schemas.DeviceFeedback)
def update_feedback(feedback_id: str, feedback: schemas.DeviceFeedbackUpdate, db: Session = Depends(get_db)):
    db_feedback = crud.device_feedback.get(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return crud.device_feedback.update(db=db, db_obj=db_feedback, obj_in=feedback)

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: str, db: Session = Depends(get_db)):
    db_feedback = crud.device_feedback.remove(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted successfully"}