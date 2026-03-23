from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..schemas.user import UserCreate, UserLogin
from ..models.user import User
from ..models.refresh_token import RefreshToken
from ..core import security
from ..core.tokens import create_access_token, create_refresh_token
from ..config import REFRESH_TOKEN_EXPIRE_DAYS


def register(db: Session, payload: UserCreate):
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(400, "Account already exists!")

    new_user = User(
        username=payload.username,
        password=security.hash_password(payload.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login(db: Session, payload: UserLogin):
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if not existing_user:
        raise HTTPException(400, "Invalid credentials!")
    if not security.compare_password(payload.password, existing_user.password):
        raise HTTPException(401, "Invalid credentials!")

    access_token = create_access_token({"sub": str(existing_user.id)})

    raw_refresh = create_refresh_token()
    db_refresh = RefreshToken(
        token=raw_refresh,
        user_id=existing_user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(db_refresh)
    db.commit()

    return {"access_token": access_token, "refresh_token": raw_refresh, "token_type": "bearer"}


def refresh(db: Session, refresh_token: str):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.now(timezone.utc),
    ).first()

    if not db_token:
        raise HTTPException(401, "Invalid or expired refresh token!")

    # Rotate: revoke the used token, issue a new one
    db_token.revoked = True

    new_raw = create_refresh_token()
    new_db_token = RefreshToken(
        token=new_raw,
        user_id=db_token.user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(new_db_token)
    db.commit()

    access_token = create_access_token({"sub": str(db_token.user_id)})
    return {"access_token": access_token, "refresh_token": new_raw, "token_type": "bearer"}


def logout(db: Session, refresh_token: str):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.revoked == False,
    ).first()

    if not db_token:
        raise HTTPException(401, "Invalid refresh token!")

    db_token.revoked = True
    db.commit()
