from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut, Token, LogoutRequest
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from app.core.redis_client import redis_client

router = APIRouter()


# =========================
# GET CURRENT USER
# =========================
@router.get("/me", response_model=UserOut)
def me(request: Request, db: Session = Depends(get_db)):
    auth = request.headers.get("Authorization")

    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = auth.replace("Bearer ", "")
    user = get_current_user(token, db)

    return user


# =========================
# REGISTER
# =========================
@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user_in.password)

    new_user = User(
        firstname=user_in.firstname,
        lastname=user_in.lastname,
        email=user_in.email,
        hashed_password=hashed_pw,
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
async def login(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Missing credentials")

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(user.id)

    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# =========================
# REFRESH TOKEN
# =========================
@router.post("/refresh")
def refresh_token(refresh_token: str):
    user_id = verify_refresh_token(refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(data={"sub": str(user_id)})

    return {
        "access_token": access_token,
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
