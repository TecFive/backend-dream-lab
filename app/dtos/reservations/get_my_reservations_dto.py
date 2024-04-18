from datetime import datetime
from typing import List, Any

from pydantic import BaseModel


class GetMyReservationsDto(BaseModel):
    id: str
    name: str
    start_date: datetime
    end_date: datetime
    reserved_equipment: List[str]

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(reservation_persistence) -> "GetMyReservationsDto":
        reserved_equipment = reservation_persistence["reserved_equipment"].split(",") if isinstance(reservation_persistence["reserved_equipment"], str) else reservation_persistence["reserved_equipment"]

        return GetMyReservationsDto(
            id=reservation_persistence["id"],
            name=reservation_persistence["name"],
            start_date=reservation_persistence["start_date"],
            end_date=reservation_persistence["end_date"],
            reserved_equipment=reserved_equipment,
        )
