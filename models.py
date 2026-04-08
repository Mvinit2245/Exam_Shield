from sqlalchemy import Column, Integer, String
from database import Base


# ================= EXAM SESSION =================
class ExamSession(Base):

    __tablename__ = "exam_sessions"

    id = Column(Integer, primary_key=True, index=True)

    # student id
    student_id = Column(String, nullable=False, index=True)

    # ✅ ADD THIS (VERY IMPORTANT)
    user = Column(String)

    tab_switch_count = Column(Integer, default=0)
    face_not_detected_count = Column(Integer, default=0)
    multiple_face_count = Column(Integer, default=0)
    sound_detected_count = Column(Integer, default=0)


# ================= USER =================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String)
    mobile = Column(String)
    password = Column(String)