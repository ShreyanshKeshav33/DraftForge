from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
import app.crud.document as crud_document

router = APIRouter()

@router.get("/documents", response_model=list[DocumentResponse])
def get_documents(user_id: int, db: Session = Depends(get_db)):
    return crud_document.get_all(db, user_id)

@router.get("/documents/{id}", response_model=DocumentResponse)
def get_document(id: int, user_id:int, db: Session = Depends(get_db)):
    document = crud_document.get_by_id(db, user_id, id)
    if not document:
        raise HTTPException(status_code=404, detail="document not found")
    return document

@router.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(user_id: int, payload: DocumentCreate, db: Session = Depends(get_db)):
    document = crud_document.create(db, user_id, payload)
    return document

@router.put("/documents/{id}", response_model=DocumentResponse)
def update_document(id: int, user_id:int, payload: DocumentUpdate, db: Session = Depends(get_db)):
    document = crud_document.update(db, id, user_id, payload)
    if not document:
        raise HTTPException(status_code=404, detail="document not found")
    return document

@router.delete("/documents/{id}")
def delete_document(id: int, user_id:int, db: Session = Depends(get_db)):
    document = crud_document.delete(db, user_id, id)
    if not document:
        raise HTTPException(status_code=404, detail="document not found")
    return Response(status_code=204)