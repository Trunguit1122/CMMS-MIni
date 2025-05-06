# app/api/profile.py

from fastapi import APIRouter, Depends
from app.deps.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/me")
def read_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "full_name": current_user.full_name
    }
