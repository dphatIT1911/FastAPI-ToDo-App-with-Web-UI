from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.user import UserCreate, UserResponse, Token
from app.repositories.user_repository import user_repository

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate
) -> Any:
    """Đăng ký tài khoản người dùng mới."""
    user = user_repository.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email này đã được sử dụng.",
        )
    return user_repository.create(db, obj_in=user_in)

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Đăng nhập bằng form-data để lấy Access Token JWT."""
    user = user_repository.get_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Người dùng đã bị vô hiệu hóa")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: Any = Depends(deps.get_current_user)) -> Any:
    """Lấy thông tin của người dùng đang đăng nhập hiện tại."""
    return current_user
