from typing import List

from app.db.client import get_conn
from app.db.models.roles.role import Role


class RoleRepository:
    @staticmethod
    def find_role_by_id(role_id: str) -> Role:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Roles WHERE id = '{role_id}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            role_dict = dict(zip(columns, row))

            role = Role.create_from_persistence(role_dict)
        else:
            role = None

        return role

    @staticmethod
    def find_role_by_name(role_name: str) -> Role:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Roles WHERE name = '{role_name.upper()}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            role_dict = dict(zip(columns, row))

            role = Role.create_from_persistence(role_dict)
        else:
            role = None

        return role

    @staticmethod
    def get_all_roles() -> List[Role]:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Roles"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            roles = [dict(zip(columns, row)) for row in rows]
            roles = [Role.create_from_persistence(role) for role in roles]
        else:
            roles = []

        return roles

    @staticmethod
    def create_role(role: Role) -> None:
        connection = get_conn()
        cursor = connection.cursor()

        normalized_permissions = ",".join(role.permissions)
        cursor.execute(
            f"INSERT INTO Roles (id, name, description, permissions, priority, created_at, updated_at) VALUES ('{role.id}', '{role.name.upper()}', '{role.description}', '{normalized_permissions}', '{role.priority}', CAST('{role.created_at}' AS DATETIME2), CAST('{role.updated_at}' AS DATETIME2))"
        )

        connection.commit()
        connection.close()

    @staticmethod
    def update_role(role: Role) -> None:
        connection = get_conn()
        cursor = connection.cursor()

        normalized_permissions = ",".join(role.permissions)
        cursor.execute(
            f"UPDATE Roles SET name = '{role.name.upper()}', description = '{role.description}', permissions = '{normalized_permissions}', priority = '{role.priority}', updated_at = CAST('{role.updated_at}' AS DATETIME2) WHERE id = '{role.id}'"
        )

        connection.commit()
        connection.close()

    @staticmethod
    def delete_role(role_id: str) -> None:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"DELETE FROM Roles WHERE id = '{role_id}'"
        )

        connection.commit()
        connection.close()
