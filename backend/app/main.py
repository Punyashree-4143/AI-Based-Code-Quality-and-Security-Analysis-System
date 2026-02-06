from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.review import router as review_router

app = FastAPI(
    title="AI Code Quality Gate",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:5173",   # local frontend
    "https://ai-code-quality-gate.onrender.com"  # backend itself (safe)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "AI Code Quality Gate is running"}
