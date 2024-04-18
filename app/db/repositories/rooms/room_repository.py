from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.rooms.room import Room

config = Settings()
database_client = DatabaseClient()


class RoomRepository:
    @staticmethod
    def get_all_rooms() -> List[Room]:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Rooms"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                rooms = [Room.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                rooms = []

            return rooms
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def find_room_by_id(room_id: str) -> Room:
        try:
            cursor = database_client.get_conn()

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

            return room
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def find_room_by_name(room_name: str) -> Room:
        try:
            cursor = database_client.get_conn()

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

            return room
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def create_room(room: Room) -> None:
        try:
            cursor = database_client.get_conn()

            normalized_room_equipment = ",".join(room.room_equipment)
            cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Rooms (id, name, description, capacity, room_equipment, created_at, updated_at) VALUES ('{room.id}', '{room.name}', '{room.description}', {room.capacity}, '{normalized_room_equipment}', CAST('{room.created_at}' AS DATETIME2), CAST('{room.updated_at}' AS DATETIME2))"
            )
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def update_room(room: Room) -> None:
        try:
            cursor = database_client.get_conn()

            normalized_room_equipment = ",".join(room.room_equipment)
            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Rooms SET name = '{room.name}', description = '{room.description}', capacity = {room.capacity}, room_equipment = '{normalized_room_equipment}', updated_at = CAST('{room.updated_at}' AS DATETIME2) WHERE id = '{room.id}'"
            )
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def delete_room(room_id: str) -> None:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Rooms WHERE id = '{room_id}'"
            )
        except Exception as e:
            database_client.close_connection()
            raise e
