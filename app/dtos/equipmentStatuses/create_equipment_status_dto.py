from pydantic import BaseModel


class CreateEquipmentStatusDto(BaseModel):
    name: str
    description: str
