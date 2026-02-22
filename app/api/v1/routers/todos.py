from typing import Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoResponse, ToDoListResponse
from app.services.todo_service import todo_service
from app.api import deps
from app.models.user import User

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("", response_model=ToDoResponse, status_code=201)
async def create_todo(
    todo: ToDoCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Tạo ToDo mới gắn với tài khoản đang đăng nhập."""
    return todo_service.create_todo(db, todo, owner_id=current_user.id)


@router.get("", response_model=ToDoListResponse)
async def get_todos(
    is_done: Optional[bool] = Query(None),
    q: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Lấy danh sách ToDo - CHỈ hiện thị dữ liệu của User hiện tại."""
    return todo_service.get_todos(
        db=db, owner_id=current_user.id, is_done=is_done, search_query=q, 
        sort_by=sort, limit=limit, offset=offset
    )


@router.get("/{todo_id}", response_model=ToDoResponse)
async def get_todo(
    todo_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return todo_service.get_todo_by_id(db, todo_id, owner_id=current_user.id)


@router.put("/{todo_id}", response_model=ToDoResponse)
async def update_todo(
    todo_id: int, 
    todo: ToDoUpdate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return todo_service.update_todo(db, todo_id, todo, owner_id=current_user.id)


@router.patch("/{todo_id}", response_model=ToDoResponse)
async def partial_update_todo(
    todo_id: int, 
    todo: ToDoUpdate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return todo_service.update_todo(db, todo_id, todo, owner_id=current_user.id)


@router.post("/{todo_id}/complete", response_model=ToDoResponse)
async def complete_todo(
    todo_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return todo_service.complete_todo(db, todo_id, owner_id=current_user.id)


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return todo_service.delete_todo(db, todo_id, owner_id=current_user.id)
