from pydantic import BaseModel


class UpdateUserDto(BaseModel):
    name: str
    email: str
    career: str
    semester: int
