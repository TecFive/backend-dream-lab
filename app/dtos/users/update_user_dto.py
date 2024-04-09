from pydantic import BaseModel


class UpdateUserDto(BaseModel):
    id: str
    name: str
    email: str
    career: str
    semester: int
