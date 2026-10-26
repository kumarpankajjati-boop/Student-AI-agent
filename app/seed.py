"""Sample students, inserted only when the table is empty."""
from app.database import SessionLocal
from app.logger import logger
from app.model import StudentModel

SAMPLE_STUDENTS = [
    {"student_name": "Rahul Sharma", "student_class": "10", "subject": "Maths", "student_section": "A", "age": 15},
    {"student_name": "Asha Verma", "student_class": "10", "subject": "Science", "student_section": "B", "age": 15},
    {"student_name": "Imran Khan", "student_class": "9", "subject": "English", "student_section": "A", "age": 14},
    {"student_name": "Priya Nair", "student_class": "11", "subject": "Physics", "student_section": "C", "age": 16},
    {"student_name": "Karan Singh", "student_class": "12", "subject": "Computer Science", "student_section": "A", "age": 17},
]


def seed_if_empty() -> int:
    db = SessionLocal()
    try:
        if db.query(StudentModel).count() > 0:
            return 0
        for row in SAMPLE_STUDENTS:
            db.add(StudentModel(**row))
        db.commit()
        logger.info("Seeded %d demo students", len(SAMPLE_STUDENTS))
        return len(SAMPLE_STUDENTS)
    finally:
        db.close()
