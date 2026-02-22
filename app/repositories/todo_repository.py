from typing import List, Optional, Dict, Any
from datetime import datetime


class ToDoRepository:
    """Repository for managing ToDo items in memory."""
    
    def __init__(self):
        """Initialize the in-memory storage."""
        self._todos: List[Dict[str, Any]] = []
        self._next_id: int = 1
    
    def create(self, title: str, is_done: bool = False) -> Dict[str, Any]:
        """Create a new ToDo item."""
        todo = {
            "id": self._next_id,
            "title": title,
            "is_done": is_done,
            "created_at": datetime.now()
        }
        self._todos.append(todo)
        self._next_id += 1
        return todo
    
    def get_all(
        self,
        is_done: Optional[bool] = None,
        search_query: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[List[Dict[str, Any]], int]:
        """
        Get all ToDo items with optional filtering, searching, sorting, and pagination.
        
        Args:
            is_done: Filter by completion status
            search_query: Search in title (case-insensitive)
            sort_by: Sort by field (created_at or -created_at for descending)
            limit: Maximum number of items to return
            offset: Number of items to skip
            
        Returns:
            Tuple of (filtered_todos, total_count)
        """
        # Start with all todos
        filtered_todos = self._todos.copy()
        
        # Filter by is_done
        if is_done is not None:
            filtered_todos = [todo for todo in filtered_todos if todo["is_done"] == is_done]
        
        # Search in title
        if search_query:
            search_lower = search_query.lower()
            filtered_todos = [
                todo for todo in filtered_todos 
                if search_lower in todo["title"].lower()
            ]
        
        # Get total count before pagination
        total = len(filtered_todos)
        
        # Sort
        if sort_by:
            reverse = False
            sort_field = sort_by
            
            if sort_by.startswith('-'):
                reverse = True
                sort_field = sort_by[1:]
            
            if sort_field == "created_at":
                filtered_todos.sort(key=lambda x: x["created_at"], reverse=reverse)
        
        # Pagination
        filtered_todos = filtered_todos[offset:offset + limit]
        
        return filtered_todos, total
    
    def get_by_id(self, todo_id: int) -> Optional[Dict[str, Any]]:
        """Get a ToDo item by ID."""
        for todo in self._todos:
            if todo["id"] == todo_id:
                return todo
        return None
    
    def update(self, todo_id: int, title: Optional[str] = None, is_done: Optional[bool] = None) -> Optional[Dict[str, Any]]:
        """Update a ToDo item."""
        todo = self.get_by_id(todo_id)
        if todo is None:
            return None
        
        if title is not None:
            todo["title"] = title
        if is_done is not None:
            todo["is_done"] = is_done
        
        return todo
    
    def delete(self, todo_id: int) -> bool:
        """Delete a ToDo item by ID."""
        for i, todo in enumerate(self._todos):
            if todo["id"] == todo_id:
                self._todos.pop(i)
                return True
        return False


# Global repository instance
todo_repository = ToDoRepository()
