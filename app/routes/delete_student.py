from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger import logger
from app.model import StudentModel

router = APIRouter(prefix="/students", tags=["Students"])


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if student is None:
        logger.warning("DELETE student id=%s not found", student_id)
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    logger.info("DELETE student id=%s", student_id)
    return {"status": "success", "message": f"Student {student_id} deleted"}
