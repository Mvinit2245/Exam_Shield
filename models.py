from sqlalchemy import Column, Integer, String
from database import Base


class ExamSession(Base):

    __tablename__ = "exam_sessions"

    id = Column(Integer, primary_key=True, index=True)

    # mandatory student id
    student_id = Column(String, nullable=False, index=True)

    tab_switch_count = Column(Integer, default=0)

    face_not_detected_count = Column(Integer, default=0)

    multiple_face_count = Column(Integer, default=0)

    sound_detected_count = Column(Integer, default=0)