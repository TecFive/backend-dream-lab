from pydantic import BaseModel


class UpdateRoleDto(BaseModel):
    id: str
    name: str
    description: str
    permissions: str
