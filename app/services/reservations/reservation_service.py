from datetime import datetime
from typing import List

import bson

from app.db.models.reservations.reservation import Reservation
from app.db.models.users.user import User
from app.db.repositories.equipmentStatuses.equipment_status_repository import EquipmentStatusRepository
from app.db.repositories.equipments.equipment_repository import EquipmentRepository
from app.db.repositories.reservationStatus.reservation_status_repositories import ReservationStatusRepository
from app.db.repositories.reservations.reservation_repository import ReservationRepository
from app.db.repositories.rooms.room_repository import RoomRepository
from app.dtos.reservations.create_reservation_dto import CreateReservationDto
from app.dtos.reservations.get_my_reservations_dto import GetMyReservationsDto
from app.dtos.reservations.reservation_equipment_detail_dto import ReservationEquipmentDetailDto
from app.dtos.reservations.update_reservation_dto import UpdateReservationDto


class ReservationService:
    reservation_repository: ReservationRepository
    reservation_status_repository: ReservationStatusRepository
    equipment_status_repository: EquipmentStatusRepository
    equipment_repository: EquipmentRepository
    room_repository: RoomRepository

    def __init__(self):
        self.reservation_repository = ReservationRepository()
        self.reservation_status_repository = ReservationStatusRepository()
        self.equipment_status_repository = EquipmentStatusRepository()
        self.equipment_repository = EquipmentRepository()
        self.room_repository = RoomRepository()

    def get_all_reservations(self) -> List[Reservation]:
        reservations = self.reservation_repository.get_all_reservations()

        return reservations

    def get_reservations_by_room_id(self, room_id: str) -> List[Reservation]:
        reservations = self.reservation_repository.get_reservations_by_room_id(room_id)

        return reservations

    def get_reservations_by_user_id(self, user_id: str) -> List[GetMyReservationsDto]:
        reservations = self.reservation_repository.get_reservations_by_user_id(user_id)

        reservations_dto = []
        for reservation in reservations:
            equipment_dto = []

            if len(reservation.reserved_equipment[0]) != 0:
                for equipment in reservation.reserved_equipment:
                    data = self.equipment_repository.find_equipment_by_id(equipment)
                    equipment_dto.append(ReservationEquipmentDetailDto(
                        id=data.id,
                        name=data.name
                    ))

            room_data = self.room_repository.find_room_by_id(reservation.room_id)
            status_data = self.reservation_status_repository.find_reservation_status_by_id(reservation.status)

            reservations_dto.append(GetMyReservationsDto(
                id=reservation.id,
                name=room_data.name,
                room_image=room_data.image,
                status=status_data.name,
                start_date=reservation.start_date,
                end_date=reservation.end_date,
                reserved_equipment=equipment_dto
            ))

        return reservations_dto

    def get_reservation_by_id(self, reservation_id: str) -> Reservation:
        reservation = self.reservation_repository.find_reservation_by_id(reservation_id)

        return reservation

    def get_available_hours(self, date: str) -> List[datetime]:
        available_hours = self.reservation_repository.get_available_hours(date)

        return available_hours

    def create_reservation(self, reservation: CreateReservationDto, user: User) -> None:
        status_found = self.reservation_status_repository.find_reservation_status_by_name("Pending")
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

    def cancel_reservation(self, reservation_id: str, user: User) -> None:
        reservation_found = self.reservation_repository.find_reservation_by_id(reservation_id)
        if not reservation_found:
            raise Exception("Reservation could not be found")

        if reservation_found.user_id != user.id:
            raise Exception("You are not allowed to delete this reservation")

        status_found = self.reservation_status_repository.find_reservation_status_by_id(reservation_found.status)
        if not status_found:
            raise Exception("Current reservation status could not be found")

        cancelled_status = self.reservation_status_repository.find_reservation_status_by_name("Cancelled")
        if not cancelled_status:
            raise Exception("Canceled reservation status could not be found")

        reservation_found.status = cancelled_status.id

        self.reservation_repository.update_reservation(reservation_found)
