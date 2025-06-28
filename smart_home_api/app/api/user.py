from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """创建新用户"""
    db_user = crud.get_user(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户列表"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    """获取单个用户信息"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """更新用户信息"""
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """删除用户"""
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/{user_id}/homes", response_model=schemas.UserHomesResponse)
def get_user_homes(user_id: str, db: Session = Depends(get_db)):
    """获取用户关联的所有房屋"""
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    homes, relations = crud.get_user_homes(db, user_id=user_id)
    
    return schemas.UserHomesResponse(
        user=user,
        homes=homes,
        relations=relations
    )

@router.post("/{user_id}/homes/{home_id}", response_model=schemas.UserHomeRelation)
def create_user_home_relation(
    user_id: str, 
    home_id: str, 
    relation_data: schemas.UserHomeRelationBase,
    db: Session = Depends(get_db)
):
    """创建用户-房屋关联关系"""
    # 检查用户和房屋是否存在
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    home = crud.get_home(db, home_id=home_id)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    
    # 检查关系是否已存在
    existing_relation = crud.get_user_home_relation(db, user_id=user_id, home_id=home_id)
    if existing_relation:
        raise HTTPException(status_code=400, detail="Relation already exists")
    
    relation = schemas.UserHomeRelationCreate(
        user_id=user_id,
        home_id=home_id,
        relation=relation_data.relation
    )
    
    return crud.create_user_home_relation(db=db, relation=relation)

@router.put("/{user_id}/homes/{home_id}", response_model=schemas.UserHomeRelation)
def update_user_home_relation(
    user_id: str,
    home_id: str,
    relation_data: schemas.UserHomeRelationUpdate,
    db: Session = Depends(get_db)
):
    """更新用户-房屋关联关系"""
    relation = crud.update_user_home_relation(db, user_id=user_id, home_id=home_id, relation=relation_data)
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    return relation

@router.delete("/{user_id}/homes/{home_id}", response_model=schemas.UserHomeRelation)
def delete_user_home_relation(user_id: str, home_id: str, db: Session = Depends(get_db)):
    """删除用户-房屋关联关系"""
    relation = crud.delete_user_home_relation(db, user_id=user_id, home_id=home_id)
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    return relation