from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

from auth import verify_token

router = APIRouter()


# ================= START EXAM =================
@router.post("/start_exam")
def start_exam(
    data: schemas.StartExam,
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)   # ✅ ADD THIS
):
    
    

    if not data.student_id:
        raise HTTPException(status_code=400, detail="student_id required")

       # ✅ DEBUG

    session = models.ExamSession(
        student_id=data.student_id,
        user=user   # ✅ STORE USER
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id,
        "student_id": session.student_id,
        "user": user   # ✅ OPTIONAL (for testing)
    }


# ================= EVENT =================
@router.post("/event/{session_id}")
def log_event(
    session_id: int,
    data: schemas.Event,
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)   # ✅ PROTECT
):

    session = db.query(models.ExamSession).filter(
        models.ExamSession.id == session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if data.event_type == "TAB_SWITCH":
        session.tab_switch_count += 1

    elif data.event_type == "NOISE":
        session.sound_detected_count += 1

    db.commit()

    return {"message": "event counted"}


# ================= FACE =================
@router.post("/face_detection/{session_id}")
def face_detection(
    session_id: int,
    data: schemas.FaceDetection,
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)   # ✅ PROTECT
):

    session = db.query(models.ExamSession).filter(
        models.ExamSession.id == session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if data.face_count == 0:
        session.face_not_detected_count += 1

    elif data.face_count > 1:
        session.multiple_face_count += 1

    db.commit()

    return {
        "face_count": data.face_count
    }


# ================= REPORT =================
@router.get("/report/{session_id}")
def report(
    session_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)   # ✅ PROTECT
):

    session = db.query(models.ExamSession).filter(
        models.ExamSession.id == session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "student_id": session.student_id,
        "user": session.user,   # ✅ SHOW USER
        "tab_switch_count": session.tab_switch_count,
        "face_not_detected_count": session.face_not_detected_count,
        "multiple_face_count": session.multiple_face_count,
        "sound_detected_count": session.sound_detected_count
    }
    
@router.get("/admin/all_sessions")
def get_all_sessions(
    db: Session = Depends(get_db),
    user: str = Depends(verify_token)
):
    sessions = db.query(models.ExamSession).all()

    result = []

    for s in sessions:
        result.append({
            "id": s.id,
            "student_id": s.student_id,
            "user": s.user,
            "tab_switch_count": s.tab_switch_count,
            "face_not_detected_count": s.face_not_detected_count,
            "multiple_face_count": s.multiple_face_count,
            "sound_detected_count": s.sound_detected_count
        })

    return result

