from datetime import datetime
from typing import Any

from pydantic import BaseModel


class EquipmentStatus(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(equipment_status_persistence) -> "EquipmentStatus":
        return EquipmentStatus(
            id=equipment_status_persistence["id"],
            name=equipment_status_persistence["name"],
            description=equipment_status_persistence["description"],
            created_at=equipment_status_persistence["created_at"],
            updated_at=equipment_status_persistence["updated_at"],
        )
