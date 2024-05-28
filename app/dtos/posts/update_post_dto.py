from typing import Optional

from pydantic import BaseModel


class UpdatePostDto(BaseModel):
    file: Optional[str]
    title: Optional[str]
    description: Optional[str]
