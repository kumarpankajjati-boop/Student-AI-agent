from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger import logger
from app.model import StudentModel
from app.schema import StudentCreate

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    record = StudentModel(**student.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    logger.info("CREATE student id=%s name=%r", record.id, record.student_name)
    return {"status": "success", "id": record.id}
