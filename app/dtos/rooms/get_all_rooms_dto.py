from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.db.models.application.equipments.equipment import Equipment


class GetAllRoomsDto(BaseModel):
    id: str
    name: str
    description: str
    capacity: int
    room_equipment: list[Equipment]
    image: Optional[str]
    created_at: datetime
    updated_at: datetime
