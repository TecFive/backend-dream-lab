from typing import List

from app.db.models.reservations.reservation import Reservation
from app.db.repositories.reservationStatus.reservation_status_repositories import ReservationStatusRepository
from app.db.repositories.reservations.reservation_repository import ReservationRepository
from app.dtos.reservations.create_reservation_dto import CreateReservationDto


class ReservationService:
    reservation_repository = ReservationRepository
    reservation_status_repository = ReservationStatusRepository

    def __init__(self):
        self.reservation_repository = ReservationRepository()
        self.reservation_status_repository = ReservationStatusRepository()

    def get_all_reservations(self) -> List[Reservation]:
        reservations = self.reservation_repository.get_all_reservations()

        return reservations

    def get_reservations_by_room_id(self, room_id: str) -> List[Reservation]:
        reservations = self.reservation_repository.get_reservations_by_room_id(room_id)

        return reservations

    def get_reservations_by_user_id(self, user_id: str) -> List[Reservation]:
        reservations = self.reservation_repository.get_reservations_by_user_id(user_id)

        return reservations

    def get_reservation_by_id(self, reservation_id: str) -> Reservation:
        reservation = self.reservation_repository.get_reservation_by_id(reservation_id)

        return reservation

    def create_reservation(self, reservation: CreateReservationDto) -> None:
        status_found = self.reservation_status_repository.find_reservation_status_by_id(reservation.status)

        new_reservation = Reservation(
            room_id=reservation.room_id,
            user_id=reservation.user_id,
            start_date=reservation.start_date,
            end_date=reservation.end_date,
            status=status_found.id
        )

        self.reservation_repository.create_reservation(new_reservation)

    def update_reservation(self, reservation: Reservation) -> None:
        self.reservation_repository.update_reservation(reservation.id, reservation)

    def delete_reservation(self, reservation_id: str) -> None:
        self.reservation_repository.delete_reservation(reservation_id)
