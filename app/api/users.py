from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import hash_password
import app.crud.user as crud_user

router= APIRouter()

@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud_user.get_all(db)

@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user= crud_user.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = crud_user.create(db, payload)
    
    if not user:
        raise HTTPException(status_code=400, detail="Email or username already exists")
    return user 
    
@router.put("/users/{id}", response_model=UserResponse)
def update_user(id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user= crud_user.update(db, id, payload)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    if user=="conflict":
        raise HTTPException(status_code=400, detail="Email or username already exists for another user")
    return user