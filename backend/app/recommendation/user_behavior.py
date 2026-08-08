from sqlalchemy.orm import Session

from app.models.rating import Rating
from app.models.enrollment import Enrollment
from app.models.learning_history import LearningHistory


def get_user_behavior(
    db: Session,
    user_id: int
):
    ratings = (
        db.query(Rating)
        .filter(
            Rating.user_id == user_id
        )
        .all()
    )

    enrollments = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == user_id
        )
        .all()
    )

    learning_history = (
        db.query(LearningHistory)
        .filter(
            LearningHistory.user_id == user_id
        )
        .all()
    )

    return {
        "ratings": ratings,
        "enrollments": enrollments,
        "learning_history": learning_history
    }