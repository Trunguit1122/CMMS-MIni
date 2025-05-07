from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.w_o import WorkOrder
from app.schemas.w_o import WorkOrderCreate, WorkOrderOut, WorkOrderUpdate
from app.deps.auth import get_current_user
from app.models.user import User
from app.models.asset import Asset

router =APIRouter(
    prefix="/work_order",
    tags=["Work Orders"],
    dependencies=[Depends(get_current_user)]
)
@router.post(
    "/",
    response_model=WorkOrderOut,
    status_code=status.HTTP_201_CREATED
)
def create_work_order(
    wo_in: WorkOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
 # Chỉ admin hoặc technician mới có quyền tạo
    if current_user.role not in {"admin", "technician"}:
        raise HTTPException(status_code=403, detail="Not enough privileges")

    # Đảm bảo Asset tồn tại và chưa bị xoá
    asset = (
        db.query(Asset)
          .filter(Asset.id == wo_in.asset_id, Asset.deleted_at.is_(None))
          .first()
    )
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Gán created_by tự động
    wo_output = WorkOrder(**wo_in.model_dump())
    wo_output.created_by = current_user.id
    # Nếu technician tự tạo mà chưa gán assigned_to → gán mình
    if current_user.role == "technician" and wo_output.assigned_to is None:
        wo_output.assigned_to = current_user.id

    db.add(wo_output)
    db.commit()
    db.refresh(wo_output)
    return wo_output