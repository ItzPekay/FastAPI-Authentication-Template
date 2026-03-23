from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..schemas.user import UserCreate, UserLogin, UserResponse
from ..schemas.auth import Token, RefreshRequest
from ..dependencies import get_db
from ..services import auth_service
from ..core.limiter import register_limiter, login_limiter


router = APIRouter()



@router.post('/register', response_model=UserResponse)
def register(request: Request, payload: UserCreate, db: Session = Depends(get_db), _: None = Depends(register_limiter)):
    return auth_service.register(db, payload)


@router.post('/login', response_model=Token)
def login(request: Request, payload: UserLogin, db: Session = Depends(get_db), _: None = Depends(login_limiter)):
    return auth_service.login(db, payload)


@router.post('/refresh', response_model=Token)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    return auth_service.refresh(db, payload.refresh_token)


@router.post('/logout', status_code=204)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    auth_service.logout(db, payload.refresh_token)
