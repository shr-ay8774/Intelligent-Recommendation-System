from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    id: int
    title: str
    score: float