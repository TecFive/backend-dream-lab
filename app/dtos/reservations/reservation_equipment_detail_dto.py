from pydantic import BaseModel


class ReservationEquipmentDetailDto(BaseModel):
    id: str
    name: str
