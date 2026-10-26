from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.logger import logger
from app.model import StudentModel
from app.schema import AIQuery
from app.services.llm_service import LLMUnavailable, ask_ai, reset_memory

router = APIRouter(tags=["AI Agent"])


def build_records_text(db: Session) -> str:
    rows = db.query(StudentModel).order_by(StudentModel.id).all()
    if not rows:
        return "No student records found."
    lines = [f"Total students: {len(rows)}"]
    for s in rows:
        lines.append(
            f"ID {s.id}: {s.student_name}, class {s.student_class}, "
            f"section {s.student_section}, subject {s.subject}, age {s.age}"
        )
    return "\n".join(lines)


@router.post("/query-ai")
def query_ai(body: AIQuery, db: Session = Depends(get_db)):
    session_id = body.session_id or "default"
    records = body.db_records or build_records_text(db)
    logger.info("AI query | provider=%s | session=%s | question=%r",
                settings.llm_provider, session_id, body.user_question)
    try:
        answer = ask_ai(body.user_question, records, session_id)
    except LLMUnavailable as exc:
        logger.error("AI query failed | %s", exc)
        raise HTTPException(status_code=503, detail=str(exc))
    logger.info("AI answer | session=%s | chars=%d", session_id, len(answer))
    return {"status": "success", "response": answer, "session_id": session_id}


@router.post("/reset-memory/{session_id}")
def clear_memory(session_id: str):
    reset_memory(session_id)
    logger.info("Memory cleared | session=%s", session_id)
    return {"status": "success", "message": f"Memory cleared for {session_id}"}
