from fastapi import APIRouter, Depends
from app.core.config import Settings
from app.db.models.users.user import User
from app.dependency import get_current_user
from app.dtos.pendingReservations.create_pending_reservation_dto import CreatePendingReservationDto
from app.dtos.reservations.create_reservation_dto import CreateReservationDto
from app.services.pendingReservations.pending_reservation_service import PendingReservationService
from app.services.reservations.reservation_service import ReservationService

config = Settings()

router = APIRouter()
reservationService = ReservationService()
pendingReservationService = PendingReservationService()


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
async def create_reservation(create_reservation_dto: CreateReservationDto, current_user: User = Depends(get_current_user)):
    try:
        reservationService.create_reservation(create_reservation_dto)

        return {"data": "Reservation created successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.post("/pending")
async def create_pending_reservation(create_pending_reservation_dto: CreatePendingReservationDto, current_user: User = Depends(get_current_user)):
    try:
        pendingReservationService.create_pending_reservation(create_pending_reservation_dto, current_user.id)

        return {"data": "Pending reservation created successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.put("/pending-to-confirmed/{reservation_id}")
async def pending_to_confirmed(pending_reservation_id: str):
    try:
        reservation_id = pendingReservationService.pending_to_confirmed(pending_reservation_id)

        return {"data": f"Reservation {reservation_id} confirmed successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.put("/{reservation_id}")
async def update_reservation(reservation_id: int, current_user: User = Depends(get_current_user)):
    pass


@router.delete("/{reservation_id}")
async def cancel_reservation(reservation_id: int, current_user: User = Depends(get_current_user)):
    pass
