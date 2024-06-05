from datetime import datetime
from typing import List

from fastapi import HTTPException

from app.db.models.application.posts.post import Post
from app.db.models.application.users.user import User
from app.db.models.shared.py_object_id import PyObjectId
from app.db.repositories.posts.post_repository import PostRepository
from app.dtos.posts.create_post_dto import CreatePostDto
from app.dtos.posts.update_post_dto import UpdatePostDto
from app.services.postTypes.post_type_service import PostTypeService


class PostService:
    post_type_service: PostTypeService
    post_repository: PostRepository

    def __init__(self):
        self.post_type_service = PostTypeService()
        self.post_repository = PostRepository()

    def get_all(self) -> List[Post]:
        posts = self.post_repository.get_all()

        return posts

    def find_by_id(self, post_id: str) -> Post:
        post = self.post_repository.find_by_id(PyObjectId(post_id))
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")

        return post

    def create(self, post_dto: CreatePostDto, current_user: User) -> Post:
        post_type = self.post_type_service.find_by_name(post_dto.type)
        if post_type is None:
            raise HTTPException(status_code=404, detail="Post type not found")

        post = Post(
            file=post_dto.file,
            title=post_dto.title,
            description=post_dto.description,
            visible=True,
            createdBy=current_user.id,
            createdAt=datetime.now().isoformat(),
            updatedBy=current_user.id,
            updatedAt=datetime.now().isoformat(),
            type=post_type.id
        )

        self.post_repository.create(post)

        return post

    def update(self, post_dto: UpdatePostDto, post_id: str, current_user: User) -> Post:
        post = self.post_repository.find_by_id(PyObjectId(post_id))
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")

        if post_dto.file is not None:
            post.file = post_dto.file

        if post_dto.title is not None:
            post.title = post_dto.title

        if post_dto.description is not None:
            post.description = post_dto.description

        if post_dto.visible is not None:
            post.visible = post_dto.visible

        post.updatedBy = current_user.id
        post.updatedAt = datetime.utcnow().isoformat()

        self.post_repository.update(post)

        return post

    def change_visibility(self, post_id: str, visible: bool, current_user: User) -> Post:
        post = self.post_repository.find_by_id(PyObjectId(post_id))
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")

        post.visible = visible
        post.updatedBy = current_user.id
        post.updatedAt = datetime.now().isoformat()

        self.post_repository.update(post)

        return post

    def delete(self, post_id: str) -> None:
        post = self.post_repository.find_by_id(PyObjectId(post_id))
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")

        self.post_repository.delete(PyObjectId(post_id))
