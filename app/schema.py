from typing import Optional

from pydantic import BaseModel


class StudentCreate(BaseModel):
    # Mandatory fields: a missing or wrong-type value gives HTTP 422
    student_name: str
    student_class: str
    subject: str
    student_section: str
    age: int


class StudentUpdate(BaseModel):
    # Optional: the client sends only the fields it wants to change
    student_name: Optional[str] = None
    student_class: Optional[str] = None
    subject: Optional[str] = None
    student_section: Optional[str] = None
    age: Optional[int] = None


class StudentOut(BaseModel):
    id: int
    student_name: str
    student_class: str
    subject: str
    student_section: str
    age: int

    model_config = {"from_attributes": True}


class AIQuery(BaseModel):
    user_question: str
    # Same session_id = the agent remembers earlier questions (chat memory)
    session_id: Optional[str] = "default"
    # If empty, the API loads the records from the database itself
    db_records: Optional[str] = None
