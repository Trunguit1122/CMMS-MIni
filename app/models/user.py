from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)      # NEW
    role = Column(String, nullable=False)  # 'technician', 'admin'...
    is_on_duty = Column(Boolean, default=False)
    created_at =Column