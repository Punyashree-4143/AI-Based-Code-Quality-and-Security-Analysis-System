from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.review import router as review_router

app = FastAPI(
    title="AI Code Quality Gate",
    version="1.0.0"
)

# 🔥 CORS FIX
origins = [
    "http://localhost:5173",
    "http://localhost:5174",   # 👈 ADD THIS
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # 👈 must match exactly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "AI Code Quality Gate is running"}
