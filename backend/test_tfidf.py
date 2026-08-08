from app.database.database import SessionLocal
from app.models.course import Course

from app.recommendation.preprocessing import prepare_courses
from app.recommendation.tfidf import create_tfidf_matrix


db = SessionLocal()

try:

    courses = db.query(Course).all()

    df = prepare_courses(courses)

    vectorizer, tfidf_matrix = create_tfidf_matrix(df)

    print("Number of courses:", len(df))

    print(
        "TF-IDF matrix shape:",
        tfidf_matrix.shape
    )

    print("\nVocabulary:")

    print(
        vectorizer.get_feature_names_out()
    )

finally:

    db.close()