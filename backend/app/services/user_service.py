from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate


def create_user(db: Session, user: UserCreate):
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=user.password,
        skill_level=user.skill_level,
        interests=user.interests,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user