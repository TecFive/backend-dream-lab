from fastapi import APIRouter, Depends
from app.core.config import Settings
from app.db.models.users.user import User
from app.dependency import get_current_user
from app.services.reservations.reservation_service import ReservationService

config = Settings()

router = APIRouter()
reservationService = ReservationService()


@router.get("/my-reservations")
async def get_my_reservations(current_user: User = Depends(get_current_user)):
    pass
