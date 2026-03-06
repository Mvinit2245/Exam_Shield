from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routes import exam
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Exam Proctoring System")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    exam.router,
    prefix="/exam",
    tags=["Exam"]
)