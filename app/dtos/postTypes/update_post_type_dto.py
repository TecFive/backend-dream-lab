from pydantic import BaseModel


class UpdatePostTypeDto(BaseModel):
    name: str
    displayName: str
