import base64
from typing import List

from app.core.config import Settings
from app.db.client import database_client
from app.db.models.rooms.room import Room

config = Settings()


class RoomRepository:
    cursor = database_client.get_conn()

    def get_all_rooms(self) -> List[Room]:
        try:
            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Rooms"
            )

            rows = self.cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in self.cursor.description]
                rooms = [Room.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                rooms = []

            return rooms
        except Exception as e:
            raise e

    def find_room_by_id(self, room_id: str) -> Room:
        try:
            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Rooms WHERE id = '{room_id}'"
            )

            row = self.cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in self.cursor.description]
                room_dict = dict(zip(columns, row))

                room = Room.create_from_persistence(room_dict)
            else:
                room = None

            return room
        except Exception as e:
            raise e

    def find_room_by_name(self, room_name: str) -> Room:
        try:
            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Rooms WHERE name = '{room_name}'"
            )

            row = self.cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in self.cursor.description]
                room_dict = dict(zip(columns, row))

                room = Room.create_from_persistence(room_dict)
            else:
                room = None

            return room
        except Exception as e:
            raise e

    def create_room(self, room: Room) -> None:
        try:
            normalized_room_equipment = ",".join(room.room_equipment)
            self.cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Rooms (id, name, description, capacity, room_equipment, created_at, updated_at) VALUES ('{room.id}', '{room.name}', '{room.description}', {room.capacity}, '{normalized_room_equipment}', CAST('{room.created_at}' AS DATETIME2), CAST('{room.updated_at}' AS DATETIME2))"
            )
        except Exception as e:
            raise e

    def update_room(self, room: Room) -> None:
        try:
            normalized_room_equipment = ",".join(room.room_equipment)
            self.cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Rooms SET name = ?, description = ?, capacity = ?, room_equipment = ?, image = ?, updated_at = CAST(? AS DATETIME2) WHERE id = ?",
                (
                    room.name,
                    room.description,
                    room.capacity,
                    normalized_room_equipment,
                    room.image,
                    room.updated_at,
                    room.id
                )
            )
        except Exception as e:
            raise e

    def delete_room(self, room_id: str) -> None:
        try:
            self.cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Rooms WHERE id = '{room_id}'"
            )
        except Exception as e:
            raise e
