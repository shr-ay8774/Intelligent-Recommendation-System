from fastapi import APIRouter

from app.api.routes import (
    user_routes,
    category_routes,
    course_routes,
    auth_routes,
    recommendation_routes,
    ai_routes
)


api_router = APIRouter()


api_router.include_router(user_routes.router)
api_router.include_router(category_routes.router)
api_router.include_router(course_routes.router)
api_router.include_router(auth_routes.router)
api_router.include_router(recommendation_routes.router)
api_router.include_router(ai_routes.router)