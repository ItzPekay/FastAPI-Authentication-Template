from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserLogin
from ..models.user import User
from fastapi import HTTPException

from ..core import security as security
from ..core.tokens import create_access_token

def register(db: Session, payload: UserCreate):

    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(400, "Account already exists!")
    
    new_user = User(username = payload.username, password = security.hash_password(payload.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login(db: Session, payload: UserLogin):
    existingUser = db.query(User).filter(User.username == payload.username).first()
    if not existingUser:
        raise HTTPException(400, "Account not found!")
    if not security.compare_password(payload.password, existingUser.password):
        raise HTTPException(401, "Incorrect username or password!")
    
    token = create_access_token({"sub" : str(existingUser.id)})
    return {"access_token" : token, "token_type" : "bearer"}

    
    
    
