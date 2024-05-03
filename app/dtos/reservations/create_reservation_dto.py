from datetime import datetime
from typing import List

from pydantic import BaseModel


class CreateReservationDto(BaseModel):
    room_id: str
    start_date: datetime
    end_date: datetime
    reserved_equipment: List[str]
    comments: str
