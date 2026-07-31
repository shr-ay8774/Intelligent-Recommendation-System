from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    course_id = Column(Integer, ForeignKey("courses.id"))

    rating = Column(Float)