from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class Equipment(BaseModel):
    id: str
    name: str
    description: str
    status: str
    reservationId: Optional[str]
    createdAt: datetime
    updatedAt: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(equipment_persistence) -> "Equipment":
        return Equipment(
            id=equipment_persistence["id"],
            name=equipment_persistence["name"],
            description=equipment_persistence["description"],
            status=equipment_persistence["status"],
            reservationId=equipment_persistence["reservationId"],
            createdAt=equipment_persistence["createdAt"],
            updatedAt=equipment_persistence["updatedAt"],
        )
