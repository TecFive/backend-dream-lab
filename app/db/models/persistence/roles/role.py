from datetime import datetime
from typing import Any, List

from pydantic import BaseModel

from app.db.models.application.roles.role import Role


class RolePersistence(BaseModel):
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
    def create_from_application(role: Role) -> "RolePersistence":
        permissions = role.permissions.split(",") if isinstance(role.permissions, str) else role.permissions

        return RolePersistence(
            id=role["id"],
            name=role["name"],
            description=role["description"],
            permissions=permissions,
            priority=role["priority"],
            created_at=role["created_at"],
            updated_at=role["updated_at"]
        )
