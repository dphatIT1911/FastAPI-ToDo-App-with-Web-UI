from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models.todo import Todo

class ToDoRepository:
    """Repository quản lý ToDo theo User sở hữu."""
    
    def create(self, db: Session, title: str, owner_id: int, description: Optional[str] = None) -> Todo:
        """Tạo ToDo mới gán cho User ID cụ thể."""
        db_todo = Todo(title=title, description=description, owner_id=owner_id)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    
    def get_all(
        self,
        db: Session,
        owner_id: int,
        is_done: Optional[bool] = None,
        search_query: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[Todo], int]:
        """Lấy danh sách ToDo - CHỈ lấy của owner_id."""
        query = db.query(Todo).filter(Todo.owner_id == owner_id)
        
        if is_done is not None:
            query = query.filter(Todo.is_done == is_done)
        if search_query:
            query = query.filter(Todo.title.ilike(f"%{search_query}%"))
            
        total = query.count()
        
        if sort_by:
            if sort_by.startswith("-"):
                field_name = sort_by[1:]
                if hasattr(Todo, field_name):
                    query = query.order_by(desc(getattr(Todo, field_name)))
            else:
                if hasattr(Todo, sort_by):
                    query = query.order_by(asc(getattr(Todo, sort_by)))
                    
        query = query.offset(offset).limit(limit)
        return query.all(), total

    def get_by_id(self, db: Session, todo_id: int, owner_id: int) -> Optional[Todo]:
        """Lấy 1 ToDo theo ID và Owner."""
        return db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == owner_id).first()
        
    def update(
        self, 
        db: Session, 
        todo_id: int, 
        owner_id: int,
        title: Optional[str] = None, 
        description: Optional[str] = None,
        is_done: Optional[bool] = None
    ) -> Optional[Todo]:
        """Cập nhật ToDo - CHỈ cho phép nếu là chủ sở hữu."""
        db_todo = self.get_by_id(db, todo_id, owner_id)
        if not db_todo:
            return None
            
        if title is not None:
            db_todo.title = title
        if description is not None:
            db_todo.description = description
        if is_done is not None:
            db_todo.is_done = is_done
            
        db.commit()
        db.refresh(db_todo)
        return db_todo
        
    def delete(self, db: Session, todo_id: int, owner_id: int) -> bool:
        """Xoá ToDo - CHỈ cho phép nếu là chủ sở hữu."""
        db_todo = self.get_by_id(db, todo_id, owner_id)
        if not db_todo:
            return False
        db.delete(db_todo)
        db.commit()
        return True

todo_repository = ToDoRepository()
