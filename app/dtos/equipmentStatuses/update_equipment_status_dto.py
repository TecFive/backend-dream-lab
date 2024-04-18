from pydantic import BaseModel


class UpdateEquipmentStatusDto(BaseModel):
    id: str
    name: str
    description: str
