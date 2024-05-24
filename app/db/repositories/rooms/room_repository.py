from typing import List

from fastapi import HTTPException

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.application.rooms.room import Room
from app.db.models.persistence.rooms.room_persistence import RoomPersistence
from app.db.repositories.equipments.equipment_repository import EquipmentRepository

config = Settings()


class RoomRepository:
    database_client: DatabaseClient = DatabaseClient()
    equipment_repository: EquipmentRepository = EquipmentRepository()

    def get_all_rooms(self) -> List[Room]:
        try:
            cursor = self.database_client.get_conn()

            query = f"SELECT * FROM {config.ENVIRONMENT}.Rooms"
            cursor.execute(query)

            rooms = []
            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                rooms_data = [dict(zip(columns, row)) for row in rows]

                for room in rooms_data:
                    room_equipment_ids = room["room_equipment"].split(",") if isinstance(room["room_equipment"], str) else room["room_equipment"]
                    room_equipment = [
                        self.equipment_repository.find_equipment_by_id(equipment_id).model_dump(by_alias=True)
                        for equipment_id in room_equipment_ids
                    ]

                    room["room_equipment"] = room_equipment

                    rooms.append(Room.create_from_persistence(room))
            else:
                rooms = []

            self.database_client.close()

            return rooms
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def find_room_by_id(self, room_id: str) -> Room:
        try:
            cursor = self.database_client.get_conn()

            query = f"SELECT * FROM {config.ENVIRONMENT}.Rooms WHERE id = ?"
            cursor.execute(query, room_id)

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                room_dict = dict(zip(columns, row))

                room_equipment_ids = room_dict["room_equipment"].split(",") if isinstance(room_dict["room_equipment"], str) else room_dict["room_equipment"]
                room_equipment = [
                    self.equipment_repository.find_equipment_by_id(equipment_id).model_dump(by_alias=True)
                    for equipment_id in room_equipment_ids
                ]

                room_dict["room_equipment"] = room_equipment

                room = Room.create_from_persistence(room_dict)
            else:
                room = None

            self.database_client.close()

            return room
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def find_room_by_name(self, room_name: str) -> Room:
        try:
            cursor = self.database_client.get_conn()

            query = f"SELECT * FROM {config.ENVIRONMENT}.Rooms WHERE name = ?"
            cursor.execute(query, room_name)

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                room_dict = dict(zip(columns, row))

                room_equipment_ids = room_dict["room_equipment"].split(",") if isinstance(room_dict["room_equipment"], str) else room_dict["room_equipment"]
                room_equipment = [
                    self.equipment_repository.find_equipment_by_id(equipment_id).model_dump(by_alias=True)
                    for equipment_id in room_equipment_ids
                ]

                room_dict["room_equipment"] = room_equipment

                room = Room.create_from_persistence(room_dict)
            else:
                room = None

            self.database_client.close()

            return room
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def create_room(self, room: Room) -> None:
        try:
            room_persistence = RoomPersistence.create_from_application(room)

            cursor = self.database_client.get_conn()

            normalized_room_equipment = ",".join(room_persistence.room_equipment)

            query = f"INSERT INTO {config.ENVIRONMENT}.Rooms (id, name, description, capacity, room_equipment, created_at, updated_at) VALUES (?, ?, ?, ?, ?, CAST(? AS DATETIME2), CAST(? AS DATETIME2))"
            cursor.execute(
                query,
                (
                    room_persistence.id,
                    room_persistence.name,
                    room_persistence.description,
                    room_persistence.capacity,
                    normalized_room_equipment,
                    room_persistence.created_at,
                    room_persistence.updated_at
                )
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_room(self, room: Room) -> None:
        try:
            room_persistence = RoomPersistence.create_from_application(room)

            cursor = self.database_client.get_conn()

            normalized_room_equipment = ",".join(room_persistence.room_equipment)
            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Rooms SET name = ?, description = ?, capacity = ?, room_equipment = ?, image = ?, updated_at = CAST(? AS DATETIME2) WHERE id = ?",
                (
                    room_persistence.name,
                    room_persistence.description,
                    room_persistence.capacity,
                    normalized_room_equipment,
                    room_persistence.image,
                    room_persistence.updated_at,
                    room_persistence.id
                )
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_room(self, room_id: str) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Rooms WHERE id = '{room_id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
