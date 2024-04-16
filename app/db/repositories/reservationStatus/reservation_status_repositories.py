from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.reservationStatus.reservationStatus import ReservationStatus

config = Settings()
database_client = DatabaseClient()


class ReservationStatusRepository:
    @staticmethod
    def get_all_reservation_statuses() -> List[ReservationStatus]:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.ReservationStatus"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            reservation_statuses = [dict(zip(columns, row)) for row in rows]
            reservation_statuses = [ReservationStatus.create_from_persistence(reservationStatus) for reservationStatus in reservation_statuses]
        else:
            reservation_statuses = []

        database_client.close_connection()

        return reservation_statuses

    @staticmethod
    def find_reservation_status_by_id(reservation_status_id: str) -> ReservationStatus:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.ReservationStatus WHERE id = '{reservation_status_id}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            reservation_status_dict = dict(zip(columns, row))

            reservation_status = ReservationStatus.create_from_persistence(reservation_status_dict)
        else:
            reservation_status = None

        database_client.close_connection()

        return reservation_status

    @staticmethod
    def find_reservation_status_by_name(reservation_status_name: str) -> ReservationStatus:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.ReservationStatus WHERE name = '{reservation_status_name.upper()}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            reservation_status_dict = dict(zip(columns, row))

            reservation_status = ReservationStatus.create_from_persistence(reservation_status_dict)
        else:
            reservation_status = None

        database_client.close_connection()

        return reservation_status

    @staticmethod
    def create_reservation_status(reservation_status: ReservationStatus) -> None:
        cursor = database_client.get_conn()

        cursor.execute(
            f"INSERT INTO {config.ENVIRONMENT}.ReservationStatus (id, name, description, created_at, updated_at) VALUES ('{reservation_status.id}', '{reservation_status.name}', '{reservation_status.description}', CAST('{reservation_status.created_at}' AS DATETIME2), CAST('{reservation_status.updated_at}' AS DATETIME2))"
        )

        database_client.commit()
        database_client.close_connection()

    @staticmethod
    def update_reservation_status(reservation_status: ReservationStatus) -> None:
        cursor = database_client.get_conn()

        cursor.execute(
            f"UPDATE {config.ENVIRONMENT}.ReservationStatus SET name = '{reservation_status.name}', description = '{reservation_status.description}', updated_at = CAST('{reservation_status.updated_at}' AS DATETIME2) WHERE id = '{reservation_status.id}'"
        )

        database_client.commit()
        database_client.close_connection()

    @staticmethod
    def delete_reservation_status(reservation_status_id: str) -> None:
        cursor = database_client.get_conn()

        cursor.execute(
            f"DELETE FROM {config.ENVIRONMENT}.ReservationStatus WHERE id = '{reservation_status_id}'"
        )

        database_client.commit()
        database_client.close_connection()
