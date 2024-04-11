from typing import List

from app.db.models.reservationStatus.reservationStatus import ReservationStatus
from app.db.repositories.reservationStatus.reservation_status_repositories import ReservationStatusRepository


class ReservationStatusService:
    reservation_status_repository = ReservationStatusRepository

    def __init__(self):
        self.reservation_status_repository = ReservationStatusRepository()

    def get_all_reservation_statuses(self) -> List[ReservationStatus]:
        return self.reservation_status_repository.get_all_reservation_statuses()

    def get_reservation_status_by_id(self, reservation_status_id: str) -> ReservationStatus:
        return self.reservation_status_repository.find_reservation_status_by_id(reservation_status_id)

    def get_reservation_status_by_name(self, name: str) -> ReservationStatus:
        return self.reservation_status_repository.find_reservation_status_by_name(name)

    def create_reservation_status(self, reservation_status: ReservationStatus) -> None:
        self.reservation_status_repository.create_reservation_status(reservation_status)

    def update_reservation_status(self, reservation_status: ReservationStatus) -> None:
        self.reservation_status_repository.update_reservation_status(reservation_status)

    def delete_reservation_status(self, reservation_status_id: str) -> None:
        self.reservation_status_repository.delete_reservation_status(reservation_status_id)
