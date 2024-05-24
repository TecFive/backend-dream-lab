from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.db.models.application.equipmentStatuses.equipment_status import EquipmentStatus


class EquipmentStatusPersistence(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_application(equipment_status: EquipmentStatus) -> "EquipmentStatusPersistence":
        return EquipmentStatusPersistence(
            id=equipment_status.id,
            name=equipment_status.name,
            description=equipment_status.description,
            created_at=equipment_status.created_at,
            updated_at=equipment_status.updated_at
        )
