from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr]=None
    username: Optional[str]=None
    password: Optional[str]=None
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool

    model_config= {"from_attributes": True}    