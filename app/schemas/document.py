from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    title: str
    content: Optional[str]

class DocumentUpdate(BaseModel):
    
    title: Optional[str]=None
    content: Optional[str]=None
    
class DocumentResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config= {"from_attributes": True} 