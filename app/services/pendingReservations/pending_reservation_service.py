from datetime import datetime
from typing import List

import bson

from app.db.models.pendingReservations.pending_reservation import PendingReservation
from app.db.models.reservations.reservation import Reservation
from app.db.repositories.pendingReservations.pending_reservation_repository import PendingReservationRepository
from app.db.repositories.reservations.reservation_repository import ReservationRepository
from app.dtos.pendingReservations.create_pending_reservation_dto import CreatePendingReservationDto
from app.dtos.pendingReservations.update_pending_reservation_dto import UpdatePendingReservationDto


class PendingReservationService:
    pending_reservation_repository = PendingReservationRepository
    reservation_repository = ReservationRepository

    def __init__(self):
        self.pending_reservation_repository = PendingReservationRepository()

    def get_pending_reservations(self) -> List[PendingReservation]:
        reservations = self.pending_reservation_repository.get_pending_reservations()

        return reservations

    def get_pending_reservations_by_room_id(self, room_id: str) -> List[PendingReservation]:
        reservations = self.pending_reservation_repository.get_pending_reservations_by_room_id(room_id)

        return reservations

    def get_pending_reservations_by_user_id(self, user_id: str) -> List[PendingReservation]:
        reservations = self.pending_reservation_repository.get_pending_reservations_by_user_id(user_id)

        return reservations

    def get_pending_reservation_by_id(self, reservation_id: str) -> PendingReservation:
        reservation = self.pending_reservation_repository.get_pending_reservation_by_id(reservation_id)

        return reservation

    def create_pending_reservation(self, reservation: CreatePendingReservationDto, user_id: str) -> None:
        new_reservation = PendingReservation(
            id=str(bson.ObjectId()),
            user_id=user_id,
            room_id=reservation.room_id,
            start_date=reservation.start_date,
            end_date=reservation.end_date,
            reserved_equipment=reservation.reserved_equipment,
            status=reservation.status,
            comments=reservation.comments,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        self.pending_reservation_repository.create_pending_reservation(new_reservation)

    def update_pending_reservation(self, reservation: UpdatePendingReservationDto) -> None:
        pending_reservation_found = self.pending_reservation_repository.get_pending_reservation_by_id(reservation.id)

        if not pending_reservation_found:
            raise Exception("Pending reservation not found")

        pending_reservation_found.start_date = reservation.start_date
        pending_reservation_found.end_date = reservation.end_date
        pending_reservation_found.reserved_equipment = reservation.reserved_equipment
        pending_reservation_found.comments = reservation.comments

        self.pending_reservation_repository.update_pending_reservation(pending_reservation_found)

    def pending_to_confirmed(self, pending_reservation_id: str) -> str:
        pending_reservation_found = self.pending_reservation_repository.get_pending_reservation_by_id(pending_reservation_id)

        if not pending_reservation_found:
            raise Exception("Pending reservation not found")

        new_reservation = Reservation(
            id=str(bson.ObjectId()),
            user_id=pending_reservation_found.user_id,
            room_id=pending_reservation_found.room_id,
            start_date=pending_reservation_found.start_date,
            end_date=pending_reservation_found.end_date,
            reserved_equipment=pending_reservation_found.reserved_equipment,
            status="confirmed",
            comments=pending_reservation_found.comments,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        self.reservation_repository.create_reservation(new_reservation)
        self.pending_reservation_repository.delete_pending_reservation(pending_reservation_id)

        return pending_reservation_found.id

    def cancel_pending_reservation(self, pending_reservation_id: str, user_id: str) -> None:
        pending_reservation_found = self.pending_reservation_repository.get_pending_reservation_by_id(pending_reservation_id)
        if not pending_reservation_found:
            raise Exception("Pending reservation not found")

        if pending_reservation_found.user_id != user_id:
            raise Exception("You are not allowed to delete this reservation")

        self.pending_reservation_repository.delete_pending_reservation(pending_reservation_id)
