from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    location = Column(String(100))
    type = Column(String(50))
    qr_url = Column(Text)
    status = Column(String(20), default="normal")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
