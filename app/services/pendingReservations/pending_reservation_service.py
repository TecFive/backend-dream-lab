from datetime import datetime
from typing import List

import bson

from app.db.client import database_client
from app.db.models.pendingReservations.pending_reservation import PendingReservation
from app.db.models.reservations.reservation import Reservation
from app.db.repositories.equipmentStatuses.equipment_status_repository import EquipmentStatusRepository
from app.db.repositories.equipments.equipment_repository import EquipmentRepository
from app.db.repositories.pendingReservations.pending_reservation_repository import PendingReservationRepository
from app.db.repositories.reservationStatus.reservation_status_repositories import ReservationStatusRepository
from app.db.repositories.reservations.reservation_repository import ReservationRepository
from app.dtos.pendingReservations.create_pending_reservation_dto import CreatePendingReservationDto
from app.dtos.pendingReservations.update_pending_reservation_dto import UpdatePendingReservationDto


class PendingReservationService:
    pending_reservation_repository: PendingReservationRepository
    reservation_repository: ReservationRepository
    reservation_status_repository: ReservationStatusRepository
    equipment_status_repository: EquipmentStatusRepository
    equipment_repository: EquipmentRepository

    def __init__(self):
        self.pending_reservation_repository = PendingReservationRepository()
        self.reservation_repository = ReservationRepository()
        self.reservation_status_repository = ReservationStatusRepository()
        self.equipment_status_repository = EquipmentStatusRepository()
        self.equipment_repository = EquipmentRepository()

    def get_pending_reservations(self) -> List[PendingReservation]:
        reservations = self.pending_reservation_repository.get_pending_reservations()
        database_client.close_connection()

        return reservations

    def get_pending_reservations_by_room_id(self, room_id: str) -> List[PendingReservation]:
        reservations = self.pending_reservation_repository.get_pending_reservations_by_room_id(room_id)
        database_client.close_connection()

        return reservations

    def get_pending_reservations_by_user_id(self, user_id: str) -> List[PendingReservation]:
        reservations = self.pending_reservation_repository.get_pending_reservations_by_user_id(user_id)
        database_client.close_connection()

        return reservations

    def get_pending_reservation_by_id(self, reservation_id: str) -> PendingReservation:
        reservation = self.pending_reservation_repository.find_pending_reservation_by_id(reservation_id)
        database_client.close_connection()

        return reservation

    def create_pending_reservation(self, reservation: CreatePendingReservationDto, user_id: str) -> None:
        status_found = self.reservation_status_repository.find_reservation_status_by_id(reservation.status)
        if not status_found:
            raise Exception("Reservation status could not be found")

        for equipment in reservation.reserved_equipment:
            equipment_found = self.equipment_repository.find_equipment_by_id(equipment)
            if not equipment_found:
                raise Exception("Equipment could not be found")

            available_equipment_status_found = self.equipment_status_repository.find_equipment_status_by_name("Available")
            if not available_equipment_status_found:
                raise Exception("Equipment status 'Available' could not be found")

            if equipment_found.status != available_equipment_status_found.id:
                raise Exception("Equipment is not available")

        new_reservation = PendingReservation(
            id=str(bson.ObjectId()),
            user_id=user_id,
            room_id=reservation.room_id,
            start_date=reservation.start_date,
            end_date=reservation.end_date,
            reserved_equipment=reservation.reserved_equipment,
            status=status_found.id,
            comments=reservation.comments,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        self.pending_reservation_repository.create_pending_reservation(new_reservation)

        database_client.commit()
        database_client.close_connection()

    def update_pending_reservation(self, reservation: UpdatePendingReservationDto) -> None:
        pending_reservation_found = self.pending_reservation_repository.find_pending_reservation_by_id(reservation.id)
        if not pending_reservation_found:
            raise Exception("Pending reservation not found")

        for equipment in reservation.reserved_equipment:
            equipment_found = self.equipment_repository.find_equipment_by_id(equipment)
            if not equipment_found:
                raise Exception("Equipment could not be found")

            available_equipment_status_found = self.equipment_status_repository.find_equipment_status_by_name("Available")
            if not available_equipment_status_found:
                raise Exception("Equipment status 'Available' could not be found")

            if equipment_found.status != available_equipment_status_found.id:
                raise Exception("Equipment is not available")

        pending_reservation_found.start_date = reservation.start_date
        pending_reservation_found.end_date = reservation.end_date
        pending_reservation_found.reserved_equipment = reservation.reserved_equipment
        pending_reservation_found.comments = reservation.comments
        pending_reservation_found.updated_at = datetime.now().isoformat()

        self.pending_reservation_repository.update_pending_reservation(pending_reservation_found)

        database_client.commit()
        database_client.close_connection()

    def pending_to_confirmed(self, pending_reservation_id: str) -> str:
        pending_reservation_found = self.pending_reservation_repository.find_pending_reservation_by_id(pending_reservation_id)
        if not pending_reservation_found:
            raise Exception("Pending reservation not found")

        approved_status_found = self.reservation_status_repository.find_reservation_status_by_name("Approved")
        if not approved_status_found:
            raise Exception("Reservation status 'Approved' could not be found")

        for equipment in pending_reservation_found.reserved_equipment:
            equipment_found = self.equipment_repository.find_equipment_by_id(equipment)
            if not equipment_found:
                raise Exception("Equipment could not be found")

            available_equipment_status_found = self.equipment_status_repository.find_equipment_status_by_name("Available")
            if not available_equipment_status_found:
                raise Exception("Equipment status 'Available' could not be found")

            if equipment_found.status != available_equipment_status_found.id:
                raise Exception("Equipment is not available")

            equipment_found.status = approved_status_found.id
            self.equipment_repository.update_equipment(equipment_found)

        new_reservation = Reservation(
            id=str(bson.ObjectId()),
            user_id=pending_reservation_found.user_id,
            room_id=pending_reservation_found.room_id,
            start_date=pending_reservation_found.start_date,
            end_date=pending_reservation_found.end_date,
            reserved_equipment=pending_reservation_found.reserved_equipment,
            status=approved_status_found.id,
            comments=pending_reservation_found.comments,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        self.reservation_repository.create_reservation(new_reservation)
        self.pending_reservation_repository.delete_pending_reservation(pending_reservation_id)

        database_client.commit()
        database_client.close_connection()

        return pending_reservation_found.id

    def cancel_pending_reservation(self, pending_reservation_id: str, user_id: str) -> None:
        pending_reservation_found = self.pending_reservation_repository.find_pending_reservation_by_id(pending_reservation_id)
        if not pending_reservation_found:
            raise Exception("Pending reservation not found")

        if pending_reservation_found.user_id != user_id:
            raise Exception("You are not allowed to delete this reservation")

        self.pending_reservation_repository.delete_pending_reservation(pending_reservation_id)

        database_client.commit()
        database_client.close_connection()
