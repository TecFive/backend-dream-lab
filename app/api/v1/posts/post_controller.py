from fastapi import APIRouter, Depends
from app.core.config import Settings
from app.db.models.application.users.user import User
from app.dependency import get_current_user
from app.dtos.posts.create_post_dto import CreatePostDto
from app.dtos.posts.update_post_dto import UpdatePostDto
from app.services.posts.post_service import PostService

config = Settings()

router = APIRouter()
post_service = PostService()


@router.get("/")
async def get_all_posts():
    try:
        posts = post_service.get_all()

        return {"data": posts}
    except Exception as e:
        raise


@router.get("/id/{post_id}")
async def find_post_by_id(post_id: str):
    try:
        post = post_service.find_by_id(post_id)

        return {"data": post}
    except Exception as e:
        raise e


@router.post("/")
async def create_post(post_dto: CreatePostDto, current_user: User = Depends(get_current_user)):
    try:
        post = post_service.create(post_dto, current_user)

        return {"data": post}
    except Exception as e:
        raise e


@router.put("/{post_id}")
async def update_post(post_dto: UpdatePostDto, post_id: str, current_user: User = Depends(get_current_user)):
    try:
        post = post_service.update(post_dto, post_id, current_user)

        return {"data": post}
    except Exception as e:
        raise e


@router.put("/{post_id}/visibility")
async def update_post_visibility(post_id: str, visibility: bool, current_user: User = Depends(get_current_user)):
    try:
        post = post_service.change_visibility(post_id, visibility, current_user)

        return {"data": post}
    except Exception as e:
        raise e


@router.delete("/{post_id}")
async def delete_post(post_id: str):
    try:
        post_service.delete(post_id)

        return {"data": "Post deleted successfully."}
    except Exception as e:
        raise e
