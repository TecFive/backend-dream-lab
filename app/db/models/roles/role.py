from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Role(BaseModel):
    id: str
    name: str
    description: str
    permissions: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(user_persistence) -> "Role":
        return Role(
            id=user_persistence["id"],
            name=user_persistence["name"],
            description=user_persistence["description"],
            permissions=user_persistence["permissions"],
            created_at=user_persistence["created_at"],
            updated_at=user_persistence["updated_at"],
        )
