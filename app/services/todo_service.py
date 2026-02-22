from typing import Optional, Dict, Any
from fastapi import HTTPException
from app.repositories.todo_repository import todo_repository
from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoResponse, ToDoListResponse


class ToDoService:
    """Service layer for ToDo business logic."""
    
    def __init__(self):
        """Initialize the service with the repository."""
        self.repository = todo_repository
    
    def create_todo(self, todo_data: ToDoCreate) -> ToDoResponse:
        """Create a new ToDo item."""
        todo = self.repository.create(title=todo_data.title)
        return ToDoResponse(**todo)
    
    def get_todos(
        self,
        is_done: Optional[bool] = None,
        search_query: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> ToDoListResponse:
        """Get all ToDo items with filtering, searching, sorting, and pagination."""
        todos, total = self.repository.get_all(
            is_done=is_done,
            search_query=search_query,
            sort_by=sort_by,
            limit=limit,
            offset=offset
        )
        
        items = [ToDoResponse(**todo) for todo in todos]
        
        return ToDoListResponse(
            items=items,
            total=total,
            limit=limit,
            offset=offset
        )
    
    def get_todo_by_id(self, todo_id: int) -> ToDoResponse:
        """Get a ToDo item by ID."""
        todo = self.repository.get_by_id(todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail=f"ToDo with id {todo_id} not found")
        return ToDoResponse(**todo)
    
    def update_todo(self, todo_id: int, todo_data: ToDoUpdate) -> ToDoResponse:
        """Update a ToDo item."""
        # Check if todo exists
        existing_todo = self.repository.get_by_id(todo_id)
        if existing_todo is None:
            raise HTTPException(status_code=404, detail=f"ToDo with id {todo_id} not found")
        
        # Update the todo
        updated_todo = self.repository.update(
            todo_id=todo_id,
            title=todo_data.title,
            is_done=todo_data.is_done
        )
        
        return ToDoResponse(**updated_todo)
    
    def delete_todo(self, todo_id: int) -> Dict[str, str]:
        """Delete a ToDo item."""
        success = self.repository.delete(todo_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"ToDo with id {todo_id} not found")
        return {"message": f"ToDo with id {todo_id} deleted successfully"}


# Global service instance
todo_service = ToDoService()
