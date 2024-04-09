from datetime import datetime
from typing import Any

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    career: str
    semester: int
    role: str
    priority: int
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(user_persistence) -> "User":
        return User(
            id=user_persistence["id"],
            name=user_persistence["name"],
            email=user_persistence["email"],
            password=user_persistence["password"],
            career=user_persistence["career"],
            semester=user_persistence["semester"],
            role=user_persistence["role"],
            priority=user_persistence["priority"],
            created_at=user_persistence["created_at"],
            updated_at=user_persistence["updated_at"]
        )
