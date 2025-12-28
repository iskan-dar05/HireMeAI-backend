from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.auth import router as auth_router
from app.routes.resume import router as resume_router
from app.routes.template import router as template_router
from fastapi.responses import Response
import os

app = FastAPI(title="HireMeAI API")  # Only ONE app declaration

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
    max_age=86400,  # 24 hours in seconds
)

# Add a middleware to handle OPTIONS requests BEFORE routing
@app.middleware("http")
async def handle_options_requests(request: Request, call_next):
    if request.method == "OPTIONS":
        # Create a preflight response
        origin = request.headers.get("origin", "")
        
        # Check if origin is allowed
        allowed_origin = origin if origin in origins else origins[0] if origins else "*"
        
        response = Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": allowed_origin,
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
                "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, Origin, X-Requested-With",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "86400",
                "Access-Control-Expose-Headers": "*",
            }
        )
        return response
    
    # For non-OPTIONS requests, proceed normally
    response = await call_next(request)
    
    # Add CORS headers to all responses
    origin = request.headers.get("origin", "")
    allowed_origin = origin if origin in origins else origins[0] if origins else "*"
    
    if "access-control-allow-origin" not in response.headers:
        response.headers["Access-Control-Allow-Origin"] = allowed_origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
    
    return response

# Remove or comment out your existing @app.options("/{path:path}") handler
# as it might conflict with the middleware above

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(resume_router, prefix="/resume", tags=["Resume"])
app.include_router(template_router, prefix="/template", tags=["Template"])

app.mount("/static", StaticFiles(directory=path), name="static")

@app.get("/")
def root():
    return {"message": "API is running"}