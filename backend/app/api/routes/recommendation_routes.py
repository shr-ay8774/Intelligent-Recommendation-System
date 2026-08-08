from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.user import User
from app.models.course import Course

from app.auth.auth import get_current_user

from app.recommendation.preprocessing import prepare_courses
from app.recommendation.personalized import (
    get_personalized_recommendations
)

from app.services.recommendation_cache_service import (
    get_cached_recommendations,
    save_recommendations_to_cache
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.get("/")
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Check cache first
    cached = get_cached_recommendations(
        db,
        current_user.id
    )

    if cached is not None:

        return {
            "source": "cache",
            "recommendations": cached
        }

    # Get courses
    courses = db.query(Course).all()

    if not courses:

        return {
            "source": "database",
            "recommendations": []
        }

    # Prepare course data
    courses_df = prepare_courses(courses)

    # Generate recommendations
    recommendations = (
        get_personalized_recommendations(
            current_user,
            courses_df,
            top_n=5
        )
    )

    recommendation_list = [
        {
            "id": int(row["id"]),
            "title": row["title"],
            "score": float(row["score"])
        }
        for _, row in recommendations.iterrows()
    ]

    # Save recommendations
    save_recommendations_to_cache(
        db,
        current_user.id,
        recommendation_list
    )

    return {
        "source": "generated",
        "recommendations": recommendation_list
    }