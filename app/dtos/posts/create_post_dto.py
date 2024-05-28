from pydantic import BaseModel


class CreatePostDto(BaseModel):
    file: str
    title: str
    description: str
    type: str
