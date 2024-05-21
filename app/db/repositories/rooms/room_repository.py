import base64
from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.application.rooms.room import Room
from app.db.models.persistence.rooms.room import RoomPersistence
from app.dtos.rooms.get_all_rooms_dto import GetAllRoomsDto

config = Settings()


class RoomRepository:
    database_client: DatabaseClient = DatabaseClient()

    def get_all_rooms(self) -> List[GetAllRoomsDto]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Rooms"
            )

            rooms_dto = []
            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                rooms = [Room.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                rooms = []

            for room in rooms:
                room_equipment = []
                for equipment in room.room_equipment:
                    cursor.execute(
                        f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE id = '{equipment}'"
                    )
                    row = cursor.fetchone()
                    if row is not None:
                        columns = [column[0] for column in cursor.description]
                        equipment_dict = dict(zip(columns, row))

                        room_equipment.append(equipment_dict)

                room_equipment_dto = []
                for equipment in room_equipment:
                    equipment_dto = {
                        "id": equipment["id"],
                        "name": equipment["name"],
                        "description": equipment["description"],
                        "status": equipment["status"],
                        "reservation_id": equipment["reservation_id"],
                        "image": equipment["image"],
                        "created_at": equipment["created_at"],
                        "updated_at": equipment["updated_at"]
                    }
                    room_equipment_dto.append(equipment_dto)

                room_dto = GetAllRoomsDto(
                    id=room.id,
                    name=room.name,
                    description=room.description,
                    capacity=room.capacity,
                    room_equipment=room_equipment_dto,
                    image=room.image,
                    created_at=room.created_at,
                    updated_at=room.updated_at
                )
                rooms_dto.append(room_dto)

            self.database_client.close()

            return rooms_dto
        except Exception as e:
            raise e

    def find_room_by_id(self, room_id: str) -> Room:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Rooms WHERE id = '{room_id}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                room_dict = dict(zip(columns, row))

                room = Room.create_from_persistence(room_dict)
            else:
                room = None

            self.database_client.close()

            return room
        except Exception as e:
            raise e

    def find_room_by_name(self, room_name: str) -> Room:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Rooms WHERE name = '{room_name}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                room_dict = dict(zip(columns, row))

                room = Room.create_from_persistence(room_dict)
            else:
                room = None

            self.database_client.close()

            return room
        except Exception as e:
            raise e

    def create_room(self, room: Room) -> None:
        try:
            room_persistence = RoomPersistence.create_from_application(room)

            cursor = self.database_client.get_conn()

            normalized_room_equipment = ",".join(room_persistence.room_equipment)
            cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Rooms (id, name, description, capacity, room_equipment, created_at, updated_at) VALUES ('{room_persistence.id}', '{room_persistence.name}', '{room_persistence.description}', {room_persistence.capacity}, '{normalized_room_equipment}', CAST('{room_persistence.created_at}' AS DATETIME2), CAST('{room_persistence.updated_at}' AS DATETIME2))"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

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
            raise e

    def delete_room(self, room_id: str) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Rooms WHERE id = '{room_id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e
