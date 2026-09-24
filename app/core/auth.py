from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.security import decode_access_token

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(get_db),
                     ) -> User:
                    payload = decode_access_token(token)
                    if payload is None:
                            raise HTTPException(status_code=401, detail="Invalid or expired token")

                    email=payload.get("sub")
                    if email is None:
                            raise HTTPException(status_code=401, detail="Invalid token payload")


                    user = db.query(User).filter(User.email==email).first()
                    if user is None:
                            raise HTTPException(status_code=401, detail="User not found")


                    return user