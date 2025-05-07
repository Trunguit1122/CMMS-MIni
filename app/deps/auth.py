"""
Dependency: get_current_user  &  get_current_admin
Giúp bảo vệ các route cần đăng nhập / phân quyền.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app.models.user import User
from app.core.jwt import SECRET_KEY, ALGORITHM   # đã định nghĩa ở app/core/jwt.py

# 1️  Khai báo “nguồn” token: header  Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 2️  Hàm decode & kiểm tra token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# 3️  Dependency: lấy người dùng hiện hành
def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
    ) -> User:
    payload = decode_token(token)
    
    # Kiểm tra hạn (exp) thủ công để có thông báo rõ ràng hơn
    exp_ts = payload.get("exp")
    if exp_ts and datetime.now(timezone.utc).timestamp() > exp_ts:
        raise HTTPException(status_code=401, detail="Token expired")

    username: str | None = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Token missing subject")

    user: User | None = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user          # → route sẽ nhận object User ORM

# 4️  Dependency: chỉ cho admin
def get_current_admin(
        user: User = Depends(get_current_user)
    ) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
