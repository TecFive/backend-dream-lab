from datetime import datetime, timedelta

import bcrypt
from jose import jwt

from app.core.config import Settings
from app.db.models.application.users.user import User

config = Settings()


class Security:
    @staticmethod
    def generate_jwt_token(user: User) -> str:
        try:
            return jwt.encode(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "career": user.career,
                    "semester": user.semester,
                    "role": user.role,
                    "exp": datetime.utcnow() + timedelta(days=config.JWT_EXPIRE_MINUTES),
                },
                key=config.JWT_SECRET_KEY,
                algorithm=config.JWT_ALGORITHM,
            )
        except Exception as e:
            raise e

    @staticmethod
    def hash_password(password: str) -> str:
        try:
            if password is None:
                raise Exception("Password is required.")
            elif len(password) < 8:
                raise Exception("Password must be at least 8 characters long.")

            password = password.encode("utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            return hashed_password.decode("utf-8")
        except Exception as e:
            raise e

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        try:
            if password is None:
                raise Exception("Password is required.")
            elif len(password) < 8:
                raise Exception("Password must be at least 8 characters long.")

            if hashed_password is None:
                raise Exception("Hashed password is required.")

            password = password.encode("utf-8")
            hashed_password = hashed_password.encode("utf-8")

            return bcrypt.checkpw(password, hashed_password)
        except Exception as e:
            raise e
