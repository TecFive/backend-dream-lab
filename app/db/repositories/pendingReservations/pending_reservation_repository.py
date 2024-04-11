from typing import List

from app.db.client import get_conn
from app.db.models.pendingReservations.pending_reservation import PendingReservation


class PendingReservationRepository:
    @staticmethod
    def get_pending_reservations() -> List[PendingReservation]:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM PendingReservations")

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            reservations = [dict(zip(columns, row)) for row in rows]
            reservations = [PendingReservation.create_from_persistence(user) for user in reservations]
        else:
            reservations = []

        connection.close()

        return reservations

    @staticmethod
    def get_pending_reservations_by_room_id(room_id: str) -> List[PendingReservation]:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM PendingReservations WHERE room_id = '{room_id}'"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            reservations = [dict(zip(columns, row)) for row in rows]
            reservations = [PendingReservation.create_from_persistence(user) for user in reservations]
        else:
            reservations = []

        connection.close()

        return reservations

    @staticmethod
    def get_pending_reservations_by_user_id(user_id: str) -> List[PendingReservation]:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM PendingReservations WHERE user_id = '{user_id}'"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            reservations = [dict(zip(columns, row)) for row in rows]
            reservations = [PendingReservation.create_from_persistence(user) for user in reservations]
        else:
            reservations = []

        connection.close()

        return reservations

    @staticmethod
    def get_pending_reservation_by_id(pending_reservation_id: str) -> PendingReservation:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM PendingReservations WHERE id = '{pending_reservation_id}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            reservation_dict = dict(zip(columns, row))

            reservation = PendingReservation.create_from_persistence(reservation_dict)
        else:
            reservation = None

        connection.close()

        return reservation

    @staticmethod
    def create_pending_reservation(pending_reservation: PendingReservation) -> None:
        connection = get_conn()
        cursor = connection.cursor()

        normalized_reserved_equipment = ",".join(pending_reservation.reserved_equipment)
        cursor.execute(
            f"INSERT INTO PendingReservations (id, room_id, user_id, start_date, end_date, reserved_equipment, status, comments, created_at, updated_at) VALUES ('{pending_reservation.id}', '{pending_reservation.room_id}', '{pending_reservation.user_id}', CAST('{pending_reservation.start_date}' AS DATETIME2), CAST('{pending_reservation.end_date}' AS DATETIME2), '{normalized_reserved_equipment}', '{pending_reservation.status}', '{pending_reservation.comments}', CAST('{str(pending_reservation.created_at)}' AS DATETIME2), CAST('{str(pending_reservation.updated_at)}' AS DATETIME2))"
        )

        connection.commit()
        connection.close()

    @staticmethod
    def update_pending_reservation(pending_reservation: PendingReservation) -> None:
        connection = get_conn()
        cursor = connection.cursor()

        normalized_reserved_equipment = ",".join(pending_reservation.reserved_equipment)
        cursor.execute(
            f"UPDATE PendingReservations SET start_date = CAST('{pending_reservation.start_date}' AS DATETIME2), end_date = CAST('{pending_reservation.end_date}' AS DATETIME2), reserved_equipment = '{normalized_reserved_equipment}', status = '{pending_reservation.status}', comments = '{pending_reservation.comments}', updated_at = CAST('{str(pending_reservation.updated_at)}' AS DATETIME2) WHERE id = '{pending_reservation.id}'"
        )

        connection.commit()
        connection.close()

    @staticmethod
    def delete_pending_reservation(pending_reservation_id: str) -> None:
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"DELETE FROM PendingReservations WHERE id = '{pending_reservation_id}'"
        )

        connection.commit()
        connection.close()

    @staticmethod
    def pending_to_confirmed(pending_reservation_id: str) -> str:
        pass
