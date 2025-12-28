from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut, Token, UserLogin, LogoutRequest
from app.schemas.token import RefreshTokenRequest
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from app.core.redis_client import redis_client

router = APIRouter()

# =========================
# REGISTER
# =========================
@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        firstname=user_in.firstname,
        lastname=user_in.lastname,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# =========================
# LOGIN
# =========================
@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {
        "user": user,
        "access_token": create_access_token({"sub": str(user.id)}),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


# =========================
# REFRESH TOKEN (FIXED)
# =========================
@router.post("/refresh")
def refresh_token(data: RefreshTokenRequest):
    user_id = verify_refresh_token(data.refresh_token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return {
        "access_token": create_access_token({"sub": str(user_id)}),
        "token_type": "bearer",
    }


# =========================
# LOGOUT
# =========================
@router.post("/logout")
def logout(data: LogoutRequest):
    deleted = redis_client.delete(f"refresh_token:{data.refresh_token}")

    if deleted == 0:
        raise HTTPException(status_code=400, detail="Invalid refresh token")

    return {"message": "Logged out successfully"}
