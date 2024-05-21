from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.application.users.user import User
from app.db.models.persistence.users.user import UserPersistence

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
            user_persistence = UserPersistence.create_from_application(user)

            cursor = self.database_client.get_conn()

            cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Users (id, name, email, password, career, semester, role, priority, created_at, updated_at) VALUES ('{user_persistence.id}', '{user_persistence.name.upper()}', '{user_persistence.email.upper()}', '{user_persistence.password}', '{user_persistence.career.upper()}', {user_persistence.semester}, '{user_persistence.role}', '{user_persistence.priority}', CAST('{str(user_persistence.created_at)}' AS DATETIME2), CAST('{str(user_persistence.updated_at)}' AS DATETIME2))"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def update_user(self, user: User) -> None:
        try:
            user_persistence = UserPersistence.create_from_application(user)

            cursor = self.database_client.get_conn()

            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Users SET name = '{user_persistence.name.upper()}', email = '{user_persistence.email.upper()}', career = '{user_persistence.career.upper()}', semester = {user_persistence.semester}, role = '{user_persistence.role}', priority = '{user_persistence.priority}', updated_at = CAST('{str(user_persistence.updated_at)}' AS DATETIME2) WHERE id = '{user_persistence.id}'"
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
