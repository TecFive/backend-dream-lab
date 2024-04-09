from pydantic import BaseModel


class CreateRoleDto(BaseModel):
    name: str
    description: str
    permissions: str
