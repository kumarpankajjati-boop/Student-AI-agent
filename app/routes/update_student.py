from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger import logger
from app.model import StudentModel
from app.schema import StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])


@router.put("/{student_id}")
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    # 1. Student identification: find the record by its unique ID
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if student is None:
        logger.warning("UPDATE student id=%s not found", student_id)
        raise HTTPException(status_code=404, detail="Student not found")

    # 2. Parameter selection: change only the fields the client actually sent
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(student, field, value)

    # 3. Commit changes
    db.commit()
    logger.info("UPDATE student id=%s fields=%s", student_id, list(changes))
    return {"status": "success", "message": f"Student {student_id} updated"}
