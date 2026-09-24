from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.core.auth import get_current_user
import app.crud.document as crud_document

router = APIRouter()

@router.get("/documents", response_model=list[DocumentResponse])
def get_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_document.get_all(db, current_user.id)

@router.get("/documents/{id}", response_model=DocumentResponse)
def get_document(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = crud_document.get_by_id(db, current_user.id, id)
    if not document:
        raise HTTPException(status_code=404, detail="document not found")
    return document

@router.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(payload: DocumentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = crud_document.create(db, current_user.id, payload)
    return document

@router.put("/documents/{id}", response_model=DocumentResponse)
def update_document(id: int, payload: DocumentUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = crud_document.update(db, id, current_user.id, payload)
    if not document:
        raise HTTPException(status_code=404, detail="document not found")
    return document

@router.delete("/documents/{id}")
def delete_document(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = crud_document.delete(db, current_user.id, id)
    if not document:
        raise HTTPException(status_code=404, detail="document not found")
    return Response(status_code=204)