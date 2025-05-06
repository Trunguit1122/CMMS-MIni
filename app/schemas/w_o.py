# app/schemas/work_order.py

from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

from pydantic import BaseModel, Field

# Import enum từ model để đồng nhất
from app.models.w_o import WOStatus, WOPriority

# ── Schema cơ bản chung (shared) ───────────────────────────────────────────
class WorkOrderBase(BaseModel):
    asset_id    : int                            
    title       : str                            
    description : Optional[str]                  
    status      : Optional[WOStatus]             
    assigned_to : Optional[int]                  
    priority    : Optional[WOPriority]          
    class Config:
        from_attributes = True   # Cho phép validate/serialize từ ORM object

# ── Schema dùng khi **tạo mới** WorkOrder (POST) ───────────────────────────
class WorkOrderCreate(WorkOrderBase):
    # Khi tạo mới, bắt buộc phải có asset_id, title; các field khác optional
    status      : WOStatus        = Field(WOStatus.open, description="Mặc định mở")
    priority    : WOPriority      = Field(WOPriority.medium, description="Mặc định trung bình")

# ── Schema dùng khi **cập nhật** WorkOrder (PUT/PATCH) ────────────────────
class WorkOrderUpdate(BaseModel):
    title       : Optional[str]        = Field(None, max_length=100, description="Tiêu đề mới")
    description : Optional[str]        = Field(None, description="Mô tả mới")
    status      : Optional[WOStatus]   = Field(None, description="Trạng thái mới")
    assigned_to : Optional[int]        = Field(None, description="Gán technician mới")
    priority    : Optional[WOPriority] = Field(None, description="Độ ưu tiên mới")

    class Config:
        from_attributes = True   # Cần để có thể khởi tạo từ ORM cho partial update

# ── Schema trả về cho client (response_model) ─────────────────────────────
class WorkOrderOut(WorkOrderBase):
    id            : int                  = Field(..., description="PK của WorkOrder")
    created_by    : Optional[int]        = Field(None, description="ID user đã tạo")
    created_at    : datetime             = Field(..., description="Thời gian tạo")
    started_at    : Optional[datetime]   = Field(None, description="Thời gian bắt đầu xử lý")
    completed_at  : Optional[datetime]   = Field(None, description="Thời gian hoàn thành")

    class Config:
        from_attributes = True   # Bật khi serialize từ ORM → JSON
