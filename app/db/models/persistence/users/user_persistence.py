from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.db.models.application.users.user import User


class UserPersistence(BaseModel):
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
    def create_from_application(user: User) -> "UserPersistence":
        return UserPersistence(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            career=user.career,
            semester=user.semester,
            role=user.role,
            priority=user.priority,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
