from sqlalchemy import Column, Integer, String

from app.database import Base


class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    student_class = Column(String)
    subject = Column(String)
    student_section = Column(String)
    age = Column(Integer)
