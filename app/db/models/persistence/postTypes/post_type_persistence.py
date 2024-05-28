from typing import Any

from bson import ObjectId
from pydantic import BaseModel, Field

from app.db.models.application.postTypes.post_type import PostType
from app.db.models.shared.py_object_id import PyObjectId


class PostTypePersistence(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    displayName: str

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_application(post_type: PostType) -> "PostTypePersistence":
        return PostTypePersistence(
            id=post_type.id,
            name=post_type.name,
            displayName=post_type.displayName
        )

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}
