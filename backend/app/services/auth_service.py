from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth_schema import LoginRequest
from app.auth.password import verify_password
from app.auth.jwt_handler import create_access_token


def login_user(db: Session, login: LoginRequest):

    user = db.query(User).filter(
        User.email == login.email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(login.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": user.email,
            "id": user.id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }