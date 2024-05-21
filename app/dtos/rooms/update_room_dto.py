from typing import List, Optional

from pydantic import BaseModel


class UpdateRoomDto(BaseModel):
    id: str
    name: Optional[str]
    description: Optional[str]
    capacity: Optional[int]
    room_equipment: Optional[List[str]]
    image: Optional[str]
