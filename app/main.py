from app.api.v1.auth import auth_controller
from app.api.v1.equipment_statuses import equipment_status_controller
from app.api.v1.equipments import equipment_controller
from app.api.v1.reservations import reservation_controller
from app.api.v1.rooms import room_controller
from app.api.v1.users import user_controller
from app.core.config import Settings

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from app.dependency import has_jwt_access

WORKING_CDN = "unpkg.com"

config = Settings()

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=f"https://{WORKING_CDN}/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url=f"https://{WORKING_CDN}/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url=f"https://{WORKING_CDN}/redoc@next/bundles/redoc.standalone.js",
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

app.include_router(
    equipment_controller.router,
    prefix="/v1/equipment",
    tags=["equipment"],
    dependencies=PROTECTED
)

app.include_router(
    equipment_status_controller.router,
    prefix="/v1/equipment-status",
    tags=["equipment-status"],
    dependencies=PROTECTED
)

app.include_router(
    room_controller.router,
    prefix="/v1/rooms",
    tags=["rooms"],
    dependencies=PROTECTED
)
