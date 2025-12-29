from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate , UserOut, Token, UserLogin, LogoutRequest
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.redis_client import redis_client
from app.core.security import get_current_user



router = APIRouter()


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
	return current_user



@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
	# Check if user exists
	existing = db.query(User).filter(User.email == user_in.email).first()
	if existing:
		raise HTTPException(status_code=400, detail="Email already registred")

	# Hash password
	hashed_pw = hash_password(user_in.password)

	# Create user
	new_user = User(firstname=user_in.firstname, lastname=user_in.lastname, email=user_in.email, hashed_password=hashed_pw, is_active=False)
	db.add(new_user)
	db.commit()
	db.refresh(new_user)

	return new_user

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
	# Find user by email
	user = db.query(User).filter(User.email==user_in.email).first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid email or password",
		)

	# verify password
	if not verify_password(user_in.password, user.hashed_password):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
		)

	# Create JWT token
	access_token = create_access_token(data={"sub": str(user.id)})
	refresh_token = create_refresh_token(user.id)

	print("ACCESS_TOKEN::::", access_token)


	return {
		"user": user,
		"access_token": access_token,
		"refresh_token": refresh_token,
		"token_type": "bearer"
	}


@router.post("/refresh")
def refresh_token(refresh_token: str):
    user_id = verify_refresh_token(refresh_token)  # should return user id
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    access_token = create_access_token(data={"sub": str(user_id)})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.post("/logout")
def logout(data: LogoutRequest):
	refresh_token = data.refresh_token
	print("REFRESH TOKEN::::::::::::", refresh_token)

	deleted = redis_client.delete(f"refresh_token:{refresh_token}")
	if deleted == 0:
		raise HTTPException(status_code=400, detail="Invalid refresh token")

	return {"message": "Logged out successfully"}




