from fastapi import APIRouter, Depends
from app.core.config import Settings
from app.db.models.users.user import User
from app.dependency import get_current_user


config = Settings()

router = APIRouter()


@router.post("/login")
async def login_for_access_token(
    current_user: User = Depends(get_current_user)
):
    pass
