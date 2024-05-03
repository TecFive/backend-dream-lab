from typing import List

from app.core.config import Settings
from app.db.client import database_client
from app.db.models.roles.role import Role

config = Settings()


class RoleRepository:
    cursor = database_client.get_conn()

    def get_all_roles(self) -> List[Role]:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Roles"
            )

            rows = self.cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in self.cursor.description]
                roles = [dict(zip(columns, row)) for row in rows]
                roles = [Role.create_from_persistence(role) for role in roles]
            else:
                roles = []

            return roles
        except Exception as e:
            raise e

    def find_role_by_id(self, role_id: str) -> Role:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Roles WHERE id = '{role_id}'"
            )

            row = self.cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in self.cursor.description]
                role_dict = dict(zip(columns, row))

                role = Role.create_from_persistence(role_dict)
            else:
                role = None

            return role
        except Exception as e:
            raise e

    def find_role_by_name(self, role_name: str) -> Role:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Roles WHERE name = '{role_name.upper()}'"
            )

            row = self.cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in self.cursor.description]
                role_dict = dict(zip(columns, row))

                role = Role.create_from_persistence(role_dict)
            else:
                role = None

            return role
        except Exception as e:
            raise e

    def create_role(self, role: Role) -> None:
        try:
            self.cursor = database_client.get_conn()

            normalized_permissions = ",".join(role.permissions)
            self.cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Roles (id, name, description, permissions, priority, created_at, updated_at) VALUES ('{role.id}', '{role.name.upper()}', '{role.description}', '{normalized_permissions}', '{role.priority}', CAST('{role.created_at}' AS DATETIME2), CAST('{role.updated_at}' AS DATETIME2))"
            )
        except Exception as e:
            raise e

    def update_role(self, role: Role) -> None:
        try:
            self.cursor = database_client.get_conn()

            normalized_permissions = ",".join(role.permissions)
            self.cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Roles SET name = '{role.name.upper()}', description = '{role.description}', permissions = '{normalized_permissions}', priority = '{role.priority}', updated_at = CAST('{role.updated_at}' AS DATETIME2) WHERE id = '{role.id}'"
            )
        except Exception as e:
            raise e

    def delete_role(self, role_id: str) -> None:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Roles WHERE id = '{role_id}'"
            )
        except Exception as e:
            raise e
