from sqlalchemy import Column, Integer, ForeignKey, Float
from app.database.database import Base


class LearningHistory(Base):
    __tablename__ = "learning_history"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    course_id = Column(Integer, ForeignKey("courses.id"))

    progress = Column(Float, default=0)