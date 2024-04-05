from typing import Any

from pydantic import BaseModel


class User(BaseModel):
    id: str

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(user_persistence) -> "User":
        return User(
            id=user_persistence["_id"]
        )
