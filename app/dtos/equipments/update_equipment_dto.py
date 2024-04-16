from pydantic import BaseModel


class UpdateEquipmentDto(BaseModel):
    id: str
    name: str
    description: str
    status: str
    reservation_id: str
