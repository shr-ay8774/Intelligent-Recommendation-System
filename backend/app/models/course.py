from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)

    description = Column(String(1000))

    difficulty = Column(String(50))

    duration = Column(Float)

    rating = Column(Float, default=0)

    category_id = Column(Integer, ForeignKey("categories.id"))