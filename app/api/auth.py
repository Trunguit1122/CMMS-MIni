# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginIn, TokenOut, RegisterIn, UserOut
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

router = APIRouter()

# 🔐 LOGIN
@router.post("/auth/login", response_model=TokenOut)
def login(login_data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


# 🔏 REGISTER (tạm mở public – sau này chỉ admin dùng)
@router.post("/auth/register", response_model=UserOut)
def register(register_data: RegisterIn, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == register_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(register_data.password)
    new_user = User(
        username=register_data.username,
        full_name=register_data.full_name,
        password_hash=hashed_pw,
        role=register_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
