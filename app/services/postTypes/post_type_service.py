from typing import List

from fastapi import HTTPException

from app.db.models.application.postTypes.post_type import PostType
from app.db.models.shared.py_object_id import PyObjectId
from app.db.repositories.postTypes.post_type_repository import PostTypeRepository
from app.dtos.postTypes.create_post_type_dto import CreatePostTypeDto
from app.dtos.postTypes.update_post_type_dto import UpdatePostTypeDto


class PostTypeService:
    post_type_repository: PostTypeRepository

    def __init__(self):
        self.post_type_repository = PostTypeRepository()

    def get_all(self) -> List[PostType]:
        post_types = self.post_type_repository.get_all()

        return post_types

    def find_by_id(self, post_type_id: str) -> PostType:
        post_type = self.post_type_repository.find_by_id(PyObjectId(post_type_id))
        if post_type is None:
            raise HTTPException(status_code=404, detail="Post type not found")

        return post_type

    def find_by_name(self, name: str) -> PostType:
        post_type = self.post_type_repository.find_by_name(name)

        if post_type is None:
            raise HTTPException(status_code=404, detail="Post type not found")

        return post_type

    def create(self, post_type_dto: CreatePostTypeDto) -> PostType:
        exists = self.post_type_repository.find_by_name(post_type_dto.name)
        if exists is not None:
            raise HTTPException(status_code=400, detail="Post type already exists")

        post_type = PostType(
            name=post_type_dto.name,
            displayName=post_type_dto.displayName
        )

        self.post_type_repository.create(post_type)

        return post_type

    def update(self, post_type_dto: UpdatePostTypeDto) -> PostType:
        post_type_found = self.post_type_repository.find_by_id(post_type_dto.id)
        if post_type_found is None:
            raise HTTPException(status_code=404, detail="Post type not found")

        post_type_found.name = post_type_dto.name
        post_type_found.displayName = post_type_dto.displayName

        self.post_type_repository.update(post_type_found)

        return post_type_found

    def delete(self, post_type_id: str) -> None:
        post_type_found = self.post_type_repository.find_by_id(PyObjectId(post_type_id))
        if post_type_found is None:
            raise HTTPException(status_code=404, detail="Post type not found")

        self.post_type_repository.delete(PyObjectId(post_type_id))
