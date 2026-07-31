from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    skill_level: str
    interests: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    skill_level: str
    interests: str

    class Config:
        from_attributes = True