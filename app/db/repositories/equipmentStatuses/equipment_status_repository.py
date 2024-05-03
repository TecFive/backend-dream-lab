from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.equipmentStatuses.equipment_status import EquipmentStatus

config = Settings()


class EquipmentStatusRepository:
    database_client: DatabaseClient = DatabaseClient()

    def get_all_equipment_statuses(self) -> List[EquipmentStatus]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.EquipmentStatus"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                equipment_statuses = [EquipmentStatus.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipment_statuses = []

            self.database_client.close()

            return equipment_statuses
        except Exception as e:
            raise e

    def find_equipment_status_by_id(self, equipment_status_id: str) -> EquipmentStatus:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.EquipmentStatus WHERE id = '{equipment_status_id}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                equipment_status = EquipmentStatus.create_from_persistence(dict(zip(columns, row)))
            else:
                equipment_status = {}

            self.database_client.close()

            return equipment_status
        except Exception as e:
            raise e

    def find_equipment_status_by_name(self, equipment_status_name: str) -> EquipmentStatus:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.EquipmentStatus WHERE name = '{equipment_status_name}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                equipment_status = EquipmentStatus.create_from_persistence(dict(zip(columns, row)))
            else:
                equipment_status = {}

            self.database_client.close()

            return equipment_status
        except Exception as e:
            raise e

    def create_equipment_status(self, equipment_status: EquipmentStatus) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.EquipmentStatus (id, name, description, created_at, updated_at) VALUES ('{equipment_status.id}', '{equipment_status.name}', '{equipment_status.description}', CAST('{equipment_status.created_at}' AS DATETIME2), CAST('{equipment_status.updated_at}' AS DATETIME2))"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def update_equipment_status(self, equipment_status: EquipmentStatus) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.EquipmentStatus SET name = '{equipment_status.name}', description = '{equipment_status.description}', updated_at = CAST('{str(equipment_status.updated_at)}' AS DATETIME2) WHERE id = '{equipment_status.id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def delete_equipment_status(self, equipment_status_id: str) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.EquipmentStatus WHERE id = '{equipment_status_id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e
