from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime

from app.database.database import Base


class RecommendationCache(Base):
    __tablename__ = "recommendation_cache"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    recommendations = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )