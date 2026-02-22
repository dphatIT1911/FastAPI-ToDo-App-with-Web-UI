from typing import Optional
from fastapi import APIRouter, Query
from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoResponse, ToDoListResponse
from app.services.todo_service import todo_service


router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=ToDoResponse, status_code=201)
async def create_todo(todo: ToDoCreate):
    """
    Create a new ToDo item.
    
    - **title**: Title of the ToDo (3-100 characters, non-empty)
    """
    return todo_service.create_todo(todo)


@router.get("", response_model=ToDoListResponse)
async def get_todos(
    is_done: Optional[bool] = Query(None, description="Filter by completion status"),
    q: Optional[str] = Query(None, description="Search query for title"),
    sort: Optional[str] = Query(None, description="Sort by field (e.g., 'created_at' or '-created_at')"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip")
):
    """
    Get all ToDo items with optional filtering, searching, sorting, and pagination.
    
    - **is_done**: Filter by completion status (true/false)
    - **q**: Search keyword in title (case-insensitive)
    - **sort**: Sort by 'created_at' (ascending) or '-created_at' (descending)
    - **limit**: Number of items per page (1-1000)
    - **offset**: Number of items to skip (for pagination)
    """
    return todo_service.get_todos(
        is_done=is_done,
        search_query=q,
        sort_by=sort,
        limit=limit,
        offset=offset
    )


@router.get("/{todo_id}", response_model=ToDoResponse)
async def get_todo(todo_id: int):
    """
    Get a specific ToDo item by ID.
    
    - **todo_id**: The ID of the ToDo item
    """
    return todo_service.get_todo_by_id(todo_id)


@router.put("/{todo_id}", response_model=ToDoResponse)
async def update_todo(todo_id: int, todo: ToDoUpdate):
    """
    Update a ToDo item.
    
    - **todo_id**: The ID of the ToDo item
    - **title**: New title (optional, 3-100 characters if provided)
    - **is_done**: New completion status (optional)
    """
    return todo_service.update_todo(todo_id, todo)


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    """
    Delete a ToDo item.
    
    - **todo_id**: The ID of the ToDo item
    """
    return todo_service.delete_todo(todo_id)
