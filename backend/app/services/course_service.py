from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course_schema import CourseCreate


def create_course(db: Session, course: CourseCreate):
    new_course = Course(
        title=course.title,
        description=course.description,
        difficulty=course.difficulty,
        duration=course.duration,
        category_id=course.category_id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


def get_courses(db: Session):
    return db.query(Course).all()


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def delete_course(db: Session, course_id: int):
    course = db.query(Course).filter(Course.id == course_id).first()

    if course:
        db.delete(course)
        db.commit()

    return course