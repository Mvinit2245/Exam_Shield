from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from auth import create_token
from pydantic import BaseModel

router = APIRouter()

# ✅ REQUEST MODEL
class UserData(BaseModel):
    username: str
    password: str

# DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ REGISTER
@router.post("/register")
def register(data: UserData, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == data.username).first()

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = models.User(
        username=data.username,
        password=data.password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}

# ✅ LOGIN (FIXED)
@router.post("/login")
def login(data: UserData, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == data.username).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token({"sub": user.username})

    return {"access_token": token}