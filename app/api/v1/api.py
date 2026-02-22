from fastapi import APIRouter
from app.api.v1.routers import todos, auth

api_router = APIRouter()
api_router.include_router(todos.router)
api_router.include_router(auth.router)
