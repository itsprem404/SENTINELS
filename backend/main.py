from fastapi import FastAPI

from database.db import Base, engine
from database import models      
from api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Autonomous AI Creator",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Autonomous AI Creator is running 🚀"
    }
    