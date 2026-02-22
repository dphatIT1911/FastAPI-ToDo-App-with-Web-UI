from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class ToDoBase(BaseModel):
    """Base schema for ToDo with common properties."""
    title: str = Field(..., min_length=3, max_length=100, description="Title of the ToDo item")
    description: Optional[str] = Field(None, max_length=500, description="Detailed description of the ToDo item")
    is_done: bool = Field(default=False, description="Whether the ToDo is completed")


class ToDoCreate(BaseModel):
    """Schema for creating a new ToDo item."""
    title: str = Field(..., min_length=3, max_length=100, description="Title of the ToDo item")
    description: Optional[str] = Field(None, max_length=500, description="Detailed description of the ToDo item")
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate that title is not empty after stripping whitespace."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()


class ToDoUpdate(BaseModel):
    """Schema for updating an existing ToDo item."""
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="Title of the ToDo item")
    description: Optional[str] = Field(None, max_length=500, description="Detailed description of the ToDo item")
    is_done: Optional[bool] = Field(None, description="Whether the ToDo is completed")
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate that title is not empty after stripping whitespace."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Title cannot be empty')
            return v.strip()
        return v


class ToDoResponse(BaseModel):
    """Schema for ToDo response with all properties."""
    id: int = Field(..., description="Unique identifier of the ToDo item")
    title: str = Field(..., description="Title of the ToDo item")
    description: Optional[str] = Field(None, description="Detailed description of the ToDo item")
    is_done: bool = Field(..., description="Whether the ToDo is completed")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True


class ToDoListResponse(BaseModel):
    """Schema for paginated list of ToDo items."""
    items: List[ToDoResponse] = Field(..., description="List of ToDo items")
    total: int = Field(..., description="Total number of items")
    limit: int = Field(..., description="Number of items per page")
    offset: int = Field(..., description="Number of items to skip")

