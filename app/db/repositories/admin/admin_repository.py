from typing import List

from fastapi import HTTPException

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.application.reservations.reservation import Reservation
from app.db.repositories.equipments.equipment_repository import EquipmentRepository
from app.db.repositories.rooms.room_repository import RoomRepository

config = Settings()


class AdminRepository:
    database_client: DatabaseClient = DatabaseClient()
    room_repository: RoomRepository = RoomRepository()
    equipment_repository: EquipmentRepository = EquipmentRepository()

    def get_all_reservations(self, filter_params) -> List[Reservation]:
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
                    {filter_params}"""
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
