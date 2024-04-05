from jose import jwt
from jose.exceptions import JOSEError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import Settings
from app.db.models.users.user import User

config = Settings()
security = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        payload = jwt.decode(
            token.credentials, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )

        # TODO: Implement user fetching from database
        user = None

        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        combined_user_info = {**user, **payload}

        # TODO: Implement user mapping from database and token
        user = User()

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Could not validate credentials: {e}"
        )


async def has_admin_access(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        user = get_current_user(credentials)

        if not user.isAdmin:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except JOSEError as e:
        raise HTTPException(status_code=401, detail=str(e))


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
