from datetime import datetime
from typing import Any, List

from pydantic import BaseModel

from app.db.models.application.reservations.reservation import Reservation


class ReservationPersistence(BaseModel):
    id: str
    user_id: str
    room_id: str
    start_date: datetime
    end_date: datetime
    reserved_equipment: List[str]
    status: str
    comments: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_application(reservation: Reservation) -> "ReservationPersistence":
        reserved_equipment = [r.id for r in reservation.reserved_equipment]

        return ReservationPersistence(
            id=reservation.id,
            user_id=reservation.user_id,
            room_id=reservation.room_id,
            start_date=reservation.start_date,
            end_date=reservation.end_date,
            reserved_equipment=reserved_equipment,
            status=reservation.status,
            comments=reservation.comments,
            created_at=reservation.created_at,
            updated_at=reservation.updated_at
        )
