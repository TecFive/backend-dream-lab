from datetime import datetime
from typing import List, Any, Optional

from pydantic import BaseModel

from app.dtos.reservations.reservation_equipment_detail_dto import ReservationEquipmentDetailDto


class GetMyReservationsDto(BaseModel):
    id: str
    name: str
    room_image: Optional[str]
    status: str
    start_date: datetime
    end_date: datetime
    reserved_equipment: List[ReservationEquipmentDetailDto]

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(reservation_persistence) -> "GetMyReservationsDto":
        return GetMyReservationsDto(
            id=reservation_persistence["id"],
            name=reservation_persistence["name"],
            room_image=reservation_persistence["room_image"],
            status=reservation_persistence["status"],
            start_date=reservation_persistence["start_date"],
            end_date=reservation_persistence["end_date"],
            reserved_equipment=reservation_persistence["reserved_equipment"],
        )
