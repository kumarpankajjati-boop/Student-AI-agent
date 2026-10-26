from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger import logger
from app.model import StudentModel
from app.schema import StudentOut

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=List[StudentOut])
def list_students(db: Session = Depends(get_db)):
    return db.query(StudentModel).order_by(StudentModel.id).all()


@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if student is None:
        logger.warning("GET student id=%s not found", student_id)
        raise HTTPException(status_code=404, detail="Student not found")
    return student
