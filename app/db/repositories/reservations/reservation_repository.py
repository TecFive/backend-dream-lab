from app.db.client import get_conn
from app.db.models.reservations.reservation import Reservation


# All static methods
class ReservationRepository:
    @staticmethod
    def get_all_reservations():
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Reservations"
        )

        reservations = cursor.fetchall()
        connection.close()

        return reservations

    @staticmethod
    def get_reservations_by_room_id(room_id: str):
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Reservations WHERE room_id = '{room_id}'"
        )

        reservations = cursor.fetchall()
        connection.close()

        return reservations

    @staticmethod
    def get_reservations_by_user_id(user_id: str):
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Reservations WHERE id_usuario = '{user_id}'"
        )

        reservations = cursor.fetchall()
        connection.close()

        return reservations

    @staticmethod
    def get_reservation_by_id(reservation_id: str):
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM Reservations WHERE id = '{reservation_id}'"
        )

        reservation = cursor.fetchone()
        connection.close()

        return reservation

    @staticmethod
    def create_reservation(reservation: Reservation):
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"INSERT INTO Reservations (id, user_id, room_id, start_date, end_date, status, comments, updated_at) "
            f"VALUES ('{reservation.id}', '{reservation.user_id}', '{reservation.room_id}', '{reservation.start_date}', "
            f"'{reservation.end_date}', '{reservation.status}', '{reservation.comments}', '{reservation.updated_at}')"
        )

        connection.commit()
        connection.close()

        return reservation

    @staticmethod
    def delete_reservation(reservation_id: str):
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"DELETE FROM Reservations WHERE id = '{reservation_id}'"
        )

        connection.commit()
        connection.close()

    @staticmethod
    def update_reservation(reservation_id: str, reservation: Reservation):
        connection = get_conn()
        cursor = connection.cursor()

        cursor.execute(
            f"UPDATE Reservations SET id = '{reservation.id}', user_id = '{reservation.user_id}', room_id = '{reservation.room_id}', "
            f"start_date = '{reservation.start_date}', end_date = '{reservation.end_date}', status = '{reservation.status}', "
            f"comments = '{reservation.comments}', updated_at = '{reservation.updated_at}' WHERE id = '{reservation_id}'"
        )

        connection.commit()
        connection.close()

        return reservation
