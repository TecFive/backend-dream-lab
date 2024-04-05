from pydantic import BaseModel


class Reservation(BaseModel):
    id: str

    def __init__(self, **data: Any):
        super().__init__(**data)

    @staticmethod
    def create_from_persistence(user_persistence) -> "Reservation":
        return Reservation(
            id=user_persistence["_id"]
        )
