from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from..crud import crud
from ..schemas import schemas

router = APIRouter()

@router.post("/", response_model=schemas.UserHomeRelation)
def create_user_home_relation(relation: schemas.UserHomeRelationCreate, db: Session = Depends(get_db)):
    return crud.user_home_relation.create(db=db, obj_in=relation)

@router.get("/{user_id}/{home_id}", response_model=schemas.UserHomeRelation)
def read_user_home_relation(user_id: str, home_id: str, db: Session = Depends(get_db)):
    db_relation = crud.user_home_relation.get(db, user_id=user_id, home_id=home_id)
    if db_relation is None:
        raise HTTPException(status_code=404, detail="User-Home relation not found")
    return db_relation

@router.get("/", response_model=List[schemas.UserHomeRelation])
def read_user_home_relations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    relations = crud.user_home_relation.get_multi(db, skip=skip, limit=limit)
    return relations

@router.delete("/{user_id}/{home_id}")
def delete_user_home_relation(user_id: str, home_id: str, db: Session = Depends(get_db)):
    db_relation = crud.user_home_relation.remove(db, user_id=user_id, home_id=home_id)
    if db_relation is None:
        raise HTTPException(status_code=404, detail="User-Home relation not found")
    return {"message": "User-Home relation deleted successfully"}