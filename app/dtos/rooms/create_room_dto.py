from typing import List, Optional

from pydantic import BaseModel


class CreateRoomDto(BaseModel):
    name: str
    description: str
    capacity: int
    room_equipment: List[str]
    image: Optional[str]
