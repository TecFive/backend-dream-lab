from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.db.models.shared.py_object_id import PyObjectId


class Post(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    file: str
    title: str
    description: Optional[str] = None
    createdBy: PyObjectId
    createdAt: str
    updatedBy: PyObjectId
    updatedAt: str
    type: PyObjectId

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(post_persistence) -> "Post":
        return Post(
            id=PyObjectId(post_persistence["_id"]),
            file=post_persistence["file"],
            title=post_persistence["title"],
            description=post_persistence["description"],
            createdBy=PyObjectId(post_persistence["createdBy"]),
            createdAt=post_persistence["createdAt"],
            updatedBy=PyObjectId(post_persistence["updatedBy"]),
            updatedAt=post_persistence["updatedAt"],
            type=PyObjectId(post_persistence["type"]),
        )

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}
