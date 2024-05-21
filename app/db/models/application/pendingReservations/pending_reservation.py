from datetime import datetime
from typing import List, Any

from pydantic import BaseModel

from app.db.models.application.equipments.equipment import Equipment
from app.db.models.application.reservationStatus.reservationStatus import ReservationStatus
from app.db.models.application.rooms.room import Room
from app.db.models.application.users.user import User


class PendingReservation(BaseModel):
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
    def create_from_persistence(pending_reservation_persistence) -> "PendingReservation":
        reserved_equipment = pending_reservation_persistence["reserved_equipment"].split(",") if isinstance(pending_reservation_persistence["reserved_equipment"], str) else pending_reservation_persistence["reserved_equipment"]

        return PendingReservation(
            id=pending_reservation_persistence["id"],
            user_id=pending_reservation_persistence["user_id"],
            room_id=pending_reservation_persistence["room_id"],
            start_date=pending_reservation_persistence["start_date"],
            end_date=pending_reservation_persistence["end_date"],
            reserved_equipment=reserved_equipment,
            status=pending_reservation_persistence["status"],
            comments=pending_reservation_persistence["comments"],
            created_at=pending_reservation_persistence["created_at"],
            updated_at=pending_reservation_persistence["updated_at"],
        )
