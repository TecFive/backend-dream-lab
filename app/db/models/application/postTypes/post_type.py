from typing import Any

from bson import ObjectId
from pydantic import BaseModel, Field

from app.db.models.shared.py_object_id import PyObjectId


class PostType(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    displayName: str

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(post_type_persistence) -> "PostType":
        return PostType(
            id=PyObjectId(post_type_persistence["_id"]),
            name=post_type_persistence["name"],
            displayName=post_type_persistence["displayName"]
        )

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}
