from typing import List

from app.core.config import Settings
from app.db.client import database_client
from app.db.models.users.user import User

config = Settings()


class UserRepository:
    cursor = database_client.get_conn()

    def get_all_users(self) -> List[User]:
        try:
            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Users"
            )

            rows = self.cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in self.cursor.description]
                users = [dict(zip(columns, row)) for row in rows]
                users = [User.create_from_persistence(user) for user in users]
            else:
                users = []

            return users
        except Exception as e:
            raise e

    def get_all_users_by_career(self, career: str) -> List[User]:
        try:
            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Users WHERE career = '{career.upper()}'"
            )

            rows = self.cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in self.cursor.description]
                users = [dict(zip(columns, row)) for row in rows]
                users = [User.create_from_persistence(user) for user in users]
            else:
                users = []

            return users
        except Exception as e:
            raise e

    def get_all_users_by_semester(self, semester: int) -> List[User]:
        try:
            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Users WHERE semester = {semester}"
            )

            rows = self.cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in self.cursor.description]
                users = [dict(zip(columns, row)) for row in rows]
                users = [User.create_from_persistence(user) for user in users]
            else:
                users = []

            return users
        except Exception as e:
            raise e

    def find_user_by_id(self, user_id: str) -> User:
        try:
            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Users WHERE id = '{user_id}'"
            )

            row = self.cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in self.cursor.description]
                user_dict = dict(zip(columns, row))

                user = User.create_from_persistence(user_dict)
            else:
                user = None

            return user
        except Exception as e:
            raise e

    def find_user_by_email(self, email: str) -> User:
        try:
            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Users WHERE email = '{email.upper()}'"
            )

            row = self.cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in self.cursor.description]
                user_dict = dict(zip(columns, row))

                user = User.create_from_persistence(user_dict)
            else:
                user = None

            return user
        except Exception as e:
            raise e

    def create_user(self, user: User) -> None:
        try:
            self.cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Users (id, name, email, password, career, semester, role, priority, created_at, updated_at) VALUES ('{user.id}', '{user.name.upper()}', '{user.email.upper()}', '{user.password}', '{user.career.upper()}', {user.semester}, '{user.role}', '{user.priority}', CAST('{str(user.created_at)}' AS DATETIME2), CAST('{str(user.updated_at)}' AS DATETIME2))"
            )
        except Exception as e:
            raise e

    def update_user(self, user: User) -> None:
        try:
            self.cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Users SET name = '{user.name.upper()}', email = '{user.email.upper()}', career = '{user.career.upper()}', semester = {user.semester}, role = '{user.role}', priority = '{user.priority}', updated_at = CAST('{str(user.updated_at)}' AS DATETIME2) WHERE id = '{user.id}'"
            )
        except Exception as e:
            raise e

    def delete_user(self, user_id: str) -> None:
        try:
            self.cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Users WHERE id = '{user_id}'"
            )
        except Exception as e:
            raise e
