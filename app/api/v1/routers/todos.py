from typing import Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoResponse, ToDoListResponse
from app.services.todo_service import todo_service
from app.api.deps import get_db

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=ToDoResponse, status_code=201)
async def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)):
    """
    Tạo một ToDo item mới.
    
    - **title**: Tiêu đề của ToDo (3-100 ký tự, không được để trống)
    - **description**: Mô tả chi tiết (không bắt buộc)
    """
    return todo_service.create_todo(db, todo)


@router.get("", response_model=ToDoListResponse)
async def get_todos(
    is_done: Optional[bool] = Query(None, description="Lọc theo trạng thái hoàn thành"),
    q: Optional[str] = Query(None, description="Từ khóa tìm kiếm trong tiêu đề"),
    sort: Optional[str] = Query(None, description="Sắp xếp theo trường (vd: 'created_at' hoặc '-created_at')"),
    limit: int = Query(100, ge=1, le=1000, description="Số lượng kết quả trả về tối đa"),
    offset: int = Query(0, ge=0, description="Vị trí bắt đầu (để phân trang)"),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách ToDo items hỗ trợ lọc, tìm kiếm, sắp xếp và phân trang trực tiếp từ CSDL.
    """
    return todo_service.get_todos(
        db=db,
        is_done=is_done,
        search_query=q,
        sort_by=sort,
        limit=limit,
        offset=offset
    )


@router.get("/{todo_id}", response_model=ToDoResponse)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết của một ToDo bằng ID."""
    return todo_service.get_todo_by_id(db, todo_id)


@router.put("/{todo_id}", response_model=ToDoResponse)
async def update_todo(todo_id: int, todo: ToDoUpdate, db: Session = Depends(get_db)):
    """
    Cập nhật toàn bộ thông tin một ToDo item.
    """
    return todo_service.update_todo(db, todo_id, todo)


@router.patch("/{todo_id}", response_model=ToDoResponse)
async def partial_update_todo(todo_id: int, todo: ToDoUpdate, db: Session = Depends(get_db)):
    """
    Cập nhật một phần ToDo item (vd: chỉ cập nhật `is_done`).
    """
    return todo_service.update_todo(db, todo_id, todo)


@router.post("/{todo_id}/complete", response_model=ToDoResponse)
async def complete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Đánh dấu một ToDo item là đã hoàn thành nhanh chóng."""
    return todo_service.complete_todo(db, todo_id)


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Xóa một ToDo item khỏi CSDL."""
    return todo_service.delete_todo(db, todo_id)
