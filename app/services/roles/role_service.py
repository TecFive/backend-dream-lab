from datetime import datetime
from typing import List

from app.db.models.application.roles.role import Role
from app.db.repositories.roles.role_repository import RoleRepository
from app.dtos.roles.create_role_dto import CreateRoleDto

import bson

from app.dtos.roles.update_role_dto import UpdateRoleDto


class RoleService:
    role_repository: RoleRepository

    def __init__(self):
        self.role_repository = RoleRepository()

    def get_all_roles(self) -> List[Role]:
        roles = self.role_repository.get_all_roles()

        return roles

    def find_role_by_id(self, role_id: str) -> Role:
        role = self.role_repository.find_role_by_id(role_id)

        return role

    def find_role_by_name(self, role_name: str) -> Role:
        role = self.role_repository.find_role_by_name(role_name)

        return role

    def create_role(self, role: CreateRoleDto) -> None:
        new_role = Role(
            id=str(bson.ObjectId()),
            name=role.name,
            description=role.description,
            permissions=role.permissions,
            priority=role.priority,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        self.role_repository.create_role(new_role)

    def update_role(self, role: UpdateRoleDto) -> None:
        role_found = self.role_repository.find_role_by_id(role.id)

        if role_found is None:
            raise Exception("Role not found.")

        role_found.name = role.name
        role_found.description = role.description
        role_found.permissions = role.permissions
        role_found.priority = role.priority
        role_found.updated_at = datetime.now().isoformat()

        self.role_repository.update_role(role_found)

    def delete_role(self, role_id: str) -> None:
        role_found = self.role_repository.find_role_by_id(role_id)

        if role_found is None:
            raise Exception("Role not found.")

        self.role_repository.delete_role(role_id)
