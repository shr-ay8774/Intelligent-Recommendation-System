from app.database.database import SessionLocal
from app.models.course import Course

from app.recommendation.preprocessing import prepare_courses
from app.recommendation.tfidf import create_tfidf_matrix
from app.recommendation.similarity import calculate_similarity


db = SessionLocal()

try:

    courses = db.query(Course).all()

    df = prepare_courses(courses)

    vectorizer, tfidf_matrix = create_tfidf_matrix(df)

    similarity_matrix = calculate_similarity(
        tfidf_matrix
    )

    print("Number of courses:", len(df))

    print(
        "Similarity matrix shape:",
        similarity_matrix.shape
    )

    print("\nSimilarity Matrix:")

    print(similarity_matrix)

finally:

    db.close()