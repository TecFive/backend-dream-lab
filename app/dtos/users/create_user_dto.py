from pydantic import BaseModel


class CreateUserDto(BaseModel):
    name: str
    email: str
    password: str
    career: str
    semester: int
