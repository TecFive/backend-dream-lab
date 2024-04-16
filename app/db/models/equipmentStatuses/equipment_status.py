from datetime import datetime
from typing import Any

from pydantic import BaseModel


class EquipmentStatus(BaseModel):
    id: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(equipment_status_persistence) -> "EquipmentStatus":
        return EquipmentStatus(
            id=equipment_status_persistence["id"],
            name=equipment_status_persistence["name"],
            description=equipment_status_persistence["description"],
            createdAt=equipment_status_persistence["createdAt"],
            updatedAt=equipment_status_persistence["updatedAt"],
        )
