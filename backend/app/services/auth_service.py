from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models.user import User
from app.auth.password import verify_password
from app.auth.jwt_handler import create_access_token


def login_user(
    db: Session,
    form_data: OAuth2PasswordRequestForm
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.password
    ):
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