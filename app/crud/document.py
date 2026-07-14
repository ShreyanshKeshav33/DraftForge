from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate


def get_all(db: Session, user_id: int):
    return db.query(Document).filter(Document.user_id==user_id).all()

def get_by_id(db: Session, document_id: int):
    return db.query(Document).filter(Document.id == document_id).first()

def create(db: Session, user_id:int, payload: DocumentCreate):
    document = Document(
        title=payload.title,
        content=payload.content,
        user_id=user_id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

def update(db: Session, document_id: int, payload: DocumentUpdate):
    document =db.query(Document).filter(Document.id==document_id).first()

    if not document:
        return None #no doc found
    
    if payload.title is not None:
        document.title=payload.title
    if payload.content is not None:
        document.content=payload.content 

    db.commit()
    db.refresh(document)
    return document       

    

def delete(db: Session, document_id:int):
    document= db.query(Document).filter(Document.id==document_id).first()
    if not document:
        return None
    db.delete(document)
    db.commit()
    return True