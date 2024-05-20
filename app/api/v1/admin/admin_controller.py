from datetime import datetime

from fastapi import APIRouter, Depends
from app.core.config import Settings
from app.db.models.application.users.user import User
from app.dependency import has_admin_access
from app.services.admin.admin_service import AdminService

config = Settings()

router = APIRouter()
adminService = AdminService()


@router.get("/reservations/{start_date}/{end_date}")
async def get_reservations(start_date: datetime, end_date: datetime, current_user: User = Depends(has_admin_access)):
    try:
        reservations = await adminService.get_reservations_between_dates(start_date, end_date)

        return reservations
    except Exception as e:
        return {"error": str(e)}
