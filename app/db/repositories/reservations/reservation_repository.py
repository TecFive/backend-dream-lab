from datetime import datetime
from typing import List

import bson

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.application.reservations.reservation import Reservation
from app.db.models.persistence.reservations.reservation import ReservationPersistence
from app.db.repositories.reservationStatus.reservation_status_repositories import ReservationStatusRepository

config = Settings()


# All static methods
class ReservationRepository:
    database_client: DatabaseClient = DatabaseClient()
    reservation_status_repository: ReservationStatusRepository = ReservationStatusRepository()

    def get_all_reservations(self) -> List[Reservation]:
        try:
            cursor = self.database_client.get_conn()

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

            self.database_client.close()

            return reservations
        except Exception as e:
            raise e

    def get_reservations_by_room_id(self, room_id: str) -> List[Reservation]:
        try:
            cursor = self.database_client.get_conn()

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

            self.database_client.close()

            return reservations
        except Exception as e:
            raise e

    def get_reservations_by_user_id(self, user_id: str) -> List[Reservation]:
        try:
            cursor = self.database_client.get_conn()

            cancelled_status = self.reservation_status_repository.find_reservation_status_by_name("Cancelled")
            if cancelled_status is None:
                raise Exception("Cancelled status not found")

            cursor.execute(f"SELECT * FROM {config.ENVIRONMENT}.Reservations WHERE user_id = '{user_id}' AND status != '{cancelled_status.id}'")

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                reservations = [dict(zip(columns, row)) for row in rows]
                reservations = [Reservation.create_from_persistence(reservation) for reservation in reservations]
            else:
                reservations = []

            self.database_client.close()

            return reservations
        except Exception as e:
            raise e

    def find_reservation_by_id(self, reservation_id: str) -> Reservation:
        try:
            cursor = self.database_client.get_conn()

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

            self.database_client.close()

            return reservation
        except Exception as e:
            raise e

    def get_available_hours(self, date: str) -> List[datetime]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Reservations WHERE start_date >= '{date} 00:00:00' AND end_date <= '{date} 23:59:59'"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                reservations = [dict(zip(columns, row)) for row in rows]
                reservations = [Reservation.create_from_persistence(reservation) for reservation in reservations]
            else:
                reservations = []

            available_hours = []
            for reservation in reservations:
                available_hours.append(reservation.start_date)
                available_hours.append(reservation.end_date)

            self.database_client.close()

            return available_hours
        except Exception as e:
            raise e

    def create_reservation(self, reservation: Reservation) -> None:
        try:
            reservation_persistence = ReservationPersistence.create_from_application(reservation)

            cursor = self.database_client.get_conn()

            normalized_reserved_equipment = ",".join(reservation_persistence.reserved_equipment)

            sql_command = f"INSERT INTO [{config.ENVIRONMENT}].Reservations (id, user_id, room_id, start_date, end_date, reserved_equipment, status, comments, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (reservation_persistence.id, reservation_persistence.user_id, reservation_persistence.room_id, reservation_persistence.start_date, reservation_persistence.end_date, normalized_reserved_equipment, reservation_persistence.status, reservation_persistence.comments, reservation_persistence.created_at, reservation_persistence.updated_at)
            cursor.execute(sql_command, values)

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def update_reservation(self, reservation: Reservation) -> None:
        try:
            reservation_persistence = ReservationPersistence.create_from_application(reservation)

            cursor = self.database_client.get_conn()

            normalized_reserved_equipment = ",".join(reservation_persistence.reserved_equipment)
            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Reservations SET start_date = CAST('{reservation_persistence.start_date}' AS DATETIME2), end_date = CAST('{reservation_persistence.end_date}' AS DATETIME2), "
                f"reserved_equipment = '{normalized_reserved_equipment}', status = '{reservation_persistence.status}', comments = '{reservation_persistence.comments}', "
                f"updated_at = CAST('{str(reservation_persistence.updated_at)}' AS DATETIME2) WHERE id = '{reservation_persistence.id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def delete_reservation(self, reservation_id: str) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Reservations WHERE id = '{reservation_id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e
