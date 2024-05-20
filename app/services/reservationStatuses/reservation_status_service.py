from typing import List

from app.db.models.application.reservationStatus.reservationStatus import ReservationStatus
from app.db.repositories.reservationStatus.reservation_status_repositories import ReservationStatusRepository


class ReservationStatusService:
    reservation_status_repository: ReservationStatusRepository

    def __init__(self):
        self.reservation_status_repository = ReservationStatusRepository()

    def get_all_reservation_statuses(self) -> List[ReservationStatus]:
        reservation_statuses = self.reservation_status_repository.get_all_reservation_statuses()

        return reservation_statuses

    def get_reservation_status_by_id(self, reservation_status_id: str) -> ReservationStatus:
        reservation_status = self.reservation_status_repository.find_reservation_status_by_id(reservation_status_id)

        return reservation_status

    def get_reservation_status_by_name(self, name: str) -> ReservationStatus:
        reservation_status = self.reservation_status_repository.find_reservation_status_by_name(name)

        return reservation_status

    def create_reservation_status(self, reservation_status: ReservationStatus) -> None:
        self.reservation_status_repository.create_reservation_status(reservation_status)

    def update_reservation_status(self, reservation_status: ReservationStatus) -> None:
        self.reservation_status_repository.update_reservation_status(reservation_status)

    def delete_reservation_status(self, reservation_status_id: str) -> None:
        self.reservation_status_repository.delete_reservation_status(reservation_status_id)
