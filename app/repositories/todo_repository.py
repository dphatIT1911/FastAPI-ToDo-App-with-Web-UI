from typing import List, Optional, Tuple, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models.todo import Todo
from app.schemas.todo import ToDoCreate, ToDoUpdate

class ToDoRepository:
    """Repository quản lý ToDo tương tác với CSDL SQLite qua SQLAlchemy."""
    
    def create(self, db: Session, title: str, description: Optional[str] = None) -> Todo:
        """Tạo một ToDo item mới."""
        db_todo = Todo(title=title, description=description)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    
    def get_all(
        self,
        db: Session,
        is_done: Optional[bool] = None,
        search_query: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[Todo], int]:
        """
        Lấy tất cả ToDo items có hỗ trợ lọc, tìm kiếm, sắp xếp và phân trang thực sự ở DB.
        """
        query = db.query(Todo)
        
        # Lọc theo is_done
        if is_done is not None:
            query = query.filter(Todo.is_done == is_done)
            
        # Tìm kiếm trong tiêu đề
        if search_query:
            query = query.filter(Todo.title.ilike(f"%{search_query}%"))
            
        # Tổng số lượng bản ghi (không tính phân trang)
        total = query.count()
        
        # Sắp xếp
        if sort_by:
            if sort_by.startswith("-"):
                field_name = sort_by[1:]
                if hasattr(Todo, field_name):
                    query = query.order_by(desc(getattr(Todo, field_name)))
            else:
                if hasattr(Todo, sort_by):
                    query = query.order_by(asc(getattr(Todo, sort_by)))
                    
        # Phân trang
        query = query.offset(offset).limit(limit)
        
        return query.all(), total

    def get_by_id(self, db: Session, todo_id: int) -> Optional[Todo]:
        """Lấy một ToDo theo ID."""
        return db.query(Todo).filter(Todo.id == todo_id).first()
        
    def update(
        self, 
        db: Session, 
        todo_id: int, 
        title: Optional[str] = None, 
        description: Optional[str] = None,
        is_done: Optional[bool] = None
    ) -> Optional[Todo]:
        """Cập nhật một ToDo item."""
        db_todo = self.get_by_id(db, todo_id)
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
        
    def delete(self, db: Session, todo_id: int) -> bool:
        """Xoá một ToDo item."""
        db_todo = self.get_by_id(db, todo_id)
        if not db_todo:
            return False
            
        db.delete(db_todo)
        db.commit()
        return True

# Khởi tạo repository instance dùng chung
todo_repository = ToDoRepository()
