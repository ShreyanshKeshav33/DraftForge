from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password



def get_all(db: Session):
    return db.query(User).all()

def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create(db: Session, payload: UserCreate):
    existing = db.query(User).filter(
        (User.email == payload.email) | (User.username == payload.username)).first()
    
    if existing:
        return None  # Email or username already exists
    user =User(
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password)
    )
    db.add(user)
    db.commit() 
    db.refresh(user)
    return user

def update(db: Session, user_id: int, payload: UserUpdate):
    user =db.query(User).filter(User.id==user_id).first()

    if not user:
        return None  # User not found

    if payload.email or payload.username:
        conflict = db.query(User).filter(
            ((User.email == payload.email) | (User.username == payload.username))
        ).first()
        if conflict:
            return "conflict"  # Email or username already exists for another user

    if payload.email is not None:
        user.email= payload.email
    if payload.username is not None:
        user.username= payload.username
    if payload.password is not None:
        user.hashed_password= hash_password(payload.password)
    db.commit()
    db.refresh(user)
    return user