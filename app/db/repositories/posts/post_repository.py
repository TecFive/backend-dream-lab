from typing import List, Any, Dict

from app.db.models.application.posts.post import Post
from app.db.models.persistence.posts.post_persistence import PostPersistence
from app.db.models.shared.py_object_id import PyObjectId
from app.db.mongodb_client import mongodb


class PostRepository:
    @staticmethod
    def get_all(filter_params: Dict[str, Any] = None) -> List[Post]:
        if filter_params is None:
            filter_params = {}

        posts = mongodb.posts.find(filter_params)

        return [Post.create_from_persistence(post) for post in posts]

    @staticmethod
    def find_by_id(post_id: PyObjectId) -> Post:
        post = mongodb.posts.find_one({"_id": post_id})

        return Post.create_from_persistence(post) if post else None

    @staticmethod
    def create(post: Post) -> None:
        post_persistence = PostPersistence.create_from_application(post)

        mongodb.posts.insert_one(post_persistence.model_dump(by_alias=True))

    @staticmethod
    def update(post: Post) -> None:
        post_persistence = PostPersistence.create_from_application(post)

        mongodb.posts.update_one(
            {"_id": post.id}, {"$set": post_persistence.model_dump(by_alias=True)}
        )

    @staticmethod
    def delete(post_id: PyObjectId) -> None:
        mongodb.posts.delete_one({"_id": post_id})
