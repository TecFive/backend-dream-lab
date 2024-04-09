from pydantic import BaseModel


class UpdateUserRoleDto(BaseModel):
    user_id: str
    role_id: str
