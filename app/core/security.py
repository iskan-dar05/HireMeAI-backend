from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.clerk_auth import verify_clerk_token



async def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.split(" ")[1]
    payload = await verify_clerk_token(token)

    print("PAYLOAD::::::::::", payload)

    user_id = payload["user_id"]


    # Find or create local user
    user = db.query(User).filter(User.id == user_id).first()

    print("USER USER USER========", user)

    if not user:
        user = User(
            id=user_id,
            email=payload["email"],
            firstname=payload["firstname"],
            lastname=payload["lastname"],
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
