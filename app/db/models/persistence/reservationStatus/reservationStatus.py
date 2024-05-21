from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.db.models.application.reservationStatus.reservationStatus import ReservationStatus


class ReservationStatusPersistence(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_application(reservation_status: ReservationStatus) -> "ReservationStatusPersistence":
        return ReservationStatusPersistence(
            id=reservation_status.id,
            name=reservation_status.name,
            description=reservation_status.description,
            created_at=reservation_status.created_at,
            updated_at=reservation_status.updated_at
        )
