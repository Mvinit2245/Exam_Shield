from pydantic import BaseModel


class StartExam(BaseModel):
    student_id: str


class Event(BaseModel):
    event_type: str


class FaceDetection(BaseModel):
    face_count: int