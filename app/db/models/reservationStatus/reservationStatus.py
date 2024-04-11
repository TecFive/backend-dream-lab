from typing import Any

from pydantic import BaseModel


class ReservationStatus(BaseModel):
    id: str
    name: str
    description: str
    created_at: str
    updated_at: str

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(user_persistence) -> "ReservationStatus":
        return ReservationStatus(
            id=user_persistence["id"],
            name=user_persistence["name"],
            description=user_persistence["description"],
            created_at=user_persistence["created_at"],
            updated_at=user_persistence["updated_at"],
        )
