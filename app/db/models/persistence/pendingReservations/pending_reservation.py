from datetime import datetime
from typing import List, Any

from pydantic import BaseModel

from app.db.models.application.pendingReservations.pending_reservation import PendingReservation


class PendingReservationPersistence(BaseModel):
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
    def create_from_application(pending_reservation: PendingReservation) -> "PendingReservationPersistence":
        reserved_equipment = [pr.id for pr in pending_reservation.reserved_equipment]

        return PendingReservationPersistence(
            id=pending_reservation.id,
            user_id=pending_reservation.user_id,
            room_id=pending_reservation.room_id,
            start_date=pending_reservation.start_date,
            end_date=pending_reservation.end_date,
            reserved_equipment=reserved_equipment,
            status=pending_reservation.status,
            comments=pending_reservation.comments,
            created_at=pending_reservation.created_at,
            updated_at=pending_reservation.updated_at
        )
