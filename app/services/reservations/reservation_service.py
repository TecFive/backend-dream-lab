from datetime import datetime
from typing import List

import bson

from app.db.models.reservations.reservation import Reservation
from app.db.models.users.user import User
from app.db.repositories.reservationStatus.reservation_status_repositories import ReservationStatusRepository
from app.db.repositories.reservations.reservation_repository import ReservationRepository
from app.dtos.pendingReservations.update_reservation_dto import UpdateReservationDto
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

    def create_reservation(self, reservation: CreateReservationDto, user: User) -> None:
        status_found = self.reservation_status_repository.find_reservation_status_by_id(reservation.status)
        if not status_found:
            raise Exception("Reservation status could not be found")

        new_reservation = Reservation(
            id=str(bson.ObjectId()),
            user_id=user.id,
            room_id=reservation.room_id,
            start_date=reservation.start_date,
            end_date=reservation.end_date,
            reserved_equipment=reservation.reserved_equipment,
            status=status_found.id,
            comments=reservation.comments,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        self.reservation_repository.create_reservation(new_reservation)

    def update_reservation(self, update_reservation_dto: UpdateReservationDto, user: User) -> None:
        reservation_found = self.reservation_repository.get_reservation_by_id(update_reservation_dto.reservation_id)
        if not reservation_found:
            raise Exception("Reservation could not be found")

        if reservation_found.user_id != user.id:
            raise Exception("You are not allowed to update this reservation")

        reservation_found.start_date = update_reservation_dto.start_date
        reservation_found.end_date = update_reservation_dto.end_date
        reservation_found.reserved_equipment = update_reservation_dto.reserved_equipment
        reservation_found.comments = update_reservation_dto.comments

        self.reservation_repository.update_reservation(reservation_found)

    def delete_reservation(self, reservation_id: str) -> None:
        reservation_found = self.reservation_repository.get_reservation_by_id(reservation_id)
        if not reservation_found:
            raise Exception("Reservation could not be found")

        status_found = self.reservation_status_repository.find_reservation_status_by_id(reservation_found.status)
        if not status_found:
            raise Exception("Current reservation status could not be found")

        if status_found.name == "CONFIRMED":
            raise Exception("You are not allowed to delete a confirmed reservation")

        self.reservation_repository.delete_reservation(reservation_id)
