from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserLogin
from ..schemas.auth import Token
from ..dependencies import get_db
from ..services import auth_service

router = APIRouter()

@router.post('/register')
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register(db, payload)

@router.post('/login', response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login(db, payload)
