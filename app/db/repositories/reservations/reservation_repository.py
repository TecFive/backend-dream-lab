from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.reservations.reservation import Reservation

config = Settings()
database_client = DatabaseClient()


# All static methods
class ReservationRepository:
    @staticmethod
    def get_all_reservations() -> List[Reservation]:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.Reservations"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            reservations = [dict(zip(columns, row)) for row in rows]
            reservations = [Reservation.create_from_persistence(reservation) for reservation in reservations]
        else:
            reservations = []

        database_client.close_connection()

        return reservations

    @staticmethod
    def get_reservations_by_room_id(room_id: str) -> List[Reservation]:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.Reservations WHERE room_id = '{room_id}'"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            reservations = [dict(zip(columns, row)) for row in rows]
            reservations = [Reservation.create_from_persistence(reservation) for reservation in reservations]
        else:
            reservations = []

        database_client.close_connection()

        return reservations

    @staticmethod
    def get_reservations_by_user_id(user_id: str) -> List[Reservation]:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.Reservations WHERE id_usuario = '{user_id}'"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            reservations = [dict(zip(columns, row)) for row in rows]
            reservations = [Reservation.create_from_persistence(reservation) for reservation in reservations]
        else:
            reservations = []

        database_client.close_connection()

        return reservations

    @staticmethod
    def find_reservation_by_id(reservation_id: str) -> Reservation:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.Reservations WHERE id = '{reservation_id}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            reservation_dict = dict(zip(columns, row))

            reservation = Reservation.create_from_persistence(reservation_dict)
        else:
            reservation = None

        database_client.close_connection()

        return reservation

    @staticmethod
    def create_reservation(reservation: Reservation) -> None:
        cursor = database_client.get_conn()

        normalized_reserved_equipment = ",".join(reservation.reserved_equipment)
        cursor.execute(
            f"INSERT INTO {config.ENVIRONMENT}.Reservations (id, user_id, room_id, start_date, end_date, reserved_equipment, status, comments, created_at, updated_at) "
            f"VALUES ('{reservation.id}', '{reservation.user_id}', '{reservation.room_id}', CAST('{reservation.start_date}' AS DATETIME2), "
            f"CAST('{reservation.end_date}' AS DATETIME2), '{normalized_reserved_equipment}', '{reservation.status}', '{reservation.comments}', "
        )

        database_client.commit()
        database_client.close_connection()

    @staticmethod
    def update_reservation(reservation: Reservation) -> None:
        cursor = database_client.get_conn()

        normalized_reserved_equipment = ",".join(reservation.reserved_equipment)
        cursor.execute(
            f"UPDATE {config.ENVIRONMENT}.Reservations SET start_date = CAST('{reservation.start_date}' AS DATETIME2), end_date = CAST('{reservation.end_date}' AS DATETIME2), "
            f"reserved_equipment = '{normalized_reserved_equipment}', status = '{reservation.status}', comments = '{reservation.comments}', "
            f"updated_at = CAST('{str(reservation.updated_at)}' AS DATETIME2) WHERE id = '{reservation.id}'"
        )

        database_client.commit()
        database_client.close_connection()

    @staticmethod
    def delete_reservation(reservation_id: str) -> None:
        cursor = database_client.get_conn()

        cursor.execute(
            f"DELETE FROM {config.ENVIRONMENT}.Reservations WHERE id = '{reservation_id}'"
        )

        database_client.commit()
        database_client.close_connection()
