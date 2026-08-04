from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import create_user
from app.auth.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def register_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):
    return create_user(db, user)

@router.get("/me")
def current_user(
    user: User = Depends(get_current_user)
):
    return user