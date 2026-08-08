from app.database.database import SessionLocal
from app.models.user import User
from app.models.course import Course

from app.recommendation.preprocessing import prepare_courses
from app.recommendation.personalized import (
    get_personalized_recommendations
)


db = SessionLocal()

try:

    # Get a user
    user = db.query(User).first()

    if user is None:
        print("No users found.")
        exit()

    # Get courses
    courses = db.query(Course).all()

    if not courses:
        print("No courses found.")
        exit()

    # Convert courses to DataFrame
    courses_df = prepare_courses(courses)

    # Generate recommendations
    recommendations = (
        get_personalized_recommendations(
            user,
            courses_df,
            top_n=5
        )
    )

    print("User:")
    print("Name:", user.full_name)
    print("Skill Level:", user.skill_level)
    print("Interests:", user.interests)

    print("\nRecommended Courses:")

    print(
        recommendations[
            ["id", "title", "score"]
        ].to_string(index=False)
    )

finally:

    db.close()