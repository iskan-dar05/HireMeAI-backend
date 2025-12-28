from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.auth import router as auth_router
from app.routes.resume import router as resume_router
from app.routes.template import router as template_router
from fastapi.responses import Response
import os

app = FastAPI(title="HireMeAI API")

path = '/'

if os.path.exists(path) is False:
	os.makedirs(path)



origins = [
	"https://hire-me-ai-frontend.vercel.app",
	"http://127.0.0.1:8080"
]


app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

@app.options("/{path:path}")
async def options_handler(path: str, request: Request):
    return Response(status_code=200)

# include auth routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(resume_router, prefix="/resume", tags=["Resume"])
app.include_router(template_router, prefix="/template", tags=["Template"])

app.mount("/static", StaticFiles(directory=path), name="static")

@app.get("/")
def root():
	return {"message": "API is running"}


