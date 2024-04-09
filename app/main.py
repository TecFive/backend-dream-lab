from app.api.v1.auth import auth_controller
from app.api.v1.reservations import reservation_controller
from app.api.v1.users import user_controller
from app.core.config import Settings

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
import os

from app.dependency import has_jwt_access

config = Settings()

app = FastAPI()
if os.getenv("ENVIRONMENT") != "dev":
    app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROTECTED = [Depends(has_jwt_access)]

app.include_router(
    auth_controller.router,
    prefix="/v1/auth",
    tags=["auth"],
    dependencies=None
)

app.include_router(
    user_controller.router,
    prefix="/v1/users",
    tags=["users"],
    dependencies=PROTECTED
)

app.include_router(
    reservation_controller.router,
    prefix="/v1/reservations",
    tags=["reservations"],
    dependencies=PROTECTED
)
