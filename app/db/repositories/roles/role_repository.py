from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.application.roles.role import Role

config = Settings()


class RoleRepository:
    database_client: DatabaseClient = DatabaseClient()

    def get_all_roles(self) -> List[Role]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Roles"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                roles = [dict(zip(columns, row)) for row in rows]
                roles = [Role.create_from_persistence(role) for role in roles]
            else:
                roles = []

            self.database_client.close()

            return roles
        except Exception as e:
            raise e

    def find_role_by_id(self, role_id: str) -> Role:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Roles WHERE id = '{role_id}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                role_dict = dict(zip(columns, row))

                role = Role.create_from_persistence(role_dict)
            else:
                role = None

            self.database_client.close()

            return role
        except Exception as e:
            raise e

    def find_role_by_name(self, role_name: str) -> Role:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Roles WHERE name = '{role_name.upper()}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                role_dict = dict(zip(columns, row))

                role = Role.create_from_persistence(role_dict)
            else:
                role = None

            self.database_client.close()

            return role
        except Exception as e:
            raise e

    def create_role(self, role: Role) -> None:
        try:
            cursor = self.database_client.get_conn()

            normalized_permissions = ",".join(role.permissions)
            cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Roles (id, name, description, permissions, priority, created_at, updated_at) VALUES ('{role.id}', '{role.name.upper()}', '{role.description}', '{normalized_permissions}', '{role.priority}', CAST('{role.created_at}' AS DATETIME2), CAST('{role.updated_at}' AS DATETIME2))"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def update_role(self, role: Role) -> None:
        try:
            cursor = self.database_client.get_conn()

            normalized_permissions = ",".join(role.permissions)
            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Roles SET name = '{role.name.upper()}', description = '{role.description}', permissions = '{normalized_permissions}', priority = '{role.priority}', updated_at = CAST('{role.updated_at}' AS DATETIME2) WHERE id = '{role.id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def delete_role(self, role_id: str) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Roles WHERE id = '{role_id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e
