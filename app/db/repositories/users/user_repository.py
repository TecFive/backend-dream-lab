from typing import List

from app.db.client import get_conn
from app.db.models.users.user import User


class UserRepository:
    @staticmethod
    def get_all_users() -> List[User]:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Users"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            users = [dict(zip(columns, row)) for row in rows]
            users = [User.create_from_persistence(user) for user in users]
        else:
            users = []

        connection.close()

        return users

    @staticmethod
    def get_all_users_by_career(career: str) -> List[User]:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Users WHERE career = '{career.upper()}'"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            users = [dict(zip(columns, row)) for row in rows]
            users = [User.create_from_persistence(user) for user in users]
        else:
            users = []

        connection.close()

        return users

    @staticmethod
    def get_all_users_by_semester(semester: int) -> List[User]:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Users WHERE semester = {semester}"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            users = [dict(zip(columns, row)) for row in rows]
            users = [User.create_from_persistence(user) for user in users]
        else:
            users = []

        connection.close()

        return users

    @staticmethod
    def find_user_by_id(user_id: str) -> User:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Users WHERE id = '{user_id}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            user_dict = dict(zip(columns, row))

            user = User.create_from_persistence(user_dict)
        else:
            user = None

        connection.close()

        return user

    @staticmethod
    def find_user_by_email(email: str) -> User:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Users WHERE email = '{email.upper()}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            user_dict = dict(zip(columns, row))

            user = User.create_from_persistence(user_dict)
        else:
            user = None

        connection.close()

        return user

    @staticmethod
    def register_user(user: User) -> None:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"INSERT INTO Users (id, name, email, password, career, semester, role, priority, created_at, updated_at) VALUES ('{user.id}', '{user.name.upper()}', '{user.email.upper()}', '{user.password}', '{user.career.upper()}', {user.semester}, '{user.role}', '{user.priority}', CAST('{str(user.created_at)}' AS DATETIME2), CAST('{str(user.updated_at)}' AS DATETIME2))"
        )

        connection.commit()
        connection.close()

    @staticmethod
    def update_user(user: User) -> None:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"UPDATE Users SET name = '{user.name.upper()}', email = '{user.email.upper()}', career = '{user.career.upper()}', semester = {user.semester}, role = '{user.role}', priority = '{user.priority}', updated_at = CAST('{str(user.updated_at)}' AS DATETIME2) WHERE id = '{user.id}'"
        )

        connection.commit()
        connection.close()

    @staticmethod
    def delete_user(user_id: str) -> None:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"DELETE FROM Users WHERE id = '{user_id}'"
        )

        connection.commit()
        connection.close()
