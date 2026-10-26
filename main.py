import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app import model  # noqa: F401  (registers the students table with SQLAlchemy)
from app.config import settings
from app.database import Base, engine
from app.logger import logger
from app.routes.base import api_router
from app.seed import seed_if_empty


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Create the tables defined in model.py
    Base.metadata.create_all(bind=engine)
    if settings.seed_demo_data:
        seed_if_empty()
    logger.info("Server started | llm_provider=%s | database=%s", settings.llm_provider, settings.database_url)
    yield
    logger.info("Server stopped")


app = FastAPI(title="Student Management API with AI Agent", lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every API call with its status and how long it took (Day 2)."""
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("UNHANDLED ERROR | %s %s", request.method, request.url.path)
        raise
    ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s -> %s (%.0f ms)", request.method, request.url.path, response.status_code, ms)
    return response


app.include_router(api_router)


@app.get("/")
def read_root():
    return {
        "message": "Student Management API with AI Agent",
        "chat_page": "/chat",
        "swagger_docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "ok", "llm_provider": settings.llm_provider}
