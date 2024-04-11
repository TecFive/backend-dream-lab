from pydantic import BaseModel


class UpdatePendingReservationDto(BaseModel):
    start_date: str
    end_date: str
    reserved_equipment: str
    comments: str
