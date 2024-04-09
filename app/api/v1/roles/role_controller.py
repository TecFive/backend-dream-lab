from fastapi import APIRouter
from app.core.config import Settings
from app.dtos.roles.create_role_dto import CreateRoleDto
from app.dtos.roles.update_role_dto import UpdateRoleDto
from app.services.roles.role_service import RoleService

config = Settings()

router = APIRouter()
roleService = RoleService()


@router.get("/")
async def get_all_roles():
    try:
        roles = roleService.get_all_roles()

        return roles
    except Exception as e:
        raise e


@router.get("/{role_id}")
async def find_role_by_id(role_id: str):
    try:
        role = roleService.find_role_by_id(role_id)

        return role
    except Exception as e:
        raise e


@router.get("/name/{role_name}")
async def find_role_by_name(role_name: str):
    try:
        role = roleService.find_role_by_name(role_name)

        return role
    except Exception as e:
        raise e


@router.post("/")
async def create_role(create_role_dto: CreateRoleDto):
    try:
        roleService.create_role(create_role_dto)

        return {"message": "Role created successfully."}
    except Exception as e:
        raise e


@router.put("/")
async def update_role(update_role_dto: UpdateRoleDto):
    try:
        roleService.update_role(update_role_dto)

        return {"message": "Role updated successfully."}
    except Exception as e:
        raise e


@router.delete("/{role_id}")
async def delete_role(role_id: str):
    try:
        roleService.delete_role(role_id)

        return {"message": "Role deleted successfully."}
    except Exception as e:
        raise e
