from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.review import router as review_router

app = FastAPI(
    title="AI Code Quality Gate",
    version="1.0.0"
)

# 🔥 CORS CONFIG (UPDATED FOR VERCEL + LOCAL)
origins = [
    # Local development
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",

    # Production frontend (Vercel)
    "https://ai-based-code-quality-and-security.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # must match exactly
    allow_credentials=True,
    allow_methods=["*"],          # allows POST, OPTIONS (preflight)
    allow_headers=["*"],
)

# API routes
app.include_router(review_router, prefix="/api/v1")

# Health check
@app.get("/")
def root():
    return {"status": "AI Code Quality Gate is running"}
