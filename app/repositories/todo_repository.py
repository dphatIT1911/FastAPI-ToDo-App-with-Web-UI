from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from datetime import datetime, timezone, date
from app.models.todo import Todo

class ToDoRepository:
    """Repository quản lý ToDo theo User sở hữu."""
    
    def create(self, db: Session, title: str, owner_id: int, description: Optional[str] = None, due_date: Optional[datetime] = None, tags: Optional[List[str]] = None) -> Todo:
        """Tạo ToDo mới gán cho User ID cụ thể."""
        if tags is None:
            tags = []
        db_todo = Todo(title=title, description=description, owner_id=owner_id, due_date=due_date, tags=tags)
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
        is_done: Optional[bool] = None,
        due_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None
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
        if due_date is not None:
            db_todo.due_date = due_date
        if tags is not None:
            db_todo.tags = tags
            
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

    def get_overdue(self, db: Session, owner_id: int, limit: int = 100, offset: int = 0) -> Tuple[List[Todo], int]:
        """Lấy các công việc đã quá hạn và chưa hoàn thành."""
        now = datetime.now(timezone.utc)
        query = db.query(Todo).filter(Todo.owner_id == owner_id, Todo.is_done == False, Todo.due_date < now)
        total = query.count()
        query = query.order_by(asc(Todo.due_date)).offset(offset).limit(limit)
        return query.all(), total

    def get_today(self, db: Session, owner_id: int, limit: int = 100, offset: int = 0) -> Tuple[List[Todo], int]:
        """Lấy các công việc có deadline trong hôm nay."""
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start.replace(hour=23, minute=59, second=59, microsecond=999999)
        query = db.query(Todo).filter(Todo.owner_id == owner_id, Todo.due_date >= today_start, Todo.due_date <= today_end)
        total = query.count()
        query = query.order_by(asc(Todo.due_date)).offset(offset).limit(limit)
        return query.all(), total

todo_repository = ToDoRepository()
