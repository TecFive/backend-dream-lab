from typing import List

from pydantic import BaseModel


class CreatePendingReservationDto(BaseModel):
    room_id: str
    start_date: str
    end_date: str
    reserved_equipment: List[str]
    status: str
    comments: str
