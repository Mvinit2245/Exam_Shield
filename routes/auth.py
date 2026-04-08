from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from auth import create_token

router = APIRouter()

# ================= REGISTER =================
@router.post("/register")
def register(data: schemas.RegisterUser, db: Session = Depends(get_db)):

    # check existing user
    user = db.query(models.User).filter(models.User.username == data.username).first()

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    new_user = models.User(
        name=data.name,
        username=data.username,
        email=data.email,
        mobile=data.mobile,
        password=data.password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


# ================= LOGIN =================
@router.post("/login")
def login(data: schemas.LoginUser, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == data.username).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token({"sub": user.username})

    return {
        "access_token": token,
        "user": {
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "mobile": user.mobile
        }
    }