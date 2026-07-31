from sqlalchemy import Column, Integer, String
from app.database.database import Base


class RecommendationCache(Base):
    __tablename__ = "recommendation_cache"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    recommendations = Column(String)