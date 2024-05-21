from pydantic import BaseModel


class UpdateEquipmentDto(BaseModel):
    id: str
    name: str
    description: str
    image: str
    status: str
    reservation_id: str
