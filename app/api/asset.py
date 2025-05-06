# routers/assets.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.asset import Asset
from app.models.user import User
from app.schemas.asset import AssetCreate, AssetOut, AssetUpdate
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
    dependencies=[Depends(get_current_user)]  
)

# ---------- POST /assets/ ----------
@router.post(
    "/",                                   
    response_model=AssetOut,
    status_code=status.HTTP_201_CREATED
)
def create_asset(
    asset_in: AssetCreate,                   
    db: Session = Depends(get_db),
):
    # Kiểm tra trùng mã thiết bị
    if db.query(Asset).filter(Asset.code == asset_in.code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Asset code already exists"
        )

    new_asset = Asset(**asset_in.model_dump())  # ✅ dùng asset_in
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset

# ---------- GET /assets/ ----------
@router.get("/",
 response_model=list[AssetOut])
def read_assets(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Trả về danh sách thiết bị, có phân trang đơn giản."""
    return (
        db.query(Asset)
        .offset(skip)
        .limit(limit)
        .all()
    )

# ---------- GET /assets/{asset_id} ----------
@router.get("/{asset_id}", response_model=AssetOut)
def read_asset(
    asset_id: int,
    db: Session = Depends(get_db),
):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    return asset

#router patch /assets/{asset_id}
@router.put("/{asset_id}", response_model=AssetOut)
def update_asset(
    asset_id: int,
    asset_in: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # cần lấy user
):
    # 1. Tìm asset
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # 2. Nếu user không đủ quyền ➞ 403 (ví dụ chỉ admin mới sửa)
    #    (Tùy dự án: bạn có thể bỏ chặn này)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough privileges")

    # 3. Nếu mã thiết bị thay đổi ➞ kiểm trùng
    if asset_in.code and asset_in.code != asset.code:
        if db.query(Asset).filter(Asset.code == asset_in.code).first():
            raise HTTPException(status_code=400, detail="Asset code already exists")

    # 4. Cập nhật field (chỉ những gì client gửi)
    asset_data = asset_in.model_dump(exclude_unset=True)
    for field, value in asset_data.items():
        setattr(asset, field, value)

    db.commit()
    db.refresh(asset)
    return asset