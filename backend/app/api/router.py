from fastapi import APIRouter

from app.api.routes import (
    user_routes,
    category_routes,
    course_routes,
)

api_router = APIRouter()

api_router.include_router(user_routes.router)
api_router.include_router(category_routes.router)
api_router.include_router(course_routes.router)