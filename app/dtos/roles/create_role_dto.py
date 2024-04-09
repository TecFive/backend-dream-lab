from typing import List

from pydantic import BaseModel


class CreateRoleDto(BaseModel):
    name: str
    description: str
    permissions: List[str]
    priority: int
