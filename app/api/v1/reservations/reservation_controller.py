from fastapi import APIRouter, Depends
from app.core.config import Settings
from app.db.models.users.user import User
from app.dependency import get_current_user
from app.services.reservations.reservation_service import ReservationService

config = Settings()

router = APIRouter()
reservationService = ReservationService()


@router.get("/")
async def get_all_reservations():
    try:
        reservations = reservationService.get_all_reservations()

        return {"data": reservations}
    except Exception as e:
        return {"error": str(e)}


@router.get("/my-reservations")
async def get_my_reservations(current_user: User = Depends(get_current_user)):
    try:
        reservations = reservationService.get_reservations_by_user_id(current_user.id)

        return {"data": reservations}
    except Exception as e:
        return {"error": str(e)}


@router.get("/{reservation_id}")
async def find_reservation_by_id(reservation_id: str):
    try:
        reservation = reservationService.get_reservation_by_id(reservation_id)

        return {"data": reservation}
    except Exception as e:
        return {"error": str(e)}


@router.post("/")
async def create_reservation(current_user: User = Depends(get_current_user)):
    pass


@router.post("/pending")
async def create_pending_reservation(current_user: User = Depends(get_current_user)):
    pass


@router.put("/pending-to-confirmed/{reservation_id}")
async def pending_to_confirmed(reservation_id: int, current_user: User = Depends(get_current_user)):
    pass


@router.put("/{reservation_id}")
async def update_reservation(reservation_id: int, current_user: User = Depends(get_current_user)):
    pass


@router.delete("/{reservation_id}")
async def cancel_reservation(reservation_id: int, current_user: User = Depends(get_current_user)):
    pass
