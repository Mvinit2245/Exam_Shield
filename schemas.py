from pydantic import BaseModel
from typing import Optional


class StartExam(BaseModel):
    student_id: str


class Event(BaseModel):
    event_type: str


class FaceDetection(BaseModel):
    face_count: int
    look_direction: str | None = None   # NEW
    
from pydantic import BaseModel

class RegisterUser(BaseModel):
    name: str
    username: str
    email: str
    mobile: str
    password: str
    confirm_password: str


class LoginUser(BaseModel):
    username: str
    password: str