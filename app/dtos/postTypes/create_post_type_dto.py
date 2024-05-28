from pydantic import BaseModel


class CreatePostTypeDto(BaseModel):
    name: str
    displayName: str
