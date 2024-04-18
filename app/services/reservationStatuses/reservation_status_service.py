from typing import List

from app.db.client import database_client
from app.db.models.reservationStatus.reservationStatus import ReservationStatus
from app.db.repositories.reservationStatus.reservation_status_repositories import ReservationStatusRepository


class ReservationStatusService:
    reservation_status_repository: ReservationStatusRepository

    def __init__(self):
        self.reservation_status_repository = ReservationStatusRepository()

    def get_all_reservation_statuses(self) -> List[ReservationStatus]:
        reservation_statuses = self.reservation_status_repository.get_all_reservation_statuses()
        database_client.close_connection()

        return reservation_statuses

    def get_reservation_status_by_id(self, reservation_status_id: str) -> ReservationStatus:
        reservation_status = self.reservation_status_repository.find_reservation_status_by_id(reservation_status_id)
        database_client.close_connection()

        return reservation_status

    def get_reservation_status_by_name(self, name: str) -> ReservationStatus:
        reservation_status = self.reservation_status_repository.find_reservation_status_by_name(name)
        database_client.close_connection()

        return reservation_status

    def create_reservation_status(self, reservation_status: ReservationStatus) -> None:
        self.reservation_status_repository.create_reservation_status(reservation_status)

        database_client.commit()
        database_client.close_connection()

    def update_reservation_status(self, reservation_status: ReservationStatus) -> None:
        self.reservation_status_repository.update_reservation_status(reservation_status)

        database_client.commit()
        database_client.close_connection()

    def delete_reservation_status(self, reservation_status_id: str) -> None:
        self.reservation_status_repository.delete_reservation_status(reservation_status_id)

        database_client.commit()
        database_client.close_connection()
