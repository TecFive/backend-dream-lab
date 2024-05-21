from pydantic import BaseModel


class CreateEquipmentDto(BaseModel):
    name: str
    description: str
    image: str
    status: str
