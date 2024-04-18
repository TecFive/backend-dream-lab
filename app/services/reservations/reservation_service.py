from datetime import datetime
from typing import List

import bson

from app.db.client import database_client
from app.db.models.reservations.reservation import Reservation
from app.db.models.users.user import User
from app.db.repositories.equipmentStatuses.equipment_status_repository import EquipmentStatusRepository
from app.db.repositories.equipments.equipment_repository import EquipmentRepository
from app.db.repositories.reservationStatus.reservation_status_repositories import ReservationStatusRepository
from app.db.repositories.reservations.reservation_repository import ReservationRepository
from app.dtos.pendingReservations.update_reservation_dto import UpdateReservationDto
from app.dtos.reservations.create_reservation_dto import CreateReservationDto
from app.dtos.reservations.get_my_reservations_dto import GetMyReservationsDto


class ReservationService:
    reservation_repository: ReservationRepository
    reservation_status_repository: ReservationStatusRepository
    equipment_status_repository: EquipmentStatusRepository
    equipment_repository: EquipmentRepository

    def __init__(self):
        self.reservation_repository = ReservationRepository()
        self.reservation_status_repository = ReservationStatusRepository()
        self.equipment_status_repository = EquipmentStatusRepository()
        self.equipment_repository = EquipmentRepository()

    def get_all_reservations(self) -> List[Reservation]:
        reservations = self.reservation_repository.get_all_reservations()
        database_client.close_connection()

        return reservations

    def get_reservations_by_room_id(self, room_id: str) -> List[Reservation]:
        reservations = self.reservation_repository.get_reservations_by_room_id(room_id)
        database_client.close_connection()

        return reservations

    def get_reservations_by_user_id(self, user_id: str) -> List[GetMyReservationsDto]:
        reservations = self.reservation_repository.get_reservations_by_user_id(user_id)
        database_client.close_connection()

        return reservations

    def get_reservation_by_id(self, reservation_id: str) -> Reservation:
        reservation = self.reservation_repository.find_reservation_by_id(reservation_id)
        database_client.close_connection()

        return reservation

    def create_reservation(self, reservation: CreateReservationDto, user: User) -> None:
        status_found = self.reservation_status_repository.find_reservation_status_by_id(reservation.status)
        if not status_found:
            raise Exception("Reservation status could not be found")

        for equipment in reservation.reserved_equipment:
            equipment_found = self.equipment_repository.find_equipment_by_id(equipment)
            if not equipment_found:
                raise Exception("Equipment could not be found")

            in_use_equipment_status_found = self.equipment_status_repository.find_equipment_status_by_name("In Use")
            available_equipment_status_found = self.equipment_status_repository.find_equipment_status_by_name("Available")
            if not in_use_equipment_status_found:
                raise Exception("Equipment status 'In Use' could not be found")

            if not available_equipment_status_found:
                raise Exception("Equipment status 'Available' could not be found")

            if equipment_found.status != available_equipment_status_found.id:
                raise Exception("Equipment is not available")

            equipment_found.status = in_use_equipment_status_found.id
            equipment_found.updated_at = datetime.now().isoformat()

            self.equipment_repository.update_equipment(equipment_found)

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

        database_client.commit()
        database_client.close_connection()

    def update_reservation(self, update_reservation_dto: UpdateReservationDto, user: User) -> None:
        reservation_found = self.reservation_repository.find_reservation_by_id(update_reservation_dto.reservation_id)
        if not reservation_found:
            raise Exception("Reservation could not be found")

        if reservation_found.user_id != user.id:
            raise Exception("You are not allowed to update this reservation")

        reservation_found.start_date = update_reservation_dto.start_date
        reservation_found.end_date = update_reservation_dto.end_date
        reservation_found.reserved_equipment = update_reservation_dto.reserved_equipment
        reservation_found.comments = update_reservation_dto.comments
        reservation_found.updated_at = datetime.now().isoformat()

        self.reservation_repository.update_reservation(reservation_found)

        database_client.commit()
        database_client.close_connection()

    def cancel_reservation(self, reservation_id: str, user: User) -> None:
        reservation_found = self.reservation_repository.find_reservation_by_id(reservation_id)
        if not reservation_found:
            raise Exception("Reservation could not be found")

        if reservation_found.user_id != user.id:
            raise Exception("You are not allowed to delete this reservation")

        status_found = self.reservation_status_repository.find_reservation_status_by_id(reservation_found.status)
        if not status_found:
            raise Exception("Current reservation status could not be found")

        if status_found.name == "Approved":
            raise Exception("You are not allowed to delete a confirmed reservation")

        canceled_status = self.reservation_status_repository.find_reservation_status_by_name("Canceled")
        if not canceled_status:
            raise Exception("Canceled reservation status could not be found")

        reservation_found.status = canceled_status.id

        self.reservation_repository.update_reservation(reservation_found)

        database_client.commit()
        database_client.close_connection()
