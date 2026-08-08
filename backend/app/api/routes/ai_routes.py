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

from app.recommendation.user_behavior import (
    get_user_behavior
)

from app.recommendation.hybrid import (
    calculate_hybrid_scores
)

from app.ai.genai_service import (
    explain_recommendations,
    generate_local_assistant_response,
    generate_local_course_explanation,
    generate_local_learning_plan,
    generate_local_quiz
)

from app.schemas.ai_schema import (
    AIRecommendationResponse,
    AssistantRequest,
    AssistantResponse,
    CourseExplanationResponse,
    LearningPlanRequest,
    LearningPlanResponse,
    QuizRequest,
    QuizResponse
)


router = APIRouter(
    prefix="/ai",
    tags=["GenAI"]
)


@router.get(
    "/recommendations/explain",
    response_model=AIRecommendationResponse
)
def explain_user_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    courses = db.query(Course).all()

    if not courses:
        return {
            "explanation": "No courses are currently available."
        }

    courses_df = prepare_courses(courses)

    behavior = get_user_behavior(
        db,
        current_user.id
    )

    content_recommendations = (
        get_personalized_recommendations(
            current_user,
            courses_df,
            top_n=len(courses_df)
        )
    )

    content_score_map = {
        row["id"]: row["score"]
        for _, row in content_recommendations.iterrows()
    }

    content_scores = courses_df["id"].map(
        content_score_map
    ).fillna(0)

    recommendations = calculate_hybrid_scores(
        courses_df,
        content_scores,
        behavior["ratings"],
        behavior["enrollments"],
        behavior["learning_history"]
    )

    recommendations = recommendations.head(5)

    recommendation_list = [
        {
            "id": int(row["id"]),
            "title": row["title"],
            "score": float(row["hybrid_score"])
        }
        for _, row in recommendations.iterrows()
    ]

    explanation = explain_recommendations(
        user_name=current_user.full_name,
        skill_level=current_user.skill_level or "",
        interests=current_user.interests or "",
        recommendations=recommendation_list
    )

    return {
        "explanation": explanation
    }


@router.post(
    "/assistant",
    response_model=AssistantResponse
)
def learning_assistant(
    request: AssistantRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    courses = db.query(Course).all()

    if not courses:
        return {
            "answer": (
                "There are currently no courses available."
            )
        }

    courses_df = prepare_courses(courses)

    behavior = get_user_behavior(
        db,
        current_user.id
    )

    content_recommendations = (
        get_personalized_recommendations(
            current_user,
            courses_df,
            top_n=len(courses_df)
        )
    )

    content_score_map = {
        row["id"]: row["score"]
        for _, row in content_recommendations.iterrows()
    }

    content_scores = courses_df["id"].map(
        content_score_map
    ).fillna(0)

    recommendations = calculate_hybrid_scores(
        courses_df,
        content_scores,
        behavior["ratings"],
        behavior["enrollments"],
        behavior["learning_history"]
    )

    recommendations = recommendations.head(5)

    recommendation_list = [
        {
            "id": int(row["id"]),
            "title": row["title"],
            "score": float(row["hybrid_score"])
        }
        for _, row in recommendations.iterrows()
    ]

    answer = generate_local_assistant_response(
        user_name=current_user.full_name,
        skill_level=current_user.skill_level or "",
        interests=current_user.interests or "",
        question=request.question,
        recommendations=recommendation_list
    )

    return {
        "answer": answer
    }


@router.get(
    "/courses/{course_id}/explain",
    response_model=CourseExplanationResponse
)
def explain_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:
        return {
            "course_id": course_id,
            "course_title": "Unknown",
            "explanation": "Course not found."
        }

    explanation = generate_local_course_explanation(
        user_name=current_user.full_name,
        skill_level=current_user.skill_level or "",
        interests=current_user.interests or "",
        course_title=course.title,
        course_description=course.description or ""
    )

    return {
        "course_id": course.id,
        "course_title": course.title,
        "explanation": explanation
    }
    
@router.post(
    "/learning-plan",
    response_model=LearningPlanResponse
)
def learning_plan(
    request: LearningPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    courses = db.query(Course).all()

    if not courses:
        return {
            "plan": "There are currently no courses available."
        }

    courses_df = prepare_courses(courses)

    behavior = get_user_behavior(
        db,
        current_user.id
    )

    content_recommendations = (
        get_personalized_recommendations(
            current_user,
            courses_df,
            top_n=len(courses_df)
        )
    )

    content_score_map = {
        row["id"]: row["score"]
        for _, row in content_recommendations.iterrows()
    }

    content_scores = courses_df["id"].map(
        content_score_map
    ).fillna(0)

    recommendations = calculate_hybrid_scores(
        courses_df,
        content_scores,
        behavior["ratings"],
        behavior["enrollments"],
        behavior["learning_history"]
    )

    recommendations = recommendations.head(5)

    recommendation_list = [
        {
            "id": int(row["id"]),
            "title": row["title"],
            "score": float(row["hybrid_score"])
        }
        for _, row in recommendations.iterrows()
    ]

    plan = generate_local_learning_plan(
        user_name=current_user.full_name,
        skill_level=current_user.skill_level or "",
        interests=current_user.interests or "",
        goal=request.goal,
        recommendations=recommendation_list
    )

    return {
        "plan": plan
    }
    
@router.post(
    "/quiz",
    response_model=QuizResponse
)
def generate_quiz(
    request: QuizRequest,
    current_user: User = Depends(get_current_user)
):

    questions = generate_local_quiz(
        topic=request.topic,
        number_of_questions=request.number_of_questions
    )

    return {
        "topic": request.topic,
        "questions": questions
    }