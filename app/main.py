from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.api import api_router


# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    description="A simple ToDo list API with CRUD operations, filtering, sorting, and pagination",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Serve static files (for the web UI)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    pass  # Directory doesn't exist yet


# Level 0 Endpoints
@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - Welcome message.
    
    Level 0 requirement: GET / returns a greeting message.
    """
    return {
        "message": "Chào mừng đến với FastAPI ToDo API!",
        "description": "Sử dụng /docs để xem API documentation",
        "version": "1.0.0"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Level 0 requirement: GET /health returns {"status": "ok"}.
    """
    return {"status": "ok"}


# Include API v1 router with prefix
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
