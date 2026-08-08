from app.database.database import SessionLocal

from app.models.user import User

from app.recommendation.user_behavior import (
    get_user_behavior
)


db = SessionLocal()

try:

    user = db.query(User).first()

    if user is None:
        print("No users found.")
        exit()

    behavior = get_user_behavior(
        db,
        user.id
    )

    print("User ID:", user.id)

    print(
        "\nRatings:",
        len(behavior["ratings"])
    )

    for rating in behavior["ratings"]:
        print(
            "Course:",
            rating.course_id,
            "Rating:",
            rating.rating
        )

    print(
        "\nEnrollments:",
        len(behavior["enrollments"])
    )

    for enrollment in behavior["enrollments"]:
        print(
            "Course:",
            enrollment.course_id
        )

    print(
        "\nLearning History:",
        len(behavior["learning_history"])
    )

    for history in behavior["learning_history"]:
        print(
            "Course:",
            history.course_id,
            "Progress:",
            history.progress
        )

finally:

    db.close()