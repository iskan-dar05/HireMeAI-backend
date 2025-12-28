from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from app.routes.auth import router as auth_router
from app.routes.resume import router as resume_router
from app.routes.template import router as template_router
import os

app = FastAPI(title="HireMeAI API")

path = '/'
if os.path.exists(path) is False:
    os.makedirs(path)

origins = [
    "https://hire-me-ai-frontend.vercel.app",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
    expose_headers=["*"],
    max_age=86400,
)

# Global exception handler to add CORS headers to all responses
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    origin = request.headers.get("origin", "")
    allowed_origin = origin if origin in origins else origins[0] if origins else "*"
    
    # Handle preflight OPTIONS requests
    if request.method == "OPTIONS":
        return JSONResponse(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": allowed_origin,
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
                "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, Origin, X-Requested-With",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "86400",
            }
        )
    
    try:
        response = await call_next(request)
    except HTTPException as exc:
        # Handle FastAPI HTTPExceptions with CORS headers
        response = JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers={
                "Access-Control-Allow-Origin": allowed_origin,
                "Access-Control-Allow-Credentials": "true",
                **exc.headers,
            }
        )
    except Exception:
        # Handle other exceptions
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
            headers={
                "Access-Control-Allow-Origin": allowed_origin,
                "Access-Control-Allow-Credentials": "true",
            }
        )
    
    # Add CORS headers to successful responses
    if "access-control-allow-origin" not in response.headers:
        response.headers["Access-Control-Allow-Origin"] = allowed_origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
    
    return response

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(resume_router, prefix="/resume", tags=["Resume"])
app.include_router(template_router, prefix="/template", tags=["Template"])

app.mount("/static", StaticFiles(directory=path), name="static")

@app.get("/")
def root():
    return {"message": "API is running"}