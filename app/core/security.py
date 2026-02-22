import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from app.core.config import settings

# Sử dụng trực tiếp thư viện bcrypt để tránh lỗi tương thích của passlib trên các bản Python mới
def get_password_hash(password: str) -> str:
    """Băm mật khẩu sử dụng bcrypt."""
    # Bcrypt yêu cầu dữ liệu dạng bytes
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu khớp với bản băm."""
    try:
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password_byte_enc = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)
    except Exception:
        return False

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """Tạo JWT Access Token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
