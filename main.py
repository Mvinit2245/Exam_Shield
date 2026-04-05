from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routes import exam
from routes import auth
import models

# ✅ Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Exam Proctoring System")

# ✅ CORS (IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES
app.include_router(
    exam.router,
    prefix="/exam",
    tags=["Exam"]
)

app.include_router(
    auth.router,
    prefix="",   # 👈 IMPORTANT (keeps /login clean)
    tags=["Auth"]
)