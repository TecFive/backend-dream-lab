from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel

from app.db.models.application.equipments.equipment import Equipment


class EquipmentPersistence(BaseModel):
    id: str
    name: str
    description: str
    status: str
    reservation_id: Optional[str]
    image: Optional[str]
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_application(equipment: Equipment) -> "EquipmentPersistence":
        return EquipmentPersistence(
            id=equipment.id,
            name=equipment.name,
            description=equipment.description,
            status=equipment.status,
            reservation_id=equipment.reservation_id,
            image=equipment.image,
            created_at=equipment.created_at,
            updated_at=equipment.updated_at
        )
