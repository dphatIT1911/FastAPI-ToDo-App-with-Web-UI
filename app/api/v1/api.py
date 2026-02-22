from fastapi import APIRouter
from app.api.v1.routers import todos


api_router = APIRouter()

# Include all routers
api_router.include_router(todos.router)
