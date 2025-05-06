# app/models/work_order.py
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Enum, func
)
from sqlalchemy.orm import relationship
from app.database import Base

# ------------------------ Enum khai báo ------------------------
class WOStatus(str, PyEnum):
    open        = "open"
    in_progress = "in_progress"
    done        = "done"
    canceled    = "canceled"

class WOPriority(str, PyEnum):
    low    = "low"
    medium = "medium"
    high   = "high"

# ------------------------ ORM WorkOrder ------------------------
class WorkOrder(Base):
    __tablename__ = "work_orders"

    # ----- PRIMARY KEY -----
    id = Column(Integer, primary_key=True, index=True)

    # ----- KHÓA NGOẠI / THÔNG TIN LIÊN KẾT -----
    asset_id     = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    assigned_to  = Column(Integer, ForeignKey("users.id"), nullable=True)   # kỹ thuật viên phụ trách
    created_by   = Column(Integer, ForeignKey("users.id"), nullable=True)   # người tạo WO

    # ----- TRƯỜNG NỘI DUNG -----
    title        = Column(String(100), nullable=False)
    description  = Column(Text)

    status       = Column(Enum(WOStatus), nullable=False, default=WOStatus.open)
    priority     = Column(Enum(WOPriority), nullable=False, default=WOPriority.medium)

    # ----- MỐC THỜI GIAN -----
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    started_at   = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # ----- QUAN HỆ ORM (giúp truy vấn thuận tiện) -----
    asset        = relationship("Asset", lazy="joined")
    technician   = relationship("User", foreign_keys=[assigned_to], lazy="joined")
    creator      = relationship("User", foreign_keys=[created_by], lazy="joined")


    