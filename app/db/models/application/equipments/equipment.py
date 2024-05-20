from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class Equipment(BaseModel):
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
    def create_from_persistence(equipment_persistence) -> "Equipment":
        return Equipment(
            id=equipment_persistence["id"],
            name=equipment_persistence["name"],
            description=equipment_persistence["description"],
            status=equipment_persistence["status"],
            reservation_id=equipment_persistence["reservation_id"],
            image=equipment_persistence["image"],
            created_at=equipment_persistence["created_at"],
            updated_at=equipment_persistence["updated_at"],
        )
