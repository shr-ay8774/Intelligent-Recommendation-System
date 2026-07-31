from fastapi import FastAPI

from app.database.database import Base, engine

from app.models import *

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent Recommendation System")


@app.get("/")
def home():
    return {"message": "Backend Running Successfully"}