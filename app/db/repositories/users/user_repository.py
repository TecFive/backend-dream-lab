from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.users.user import User

config = Settings()


class UserRepository:
    database_client: DatabaseClient = DatabaseClient()

    def get_all_users(self) -> List[User]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Users"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                users = [dict(zip(columns, row)) for row in rows]
                users = [User.create_from_persistence(user) for user in users]
            else:
                users = []

            self.database_client.close()

            return users
        except Exception as e:
            raise e

    def get_all_users_by_career(self, career: str) -> List[User]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Users WHERE career = '{career.upper()}'"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                users = [dict(zip(columns, row)) for row in rows]
                users = [User.create_from_persistence(user) for user in users]
            else:
                users = []

            self.database_client.close()

            return users
        except Exception as e:
            raise e

    def get_all_users_by_semester(self, semester: int) -> List[User]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Users WHERE semester = {semester}"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                users = [dict(zip(columns, row)) for row in rows]
                users = [User.create_from_persistence(user) for user in users]
            else:
                users = []

            self.database_client.close()

            return users
        except Exception as e:
            raise e

    def find_user_by_id(self, user_id: str) -> User:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Users WHERE id = '{user_id}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                user_dict = dict(zip(columns, row))

                user = User.create_from_persistence(user_dict)
            else:
                user = None

            self.database_client.close()

            return user
        except Exception as e:
            raise e

    def find_user_by_email(self, email: str) -> User:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Users WHERE email = '{email.upper()}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                user_dict = dict(zip(columns, row))

                user = User.create_from_persistence(user_dict)
            else:
                user = None

            self.database_client.close()

            return user
        except Exception as e:
            raise e

    def create_user(self, user: User) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Users (id, name, email, password, career, semester, role, priority, created_at, updated_at) VALUES ('{user.id}', '{user.name.upper()}', '{user.email.upper()}', '{user.password}', '{user.career.upper()}', {user.semester}, '{user.role}', '{user.priority}', CAST('{str(user.created_at)}' AS DATETIME2), CAST('{str(user.updated_at)}' AS DATETIME2))"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def update_user(self, user: User) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Users SET name = '{user.name.upper()}', email = '{user.email.upper()}', career = '{user.career.upper()}', semester = {user.semester}, role = '{user.role}', priority = '{user.priority}', updated_at = CAST('{str(user.updated_at)}' AS DATETIME2) WHERE id = '{user.id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def delete_user(self, user_id: str) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Users WHERE id = '{user_id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e
