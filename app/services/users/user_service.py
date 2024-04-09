from datetime import datetime
from typing import List

import bson

from app.core.security import Security
from app.db.models.users.user import User
from app.db.repositories.roles.role_repository import RoleRepository
from app.db.repositories.users.user_repository import UserRepository
from app.dtos.users.create_user_dto import CreateUserDto
from app.dtos.users.update_user_dto import UpdateUserDto


class UserService:
    user_repository = UserRepository
    role_repository = RoleRepository

    def __init__(self):
        self.user_repository = UserRepository()
        self.role_repository = RoleRepository()

    def get_all_users(self) -> List[User]:
        users = self.user_repository.get_all_users()

        return users

    def get_all_users_by_career(self, career: str) -> List[User]:
        users = self.user_repository.get_all_users_by_career(career)

        return users

    def get_all_users_by_semester(self, semester: int) -> List[User]:
        users = self.user_repository.get_all_users_by_semester(semester)

        return users

    def find_user_by_id(self, user_id: str) -> User:
        user = self.user_repository.find_user_by_id(user_id)

        return user

    def find_user_by_email(self, email: str) -> User:
        user = self.user_repository.find_user_by_email(email)

        return user

    def register_user(self, create_user_dto: CreateUserDto) -> User:
        role = self.role_repository.find_role_by_name("Student")
        user = User(
            id=str(bson.ObjectId()),
            name=create_user_dto.name,
            email=create_user_dto.email,
            password=Security.hash_password(create_user_dto.password),
            career=create_user_dto.career,
            semester=create_user_dto.semester,
            role=role.id,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        self.user_repository.register_user(user)

        return user

    def update_user(self, update_user_dto: UpdateUserDto) -> User:
        user = self.find_user_by_id(update_user_dto.id)

        if user is None:
            raise Exception("User could not be found")

        user = User(
            name=update_user_dto.name,
            email=update_user_dto.email,
            career=update_user_dto.career,
            semester=update_user_dto.semester,
            updated_at=datetime.now().isoformat(),
        )

        self.user_repository.update_user(user)

        return user

    def delete_user(self, user_id: str) -> bool:
        self.user_repository.delete_user(user_id)

        return True
