from datetime import datetime
from typing import Any, List

from pydantic import BaseModel

from app.db.models.application.equipments.equipment import Equipment
from app.db.models.application.reservationStatus.reservation_status import ReservationStatus
from app.db.models.application.rooms.room import Room
from app.db.models.application.users.user import User


class Reservation(BaseModel):
    id: str
    user: User
    room: Room
    start_date: datetime
    end_date: datetime
    reserved_equipment: List[Equipment]
    status: ReservationStatus
    comments: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(reservation_persistence) -> "Reservation":
        return Reservation(
            id=reservation_persistence["id"],
            user=reservation_persistence["user"],
            room=reservation_persistence["room"],
            start_date=reservation_persistence["start_date"],
            end_date=reservation_persistence["end_date"],
            reserved_equipment=reservation_persistence["reserved_equipment"],
            status=reservation_persistence["status"],
            comments=reservation_persistence["comments"],
            created_at=reservation_persistence["created_at"],
            updated_at=reservation_persistence["updated_at"],
        )
