from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.resume import router as resume_router
from app.routes.template import router as template_router

app = FastAPI(title="HireMeAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hire-me-ai-frontend.vercel.app",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(resume_router, prefix="/resume")
app.include_router(template_router, prefix="/template")

@app.get("/")
def root():
    return {"message": "API is running"}
