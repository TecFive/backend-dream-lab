from datetime import datetime

from fastapi import APIRouter, Depends
from app.core.config import Settings
from app.db.models.application.users.user import User
from app.dependency import has_admin_access
from app.services.admin.admin_service import AdminService

config = Settings()

router = APIRouter()
adminService = AdminService()


@router.get("/all-stats")
async def get_all_stats(current_user: User = Depends(has_admin_access)):
    daily_reservations = await adminService.get_daily_reservations()
    weekly_reserved_rooms = await adminService.get_weekly_reserved_rooms()
    monthly_reservations = await adminService.get_monthly_reserved_rooms()
    all_time_reservations = await adminService.get_all_time_reservations()
    reservations_per_month = await adminService.get_reservations_per_month()

    weekly_reserved_equipment = await adminService.get_weekly_reserved_equipment()
    monthly_reserved_equipment = await adminService.get_equipment_stats_monthly()
    equipment_stats_per_month = await adminService.get_equipment_stats_per_month()

    return {
        "daily_reservations": daily_reservations,
        "weekly_reserved_rooms": weekly_reserved_rooms,
        "monthly_reservations": monthly_reservations,
        "all_time_reservations": all_time_reservations,
        "reservations_per_month": reservations_per_month,
        "weekly_reserved_equipment": weekly_reserved_equipment,
        "monthly_reserved_equipment": monthly_reserved_equipment,
        "equipment_stats_per_month": equipment_stats_per_month
    }


@router.get("/reservations/selector/{start_date}/{end_date}")
async def get_reservations(start_date: datetime, end_date: datetime, current_user: User = Depends(has_admin_access)):
    try:
        reservations = await adminService.get_reservations_between_dates(start_date, end_date)
        return reservations
    except Exception as e:
        raise e


@router.get("/reservations/stats/daily")
async def get_daily_reservations(current_user: User = Depends(has_admin_access)):
    try:
        reservations = await adminService.get_daily_reservations()

        return reservations
    except Exception as e:
        raise e


@router.get("/reservations/stats/weekly")
async def get_all_time_reservations(current_user: User = Depends(has_admin_access)):
    try:
        reservations = await adminService.get_weekly_reservations()

        return reservations
    except Exception as e:
        raise e


@router.get("/reservations/stats/all-time")
async def get_all_time_reservations(current_user: User = Depends(has_admin_access)):
    try:
        reservations = await adminService.get_all_time_reservations()

        return reservations
    except Exception as e:
        raise e


@router.get("/reservations/stats/per-month")
async def get_reservations_per_month(current_user: User = Depends(has_admin_access)):
    try:
        reservations = await adminService.get_reservations_per_month()

        return reservations
    except Exception as e:
        raise e


@router.get("/reservations/stats/monthly")
async def get_monthly_reserved_rooms(current_user: User = Depends(has_admin_access)):
    try:
        room_stats = await adminService.get_monthly_reserved_rooms()

        return room_stats
    except Exception as e:
        raise e


@router.get("/rooms/stats/weekly")
async def get_weekly_reserved_rooms(current_user: User = Depends(has_admin_access)):
    try:
        room_stats = await adminService.get_weekly_reserved_rooms()

        return room_stats
    except Exception as e:
        raise e


@router.get("/equipment/stats/weekly")
async def get_weekly_reserved_equipment(current_user: User = Depends(has_admin_access)):
    try:
        equipment_stats = await adminService.get_weekly_reserved_equipment()

        return equipment_stats
    except Exception as e:
        raise e


@router.get("/equipment/stats/per-month")
async def get_equipment_stats_per_month(current_user: User = Depends(has_admin_access)):
    try:
        equipment_stats = await adminService.get_equipment_stats_per_month()

        return equipment_stats
    except Exception as e:
        raise e


@router.get("/equipment/stats/monthly")
async def get_equipment_stats_monthly(current_user: User = Depends(has_admin_access)):
    try:
        equipment_stats = await adminService.get_equipment_stats_monthly()

        return equipment_stats
    except Exception as e:
        raise e


@router.put("/reservations/status/{reservation_id}")
async def update_reservation_status(reservation_id: str, status: str, current_user: User = Depends(has_admin_access)):
    try:
        reservation = await adminService.update_reservation_status(reservation_id, status)

        return reservation
    except Exception as e:
        raise e
