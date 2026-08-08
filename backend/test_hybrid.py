from app.database.database import SessionLocal

from app.models.user import User
from app.models.course import Course

from app.recommendation.preprocessing import prepare_courses
from app.recommendation.personalized import (
    get_personalized_recommendations
)

from app.recommendation.user_behavior import (
    get_user_behavior
)

from app.recommendation.hybrid import (
    calculate_hybrid_scores
)


db = SessionLocal()

try:

    user = db.query(User).first()

    if user is None:
        print("No user found.")
        exit()

    courses = db.query(Course).all()

    if not courses:
        print("No courses found.")
        exit()

    # Prepare courses
    courses_df = prepare_courses(courses)

    # Get user behavior
    behavior = get_user_behavior(
        db,
        user.id
    )

    # Get content recommendations
    content_recommendations = (
        get_personalized_recommendations(
            user,
            courses_df,
            top_n=len(courses_df)
        )
    )

    # Create content score map
    content_score_map = {
        row["id"]: row["score"]
        for _, row in content_recommendations.iterrows()
    }

    # Apply content scores to all courses
    content_scores = courses_df["id"].map(
        content_score_map
    ).fillna(0)

    # Calculate hybrid scores
    recommendations = calculate_hybrid_scores(
        courses_df,
        content_scores,
        behavior["ratings"],
        behavior["enrollments"],
        behavior["learning_history"]
    )

    print("\nUser:")
    print("ID:", user.id)
    print("Name:", user.full_name)
    print("Interests:", user.interests)

    print("\nHybrid Recommendations:")

    print(
        recommendations[
            [
                "id",
                "title",
                "content_score",
                "rating_score",
                "enrollment_score",
                "progress_score",
                "hybrid_score"
            ]
        ].to_string(index=False)
    )

finally:

    db.close()