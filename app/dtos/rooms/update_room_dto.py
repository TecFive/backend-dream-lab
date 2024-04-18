from typing import List

from pydantic import BaseModel


class UpdateRoomDto(BaseModel):
    id: str
    name: str
    description: str
    capacity: int
    room_equipment: List[str]
