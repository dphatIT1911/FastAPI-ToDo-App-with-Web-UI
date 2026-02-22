from typing import Optional, Dict
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.todo_repository import todo_repository
from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoResponse, ToDoListResponse

class ToDoService:
    """Service layer xử lý logic nghiệp vụ cho ToDo."""
    
    def __init__(self):
        self.repository = todo_repository
    
    def create_todo(self, db: Session, todo_data: ToDoCreate) -> ToDoResponse:
        """Tạo ToDo item mới."""
        todo = self.repository.create(db, title=todo_data.title, description=todo_data.description)
        return ToDoResponse.model_validate(todo)
    
    def get_todos(
        self,
        db: Session,
        is_done: Optional[bool] = None,
        search_query: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> ToDoListResponse:
        """Danh sách ToDo kèm filter, sort và pagination."""
        todos, total = self.repository.get_all(
            db,
            is_done=is_done,
            search_query=search_query,
            sort_by=sort_by,
            limit=limit,
            offset=offset
        )
        
        items = [ToDoResponse.model_validate(todo) for todo in todos]
        
        return ToDoListResponse(
            items=items,
            total=total,
            limit=limit,
            offset=offset
        )
    
    def get_todo_by_id(self, db: Session, todo_id: int) -> ToDoResponse:
        """Lấy ToDo bằng ID."""
        todo = self.repository.get_by_id(db, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy ToDo với id {todo_id}")
        return ToDoResponse.model_validate(todo)
    
    def update_todo(self, db: Session, todo_id: int, todo_data: ToDoUpdate) -> ToDoResponse:
        """Cập nhật toàn bộ/một phần ToDo."""
        existing_todo = self.repository.get_by_id(db, todo_id)
        if existing_todo is None:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy ToDo với id {todo_id}")
            
        updated_todo = self.repository.update(
            db,
            todo_id=todo_id,
            title=todo_data.title,
            description=todo_data.description,
            is_done=todo_data.is_done
        )
        return ToDoResponse.model_validate(updated_todo)
        
    def complete_todo(self, db: Session, todo_id: int) -> ToDoResponse:
        """Đánh dấu hoàn thành ToDo."""
        existing_todo = self.repository.get_by_id(db, todo_id)
        if existing_todo is None:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy ToDo với id {todo_id}")
            
        updated_todo = self.repository.update(db, todo_id=todo_id, is_done=True)
        return ToDoResponse.model_validate(updated_todo)
    
    def delete_todo(self, db: Session, todo_id: int) -> Dict[str, str]:
        """Xoá ToDo."""
        success = self.repository.delete(db, todo_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy ToDo với id {todo_id}")
        return {"message": f"Đã xoá thành công ToDo với id {todo_id}"}

todo_service = ToDoService()
