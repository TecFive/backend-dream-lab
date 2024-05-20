from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.reservations.reservation import Reservation

config = Settings()


class AdminRepository:
    database_client: DatabaseClient = DatabaseClient()

    def get_all_reservations(self, filter_params) -> List[Reservation]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Reservations {filter_params}"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                equipments = [Reservation.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipments = []

            self.database_client.close()

            return equipments
        except Exception as e:
            raise e
