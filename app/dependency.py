from jose import jwt
from jose.exceptions import JOSEError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import Settings
from app.db.models.users.user import User
from app.services.users.user_service import UserService

config = Settings()
security = HTTPBearer()
userService = UserService()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        payload = jwt.decode(
            token.credentials, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
        )

        user = userService.find_user_by_id(payload["id"])

        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Could not validate credentials: {e}"
        )


async def has_jwt_access(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        jwt.decode(
            token,
            key=config.JWT_SECRET_KEY,
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iss": False,
            },
        )
    except JOSEError as e:
        raise HTTPException(status_code=401, detail=str(e))


def has_admin_access(token: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        payload = jwt.decode(
            token.credentials, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
        )

        role = payload["role"].lower().replace(" ", "")
        if role != "superadmin":
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = userService.find_user_by_id(payload["id"])

        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Could not validate credentials: {e}"
        )
