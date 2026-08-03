from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.auth.password import hash_password


def create_user(db: Session, user: UserCreate):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        skill_level=user.skill_level,
        interests=user.interests
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user