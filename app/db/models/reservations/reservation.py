from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Reservation(BaseModel):
    id: str
    user_id: str
    room_id: str
    start_date: datetime
    end_date: datetime
    status: int
    comments: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(user_persistence) -> "Reservation":
        return Reservation(
            id=user_persistence["id"],
            user_id=user_persistence["user_id"],
            room_id=user_persistence["room_id"],
            start_date=user_persistence["start_date"],
            end_date=user_persistence["end_date"],
            status=user_persistence["status"],
            comments=user_persistence["comments"],
            created_at=user_persistence["created_at"],
            updated_at=user_persistence["updated_at"],
        )
