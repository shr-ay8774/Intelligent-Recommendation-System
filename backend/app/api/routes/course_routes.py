from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.course_schema import CourseCreate, CourseResponse
from app.services.course_service import (
    create_course,
    get_courses,
    get_course,
    delete_course,
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post("/", response_model=CourseResponse)
def add_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db, course)


@router.get("/", response_model=list[CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    return get_courses(db)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    course = get_course(db, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@router.delete("/{course_id}")
def remove_course(course_id: int, db: Session = Depends(get_db)):
    course = delete_course(db, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return {"message": "Course deleted successfully"}