from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Room(BaseModel):
    id: str
    name: str
    description: str
    capacity: int
    room_equipment: list[str]
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(room_persistence) -> "Room":
        room_equipment = room_persistence["room_equipment"].split(",") if isinstance(room_persistence["room_equipment"], str) else room_persistence["room_equipment"]

        return Room(
            id=room_persistence["id"],
            name=room_persistence["name"],
            description=room_persistence["description"],
            capacity=room_persistence["capacity"],
            room_equipment=room_equipment,
            created_at=room_persistence["created_at"],
            updated_at=room_persistence["updated_at"],
        )
