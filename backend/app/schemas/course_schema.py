from pydantic import BaseModel, ConfigDict


class CourseCreate(BaseModel):
    title: str
    description: str
    difficulty: str
    duration: float
    category_id: int


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    duration: float
    rating: float
    category_id: int

    model_config = ConfigDict(from_attributes=True)