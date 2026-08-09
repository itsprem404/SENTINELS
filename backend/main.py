from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from database import models      
from api.routes import router
from scheduler.scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Autonomous AI Creator",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

start_scheduler()

@app.get("/")
def home():
    return {
        "message": "Autonomous AI Creator is running 🚀"
    }
    