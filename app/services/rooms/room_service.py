from datetime import datetime
from typing import List

import bson

from app.db.client import database_client
from app.db.models.rooms.room import Room
from app.db.repositories.rooms.room_repository import RoomRepository
from app.dtos.rooms.create_room_dto import CreateRoomDto
from app.dtos.rooms.update_room_dto import UpdateRoomDto


class RoomService:
    room_repository: RoomRepository

    def __init__(self):
        self.room_repository = RoomRepository()

    def get_all_rooms(self) -> List[Room]:
        rooms = self.room_repository.get_all_rooms()
        database_client.close_connection()

        return rooms

    def find_room_by_id(self, room_id: str) -> Room:
        room = self.room_repository.find_room_by_id(room_id)
        database_client.close_connection()

        return room

    def find_room_by_name(self, room_name: str) -> Room:
        room = self.room_repository.find_room_by_name(room_name)
        database_client.close_connection()

        return room

    def create_room(self, room_dto: CreateRoomDto) -> None:
        room = Room(
            id=str(bson.ObjectId()),
            name=room_dto.name,
            description=room_dto.description,
            capacity=room_dto.capacity,
            room_equipment=room_dto.room_equipment,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        self.room_repository.create_room(room)

        database_client.commit()
        database_client.close_connection()

    def update_room(self, room_dto: UpdateRoomDto) -> None:
        room_found = self.room_repository.find_room_by_id(room_dto.id)
        if room_found is None:
            raise Exception("Room not found.")

        room_found.name = room_dto.name
        room_found.description = room_dto.description
        room_found.capacity = room_dto.capacity
        room_found.room_equipment = room_dto.room_equipment
        room_found.updated_at = datetime.now().isoformat()

        self.room_repository.update_room(room_found)

        database_client.commit()
        database_client.close_connection()

    def delete_room(self, room_id: str) -> None:
        self.room_repository.delete_room(room_id)

        database_client.commit()
        database_client.close_connection()
