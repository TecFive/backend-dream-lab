from fastapi import APIRouter
from app.core.config import Settings
from app.dtos.postTypes.create_post_type_dto import CreatePostTypeDto
from app.dtos.postTypes.update_post_type_dto import UpdatePostTypeDto
from app.services.postTypes.post_type_service import PostTypeService

config = Settings()

router = APIRouter()
post_type_service = PostTypeService()


@router.get("/")
async def get_all_post_types():
    try:
        post_types = post_type_service.get_all()

        return {"data": post_types}
    except Exception as e:
        raise


@router.get("/id/{post_type_id}")
async def find_post_type_by_id(post_type_id: str):
    try:
        post_type = post_type_service.find_by_id(post_type_id)

        return {"data": post_type}
    except Exception as e:
        raise e


@router.get("/name/{post_type_name}")
async def find_post_type_by_name(post_type_name: str):
    try:
        post_type = post_type_service.find_by_name(post_type_name)

        return {"data": post_type}
    except Exception as e:
        raise e


@router.post("/")
async def create_post_type(post_type_data: CreatePostTypeDto):
    try:
        post_type = post_type_service.create(post_type_data)

        return {"data": post_type}
    except Exception as e:
        raise e


@router.put("/")
async def update_post_type(post_type_dto: UpdatePostTypeDto):
    try:
        post_type = post_type_service.update(post_type_dto)

        return {"data": post_type}
    except Exception as e:
        raise e


@router.delete("/{post_type_id}")
async def delete_post_type(post_type_id: str):
    try:
        post_type_service.delete(post_type_id)

        return {"data": "Post type deleted successfully."}
    except Exception as e:
        raise e
