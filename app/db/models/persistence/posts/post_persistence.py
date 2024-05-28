from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.db.models.application.posts.post import Post
from app.db.models.shared.py_object_id import PyObjectId


class PostPersistence(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    file: str
    title: str
    description: Optional[str] = None
    visible: bool
    createdBy: PyObjectId
    createdAt: str
    updatedBy: PyObjectId
    updatedAt: str
    type: PyObjectId

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_application(post: Post) -> "PostPersistence":
        return PostPersistence(
            id=post.id,
            file=post.file,
            title=post.title,
            description=post.description,
            visible=post.visible,
            createdBy=post.createdBy,
            createdAt=post.createdAt,
            updatedBy=post.updatedBy,
            updatedAt=post.updatedAt,
            type=post.type
        )

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}
