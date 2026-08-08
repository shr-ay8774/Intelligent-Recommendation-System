from app.database.database import SessionLocal
from app.models.course import Course

from app.recommendation.preprocessing import prepare_courses


db = SessionLocal()

try:

    courses = db.query(Course).all()

    print("Number of courses:", len(courses))

    df = prepare_courses(courses)

    print("\nCourse Data:")
    print(df)

finally:

    db.close()