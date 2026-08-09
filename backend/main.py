import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import Base, engine
from database import models  # noqa: F401
from api.routes import router
from scheduler.scheduler import start_scheduler, stop_scheduler

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(
    title="SENTINELS — Autonomous AI Persona",
    version="2.0.0",
    description="Autonomous research, editorial judgment, memory and simulated publishing.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def home():
    return {
        "service": "SENTINELS",
        "status": "running",
        "autonomy": "research -> editorial gate -> memory -> publish",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
