from typing import Any, Dict, List

from app.db.models.application.postTypes.post_type import PostType
from app.db.models.persistence.postTypes.post_type_persistence import PostTypePersistence
from app.db.models.shared.py_object_id import PyObjectId
from app.db.mongodb_client import mongodb


class PostTypeRepository:
    @staticmethod
    def get_all(filter_params: Dict[str, Any] = None) -> List[PostType]:
        if filter_params is None:
            filter_params = {}

        post_types = mongodb.post_types.find(filter_params)

        return [PostType.create_from_persistence(post_type) for post_type in post_types]

    @staticmethod
    def find_by_id(post_type_id: PyObjectId) -> PostType:
        post_type = mongodb.post_types.find_one({"_id": post_type_id})

        return PostType.create_from_persistence(post_type) if post_type else None

    @staticmethod
    def find_by_name(name: str) -> PostType:
        post_type = mongodb.post_types.find_one({"name": name})

        return PostType.create_from_persistence(post_type) if post_type else None

    @staticmethod
    def create(post_type: PostType) -> None:
        post_type_persistence = PostTypePersistence.create_from_application(post_type)

        mongodb.post_types.insert_one(post_type_persistence.model_dump(by_alias=True))

    @staticmethod
    def update(post_type: PostType) -> None:
        post_type_persistence = PostTypePersistence.create_from_application(post_type)

        mongodb.post_types.update_one(
            {"_id": post_type.id}, {"$set": post_type_persistence.model_dump(by_alias=True)}
        )

    @staticmethod
    def delete(post_type_id: str) -> None:
        mongodb.post_types.delete_one({"_id": post_type_id})
