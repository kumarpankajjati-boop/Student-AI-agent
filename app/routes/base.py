"""Router registry (Day 7 'base.py'): main.py only has to include this one router."""
from fastapi import APIRouter

from app.routes import (
    ai_query,
    chat_page,
    create_student,
    delete_student,
    get_student,
    update_student,
)

api_router = APIRouter()
api_router.include_router(create_student.router)
api_router.include_router(get_student.router)
api_router.include_router(update_student.router)
api_router.include_router(delete_student.router)
api_router.include_router(ai_query.router)
api_router.include_router(chat_page.router)
