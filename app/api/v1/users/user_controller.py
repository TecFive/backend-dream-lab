from fastapi import APIRouter, Depends
from app.core.config import Settings
from app.db.models.users.user import User
from app.dependency import get_current_user
from app.services.users.user_service import UserService

config = Settings()

router = APIRouter()
userService = UserService()


@router.get("/my-info")
async def get_logged_user_info(
    current_user: User = Depends(get_current_user)
):
    try:
        return {"data": current_user}
    except Exception as e:
        return {"error": str(e)}
