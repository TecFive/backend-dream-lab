from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from app.db.models.application.rooms.room import Room


class RoomPersistence(BaseModel):
    id: str
    name: str
    description: str
    capacity: int
    room_equipment: list[str]
    image: Optional[str]
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_application(room: Room) -> "RoomPersistence":
        room_equipment = [e.id for e in room.room_equipment]

        return RoomPersistence(
            id=room.id,
            name=room.name,
            description=room.description,
            capacity=room.capacity,
            room_equipment=room_equipment,
            image=room.image,
            created_at=room.created_at,
            updated_at=room.updated_at
        )
