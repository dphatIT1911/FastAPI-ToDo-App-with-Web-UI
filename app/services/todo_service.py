from typing import Optional, Dict
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.todo_repository import todo_repository
from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoResponse, ToDoListResponse

class ToDoService:
    """Service layer xử lý logic ToDo gắn liền với User."""
    
    def __init__(self):
        self.repository = todo_repository
    
    def create_todo(self, db: Session, todo_data: ToDoCreate, owner_id: int) -> ToDoResponse:
        todo = self.repository.create(db, title=todo_data.title, description=todo_data.description, owner_id=owner_id, due_date=todo_data.due_date, tags=todo_data.tags)
        return ToDoResponse.model_validate(todo)
    
    def get_todos(
        self,
        db: Session,
        owner_id: int,
        is_done: Optional[bool] = None,
        search_query: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> ToDoListResponse:
        todos, total = self.repository.get_all(
            db, owner_id=owner_id, is_done=is_done, search_query=search_query, 
            sort_by=sort_by, limit=limit, offset=offset
        )
        items = [ToDoResponse.model_validate(todo) for todo in todos]
        return ToDoListResponse(items=items, total=total, limit=limit, offset=offset)
    
    def get_todo_by_id(self, db: Session, todo_id: int, owner_id: int) -> ToDoResponse:
        todo = self.repository.get_by_id(db, todo_id, owner_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy ToDo hoặc bạn không có quyền.")
        return ToDoResponse.model_validate(todo)
    
    def update_todo(self, db: Session, todo_id: int, todo_data: ToDoUpdate, owner_id: int) -> ToDoResponse:
        updated_todo = self.repository.update(
            db, todo_id=todo_id, owner_id=owner_id,
            title=todo_data.title, description=todo_data.description, is_done=todo_data.is_done, due_date=todo_data.due_date, tags=todo_data.tags
        )
        if not updated_todo:
            raise HTTPException(status_code=404, detail="Không tìm thấy ToDo hoặc bạn không có quyền.")
        return ToDoResponse.model_validate(updated_todo)
        
    def complete_todo(self, db: Session, todo_id: int, owner_id: int) -> ToDoResponse:
        updated_todo = self.repository.update(db, todo_id=todo_id, owner_id=owner_id, is_done=True)
        if not updated_todo:
            raise HTTPException(status_code=404, detail="Không tìm thấy ToDo hoặc bạn không có quyền.")
        return ToDoResponse.model_validate(updated_todo)
    
    def delete_todo(self, db: Session, todo_id: int, owner_id: int) -> Dict[str, str]:
        success = self.repository.delete(db, todo_id, owner_id)
        if not success:
            raise HTTPException(status_code=404, detail="Không tìm thấy ToDo hoặc bạn không có quyền.")
        return {"message": f"Đã xoá thành công ToDo với id {todo_id}"}
    
    def get_overdue_todos(self, db: Session, owner_id: int, limit: int = 100, offset: int = 0) -> ToDoListResponse:
        todos, total = self.repository.get_overdue(db, owner_id=owner_id, limit=limit, offset=offset)
        items = [ToDoResponse.model_validate(todo) for todo in todos]
        return ToDoListResponse(items=items, total=total, limit=limit, offset=offset)

    def get_today_todos(self, db: Session, owner_id: int, limit: int = 100, offset: int = 0) -> ToDoListResponse:
        todos, total = self.repository.get_today(db, owner_id=owner_id, limit=limit, offset=offset)
        items = [ToDoResponse.model_validate(todo) for todo in todos]
        return ToDoListResponse(items=items, total=total, limit=limit, offset=offset)

todo_service = ToDoService()
