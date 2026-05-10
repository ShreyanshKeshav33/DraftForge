from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import hash_password

router= APIRouter()

@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users= db.query(User).all()
    return users

@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user= db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(
        (User.email == payload.email) | (User.username == payload.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email or username already exists")    
    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
@router.put("/users/{id}", response_model=UserResponse)
def update_user(id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user= db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if payload.email is not None:
        user.email= payload.email
    if payload.username is not None:
        user.username= payload.username
    if payload.password is not None:
        user.hashed_password= hash_password(payload.password)

    db.commit()
    db.refresh(user)
    return user