from app.database.database import SessionLocal

from app.models.user import User
from app.models.course import Course
from app.models.rating import Rating
from app.models.enrollment import Enrollment
from app.models.learning_history import LearningHistory


db = SessionLocal()

try:
    user = db.query(User).first()
    courses = db.query(Course).all()

    if user is None:
        print("No user found.")
        exit()

    if len(courses) < 2:
        print("You need at least 2 courses.")
        exit()

    course_1 = courses[0]
    course_2 = courses[1]

    # Enrollments
    db.add_all([
        Enrollment(
            user_id=user.id,
            course_id=course_1.id
        ),
        Enrollment(
            user_id=user.id,
            course_id=course_2.id
        )
    ])

    # Ratings
    db.add_all([
        Rating(
            user_id=user.id,
            course_id=course_1.id,
            rating=5
        ),
        Rating(
            user_id=user.id,
            course_id=course_2.id,
            rating=4
        )
    ])

    # Learning history
    db.add_all([
        LearningHistory(
            user_id=user.id,
            course_id=course_1.id,
            progress=80
        ),
        LearningHistory(
            user_id=user.id,
            course_id=course_2.id,
            progress=40
        )
    ])

    db.commit()

    print("Test behavior data added successfully.")

finally:
    db.close()