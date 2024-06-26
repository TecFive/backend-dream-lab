from datetime import datetime
from typing import List

import bson
from fastapi import HTTPException

from app.db.models.application.rooms.room import Room
from app.db.repositories.rooms.room_repository import RoomRepository
from app.dtos.rooms.create_room_dto import CreateRoomDto
from app.dtos.rooms.update_room_dto import UpdateRoomDto
from app.services.equipments.equipment_service import EquipmentService


class RoomService:
    equipment_service: EquipmentService
    room_repository: RoomRepository

    def __init__(self):
        self.equipment_service = EquipmentService()
        self.room_repository = RoomRepository()

    def get_all_rooms(self) -> List[Room]:
        rooms = self.room_repository.get_all_rooms()

        return rooms

    def find_room_by_id(self, room_id: str) -> Room:
        room = self.room_repository.find_room_by_id(room_id)

        return room

    def find_room_by_name(self, room_name: str) -> Room:
        room = self.room_repository.find_room_by_name(room_name)

        return room

    def create_room(self, room_dto: CreateRoomDto) -> None:
        room_equipment = [
            self.equipment_service.find_equipment_by_id(equipment_id)
            for equipment_id in room_dto.room_equipment
        ]

        room = Room(
            id=str(bson.ObjectId()),
            name=room_dto.name,
            description=room_dto.description,
            capacity=room_dto.capacity,
            room_equipment=room_equipment,
            image=room_dto.image,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        self.room_repository.create_room(room)

    def update_room(self, room_dto: UpdateRoomDto) -> None:
        room_found = self.room_repository.find_room_by_id(room_dto.id)
        if room_found is None:
            raise HTTPException(status_code=404, detail="Room not found")

        if room_dto.name is not None:
            room_found.name = room_dto.name

        if room_dto.description is not None:
            room_found.description = room_dto.description

        if room_dto.capacity is not None:
            room_found.capacity = room_dto.capacity

        if room_dto.room_equipment is not None:
            room_equipment = [
                self.equipment_service.find_equipment_by_id(equipment_id)
                for equipment_id in room_dto.room_equipment
            ]

            room_found.room_equipment = room_equipment

        if room_dto.image is not None:
            room_found.image = room_dto.image

        room_found.updated_at = datetime.now().isoformat()

        self.room_repository.update_room(room_found)

    def add_image_to_room(self, room_id: str, image_url: str) -> None:
        room_found = self.room_repository.find_room_by_id(room_id)
        if room_found is None:
            raise HTTPException(status_code=404, detail="Room not found")

        room_found.image = image_url
        room_found.updated_at = datetime.now().isoformat()

        self.room_repository.update_room(room_found)

    def delete_room(self, room_id: str) -> None:
        self.room_repository.delete_room(room_id)
