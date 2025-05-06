from pydantic import BaseModel
from typing import Optional 

class AssetBase(BaseModel):
    name: str
    code: str
    location: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = "normal"
    qr_url: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetOut(AssetBase):
    id: int
    created_at: str
    

    class Config:
        orm_mode = True

class AssetUpdate(BaseModel):
    name:        Optional[str] = None
    code:        Optional[str] = None          # vẫn cho đổi mã nếu cần
    status:      Optional[str] = None
    description: Optional[str] = None
    # … thêm field nào bạn dùng trong DB

    class Config:
        from_attributes = True            