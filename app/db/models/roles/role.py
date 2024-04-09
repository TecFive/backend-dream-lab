from datetime import datetime
from typing import Any, List

from pydantic import BaseModel


class Role(BaseModel):
    id: str
    name: str
    description: str
    permissions: List[str]
    priority: int
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(user_persistence) -> "Role":
        permissions = user_persistence["permissions"].split(",") if isinstance(user_persistence["permissions"], str) else user_persistence["permissions"]

        return Role(
            id=user_persistence["id"],
            name=user_persistence["name"],
            description=user_persistence["description"],
            permissions=permissions,
            priority=user_persistence["priority"],
            created_at=user_persistence["created_at"],
            updated_at=user_persistence["updated_at"],
        )
