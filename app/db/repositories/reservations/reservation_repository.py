from datetime import datetime
from typing import List

from fastapi import HTTPException

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.application.reservations.reservation import Reservation
from app.db.models.persistence.reservations.reservation_persistence import ReservationPersistence
from app.db.repositories.equipments.equipment_repository import EquipmentRepository
from app.db.repositories.reservationStatus.reservation_status_repository import ReservationStatusRepository
from app.db.repositories.rooms.room_repository import RoomRepository

config = Settings()


# All static methods
class ReservationRepository:
    database_client: DatabaseClient = DatabaseClient()
    reservation_status_repository: ReservationStatusRepository = ReservationStatusRepository()
    room_repository: RoomRepository = RoomRepository()
    equipment_repository: EquipmentRepository = EquipmentRepository()

    def get_all_reservations(self) -> List[Reservation]:
        try:
            cursor = self.database_client.get_conn()

            query = f"""
                SELECT
                    r.id AS id,
                    u.id AS user_id,
                    u.name AS user_name,
                    u.email AS user_email,
                    u.password AS user_password,
                    u.career AS user_career,
                    u.semester AS user_semester,
                    u.role AS user_role,
                    u.priority AS user_priority,
                    u.created_at AS user_created_at,
                    u.updated_at AS user_updated_at,
                    r.room_id AS room_id,
                    r.start_date AS start_date,
                    r.end_date AS end_date,
                    r.reserved_equipment AS reserved_equipment,
                    rs.id AS status_id,
                    rs.name AS status_name,
                    rs.description AS status_description,
                    rs.created_at AS status_created_at,
                    rs.updated_at AS status_updated_at,
                    r.comments AS comments,
                    r.created_at AS created_at,
                    r.updated_at AS updated_at
                FROM {config.ENVIRONMENT}.Reservations AS r
                    INNER JOIN {config.ENVIRONMENT}.Users AS u ON u.id = r.user_id
                    INNER JOIN {config.ENVIRONMENT}.ReservationStatus AS rs ON rs.id = r.status"""
            cursor.execute(query)

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                data = [dict(zip(columns, row)) for row in rows]

                reservations = []
                if data is not None and len(data) > 0:
                    for row in data:
                        room_data = self.room_repository.find_room_by_id(row["room_id"]).model_dump(by_alias=True)

                        reserved_equipment_ids = row["reserved_equipment"].split(",")
                        reserved_equipment = [
                            self.equipment_repository.find_equipment_by_id(equipment_id).model_dump(by_alias=True)
                            for equipment_id in reserved_equipment_ids
                        ]

                        reservation_data = {
                            "id": row["id"],
                            "user": {
                                "id": row["user_id"],
                                "name": row["user_name"],
                                "email": row["user_email"],
                                "password": row["user_password"],
                                "career": row["user_career"],
                                "semester": row["user_semester"],
                                "role": row["user_role"],
                                "priority": row["user_priority"],
                                "created_at": row["user_created_at"],
                                "updated_at": row["user_updated_at"]
                            },
                            "room": room_data,
                            "start_date": row["start_date"],
                            "end_date": row["end_date"],
                            "reserved_equipment": reserved_equipment,
                            "status": {
                                "id": row["status_id"],
                                "name": row["status_name"],
                                "description": row["status_description"],
                                "created_at": row["status_created_at"],
                                "updated_at": row["status_updated_at"]
                            },
                            "comments": row["comments"],
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"]
                        }

                        reservations.append(Reservation.create_from_persistence(reservation_data))
            else:
                reservations = []

            self.database_client.close()
            return reservations
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_reservations_by_room_id(self, room_id: str) -> List[Reservation]:
        try:
            cursor = self.database_client.get_conn()

            query = f"""
                SELECT
                    r.id AS id,
                    u.id AS user_id,
                    u.name AS user_name,
                    u.email AS user_email,
                    u.password AS user_password,
                    u.career AS user_career,
                    u.semester AS user_semester,
                    u.role AS user_role,
                    u.priority AS user_priority,
                    u.created_at AS user_created_at,
                    u.updated_at AS user_updated_at,
                    r.room_id AS room_id,
                    r.start_date AS start_date,
                    r.end_date AS end_date,
                    r.reserved_equipment AS reserved_equipment,
                    rs.id AS status_id,
                    rs.name AS status_name,
                    rs.description AS status_description,
                    rs.created_at AS status_created_at,
                    rs.updated_at AS status_updated_at,
                    r.comments AS comments,
                    r.created_at AS created_at,
                    r.updated_at AS updated_at
                FROM {config.ENVIRONMENT}.Reservations AS r
                    INNER JOIN {config.ENVIRONMENT}.Users AS u ON u.id = r.user_id
                    INNER JOIN {config.ENVIRONMENT}.ReservationStatus AS rs ON rs.id = r.status
                WHERE r.room_id = ?"""
            cursor.execute(query, room_id)

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                data = [dict(zip(columns, row)) for row in rows]

                reservations = []
                if data is not None and len(data) > 0:
                    for row in data:
                        room_data = self.room_repository.find_room_by_id(row["room_id"]).model_dump(by_alias=True)

                        reserved_equipment_ids = row["reserved_equipment"].split(",")
                        reserved_equipment = [
                            self.equipment_repository.find_equipment_by_id(equipment_id).model_dump(by_alias=True)
                            for equipment_id in reserved_equipment_ids
                        ]

                        reservation_data = {
                            "id": row["id"],
                            "user": {
                                "id": row["user_id"],
                                "name": row["user_name"],
                                "email": row["user_email"],
                                "password": row["user_password"],
                                "career": row["user_career"],
                                "semester": row["user_semester"],
                                "role": row["user_role"],
                                "priority": row["user_priority"],
                                "created_at": row["user_created_at"],
                                "updated_at": row["user_updated_at"]
                            },
                            "room": room_data,
                            "start_date": row["start_date"],
                            "end_date": row["end_date"],
                            "reserved_equipment": reserved_equipment,
                            "status": {
                                "id": row["status_id"],
                                "name": row["status_name"],
                                "description": row["status_description"],
                                "created_at": row["status_created_at"],
                                "updated_at": row["status_updated_at"]
                            },
                            "comments": row["comments"],
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"]
                        }

                        reservations.append(Reservation.create_from_persistence(reservation_data))
            else:
                reservations = []

            self.database_client.close()

            return reservations
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_reservations_by_user_id(self, user_id: str) -> List[Reservation]:
        try:
            cursor = self.database_client.get_conn()

            cancelled_status = self.reservation_status_repository.find_reservation_status_by_name("Cancelled")
            if cancelled_status is None:
                raise HTTPException(status_code=404, detail="Reservation status 'Cancelled' could not be found")

            query = f"""
                SELECT
                    r.id AS id,
                    u.id AS user_id,
                    u.name AS user_name,
                    u.email AS user_email,
                    u.password AS user_password,
                    u.career AS user_career,
                    u.semester AS user_semester,
                    u.role AS user_role,
                    u.priority AS user_priority,
                    u.created_at AS user_created_at,
                    u.updated_at AS user_updated_at,
                    r.room_id AS room_id,
                    r.start_date AS start_date,
                    r.end_date AS end_date,
                    r.reserved_equipment AS reserved_equipment,
                    rs.id AS status_id,
                    rs.name AS status_name,
                    rs.description AS status_description,
                    rs.created_at AS status_created_at,
                    rs.updated_at AS status_updated_at,
                    r.comments AS comments,
                    r.created_at AS created_at,
                    r.updated_at AS updated_at
                FROM {config.ENVIRONMENT}.Reservations AS r
                    INNER JOIN {config.ENVIRONMENT}.Users AS u ON u.id = r.user_id
                    INNER JOIN {config.ENVIRONMENT}.ReservationStatus AS rs ON rs.id = r.status
                WHERE user_id = ? AND status != ?"""
            cursor.execute(query, (user_id, cancelled_status.id))

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                data = [dict(zip(columns, row)) for row in rows]

                reservations = []
                if data is not None and len(data) > 0:
                    for row in data:
                        room_data = self.room_repository.find_room_by_id(row["room_id"]).model_dump(by_alias=True)

                        reserved_equipment_ids = row["reserved_equipment"].split(",")
                        reserved_equipment = [
                            self.equipment_repository.find_equipment_by_id(equipment_id).model_dump(by_alias=True)
                            for equipment_id in reserved_equipment_ids
                        ]

                        reservation_data = {
                            "id": row["id"],
                            "user": {
                                "id": row["user_id"],
                                "name": row["user_name"],
                                "email": row["user_email"],
                                "password": row["user_password"],
                                "career": row["user_career"],
                                "semester": row["user_semester"],
                                "role": row["user_role"],
                                "priority": row["user_priority"],
                                "created_at": row["user_created_at"],
                                "updated_at": row["user_updated_at"]
                            },
                            "room": room_data,
                            "start_date": row["start_date"],
                            "end_date": row["end_date"],
                            "reserved_equipment": reserved_equipment,
                            "status": {
                                "id": row["status_id"],
                                "name": row["status_name"],
                                "description": row["status_description"],
                                "created_at": row["status_created_at"],
                                "updated_at": row["status_updated_at"]
                            },
                            "comments": row["comments"],
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"]
                        }

                        reservations.append(Reservation.create_from_persistence(reservation_data))
            else:
                reservations = []

            self.database_client.close()

            return reservations
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def find_reservation_by_id(self, reservation_id: str) -> Reservation:
        try:
            cursor = self.database_client.get_conn()

            query = f"""
                SELECT
                    r.id AS id,
                    u.id AS user_id,
                    u.name AS user_name,
                    u.email AS user_email,
                    u.password AS user_password,
                    u.career AS user_career,
                    u.semester AS user_semester,
                    u.role AS user_role,
                    u.priority AS user_priority,
                    u.created_at AS user_created_at,
                    u.updated_at AS user_updated_at,
                    r.room_id AS room_id,
                    r.start_date AS start_date,
                    r.end_date AS end_date,
                    r.reserved_equipment AS reserved_equipment,
                    rs.id AS status_id,
                    rs.name AS status_name,
                    rs.description AS status_description,
                    rs.created_at AS status_created_at,
                    rs.updated_at AS status_updated_at,
                    r.comments AS comments,
                    r.created_at AS created_at,
                    r.updated_at AS updated_at
                FROM {config.ENVIRONMENT}.Reservations AS r
                    INNER JOIN {config.ENVIRONMENT}.Users AS u ON u.id = r.user_id
                    INNER JOIN {config.ENVIRONMENT}.ReservationStatus AS rs ON rs.id = r.status
                WHERE r.id = ?"""
            cursor.execute(query, reservation_id)

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                reservation_dict = dict(zip(columns, row))

                reservation_data = {
                    "id": reservation_dict["id"],
                    "user": {
                        "id": reservation_dict["user_id"],
                        "name": reservation_dict["user_name"],
                        "email": reservation_dict["user_email"],
                        "password": reservation_dict["user_password"],
                        "career": reservation_dict["user_career"],
                        "semester": reservation_dict["user_semester"],
                        "role": reservation_dict["user_role"],
                        "priority": reservation_dict["user_priority"],
                        "created_at": reservation_dict["user_created_at"],
                        "updated_at": reservation_dict["user_updated_at"]
                    },
                    "room": self.room_repository.find_room_by_id(reservation_dict["room_id"]).model_dump(by_alias=True),
                    "start_date": reservation_dict["start_date"],
                    "end_date": reservation_dict["end_date"],
                    "reserved_equipment": [
                        self.equipment_repository.find_equipment_by_id(equipment_id).model_dump(by_alias=True)
                        for equipment_id in reservation_dict["reserved_equipment"].split(",")
                    ],
                    "status": {
                        "id": reservation_dict["status_id"],
                        "name": reservation_dict["status_name"],
                        "description": reservation_dict["status_description"],
                        "created_at": reservation_dict["status_created_at"],
                        "updated_at": reservation_dict["status_updated_at"]
                    },
                    "comments": reservation_dict["comments"],
                    "created_at": reservation_dict["created_at"],
                    "updated_at": reservation_dict["updated_at"]
                }

                reservation = Reservation.create_from_persistence(reservation_data)
            else:
                reservation = None

            self.database_client.close()

            return reservation
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_available_hours(self, date: str) -> List[datetime]:
        try:
            cursor = self.database_client.get_conn()

            query = f"""
                SELECT
                    r.id AS id,
                    u.id AS user_id,
                    u.name AS user_name,
                    u.email AS user_email,
                    u.password AS user_password,
                    u.career AS user_career,
                    u.semester AS user_semester,
                    u.role AS user_role,
                    u.priority AS user_priority,
                    u.created_at AS user_created_at,
                    u.updated_at AS user_updated_at,
                    r.room_id AS room_id,
                    r.start_date AS start_date,
                    r.end_date AS end_date,
                    r.reserved_equipment AS reserved_equipment,
                    rs.id AS status_id,
                    rs.name AS status_name,
                    rs.description AS status_description,
                    rs.created_at AS status_created_at,
                    rs.updated_at AS status_updated_at,
                    r.comments AS comments,
                    r.created_at AS created_at,
                    r.updated_at AS updated_at
                FROM {config.ENVIRONMENT}.Reservations AS r
                    INNER JOIN {config.ENVIRONMENT}.Users AS u ON u.id = r.user_id
                    INNER JOIN {config.ENVIRONMENT}.ReservationStatus AS rs ON rs.id = r.status
                WHERE start_date >= '{date} 00:00:00' AND end_date <= '{date} 23:59:59'"""
            cursor.execute(query)

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                data = [dict(zip(columns, row)) for row in rows]

                reservations = []
                if data is not None and len(data) > 0:
                    for row in data:
                        room_data = self.room_repository.find_room_by_id(row["room_id"]).model_dump(by_alias=True)

                        reserved_equipment_ids = row["reserved_equipment"].split(",")
                        reserved_equipment = [
                            self.equipment_repository.find_equipment_by_id(equipment_id).model_dump(by_alias=True)
                            for equipment_id in reserved_equipment_ids
                        ]

                        reservation_data = {
                            "id": row["id"],
                            "user": {
                                "id": row["user_id"],
                                "name": row["user_name"],
                                "email": row["user_email"],
                                "password": row["user_password"],
                                "career": row["user_career"],
                                "semester": row["user_semester"],
                                "role": row["user_role"],
                                "priority": row["user_priority"],
                                "created_at": row["user_created_at"],
                                "updated_at": row["user_updated_at"]
                            },
                            "room": room_data,
                            "start_date": row["start_date"],
                            "end_date": row["end_date"],
                            "reserved_equipment": reserved_equipment,
                            "status": {
                                "id": row["status_id"],
                                "name": row["status_name"],
                                "description": row["status_description"],
                                "created_at": row["status_created_at"],
                                "updated_at": row["status_updated_at"]
                            },
                            "comments": row["comments"],
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"]
                        }

                        reservations.append(Reservation.create_from_persistence(reservation_data))
            else:
                reservations = []

            available_hours = []
            for reservation in reservations:
                available_hours.append(reservation.start_date)
                available_hours.append(reservation.end_date)

            self.database_client.close()

            return available_hours
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def create_reservation(self, reservation: Reservation) -> None:
        try:
            reservation_persistence = ReservationPersistence.create_from_application(reservation)

            cursor = self.database_client.get_conn()

            normalized_reserved_equipment = ",".join(reservation_persistence.reserved_equipment)

            query = f"INSERT INTO [{config.ENVIRONMENT}].Reservations (id, user_id, room_id, start_date, end_date, reserved_equipment, status, comments, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(
                query,
                (
                    reservation_persistence.id, reservation_persistence.user_id, reservation_persistence.room_id,
                    reservation_persistence.start_date, reservation_persistence.end_date, normalized_reserved_equipment,
                    reservation_persistence.status, reservation_persistence.comments, reservation_persistence.created_at,
                    reservation_persistence.updated_at
                )
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_reservation(self, reservation: Reservation) -> None:
        try:
            reservation_persistence = ReservationPersistence.create_from_application(reservation)

            cursor = self.database_client.get_conn()

            normalized_reserved_equipment = ",".join(reservation_persistence.reserved_equipment)
            query = f"""
                UPDATE {config.ENVIRONMENT}.Reservations SET 
                    start_date = CAST(? AS DATETIME2), 
                    end_date = CAST(? AS DATETIME2), 
                    reserved_equipment = ?, 
                    status = ?, 
                    comments = ?, 
                    updated_at = CAST(? AS DATETIME2) 
                WHERE id = ?"""
            cursor.execute(
                query,
                (
                    reservation_persistence.start_date, reservation_persistence.end_date, normalized_reserved_equipment,
                    reservation_persistence.status, reservation_persistence.comments, reservation_persistence.updated_at,
                    reservation_persistence.id
                )
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_reservation(self, reservation_id: str) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Reservations WHERE id = '{reservation_id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
