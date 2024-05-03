from pydantic import BaseModel


class UpdateReservationDto(BaseModel):
    reservation_id: str
    start_date: str
    end_date: str
    reserved_equipment: list[str]
    comments: str
