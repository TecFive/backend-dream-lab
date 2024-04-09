from typing import List

from fastapi import APIRouter, HTTPException
from app.core.config import Settings
from app.core.security import Security
from app.dtos.users.create_user_dto import CreateUserDto
from app.services.users.user_service import UserService

config = Settings()

router = APIRouter()
userService = UserService()


@router.post("/login")
async def login_for_access_token(password: str, email: str):
    try:
        if email is None or password is None:
            raise HTTPException(
                status_code=400,
                detail="Email or password are incorrect. Please try again.",
            )

        user = userService.find_user_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=400,
                detail="Email or password are incorrect. Please try again.",
            )

        if not Security.verify_password(password, user.password):
            raise HTTPException(
                status_code=400,
                detail="Email or password are incorrect. Please try again.",
            )

        return {"data": Security.generate_jwt_token(user)}
    except Exception as e:
        return {"error": str(e)}


@router.post("/register")
async def register_user(create_user_dto: CreateUserDto):
    try:
        user = userService.register_user(create_user_dto)

        return {"data": user}
    except Exception as e:
        return {"error": str(e)}


@router.post("/multi-register")
async def register_multiple_users(create_user_dtos: List[CreateUserDto]):
    try:
        users = []
        for create_user_dto in create_user_dtos:
            user = userService.register_user(create_user_dto)
            users.append(user)

        return {"data": users}
    except Exception as e:
        return {"error": str(e)}
