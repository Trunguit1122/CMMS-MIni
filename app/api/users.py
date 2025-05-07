from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserIn, UserOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/check-in", response_model=UserOut)
def check_in(user_in: UserIn, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        # Nếu đã có, cập nhật trạng thái trực
        existing_user.is_on_duty = True
        db.commit()
        db.refresh(existing_user)
        return existing_user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/users/check-out", response_model=UserOut)
def check_out(user_in: UserIn, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_in.username).first()

    if existing_user and existing_user.is_on_duty:
        existing_user.is_on_duty = False
        db.commit()
        db.refresh(existing_user)
        return existing_user
    else:
        raise HTTPException(status_code=404, detail="User not found or not check-in yet")

