from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Chat page"])

CHAT_HTML = Path(__file__).resolve().parent.parent / "static" / "chat.html"


@router.get("/chat", response_class=HTMLResponse)
def chat_page():
    return HTMLResponse(CHAT_HTML.read_text(encoding="utf-8"))
