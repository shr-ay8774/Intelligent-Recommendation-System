from fastapi import FastAPI

from app.database.database import Base, engine

from app.models import *

from app.api.router import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intelligent Recommendation System"
)

app.include_router(api_router)


@app.get("/")
def home():
    return {
        "message": "Backend Running Successfully"
    }