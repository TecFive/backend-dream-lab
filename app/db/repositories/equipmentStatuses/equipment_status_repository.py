from typing import List

from app.core.config import Settings
from app.db.client import database_client
from app.db.models.equipmentStatuses.equipment_status import EquipmentStatus

config = Settings()


class EquipmentStatusRepository:
    @staticmethod
    def get_all_equipment_statuses() -> List[EquipmentStatus]:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.EquipmentStatus"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                equipment_statuses = [EquipmentStatus.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipment_statuses = []

            return equipment_statuses
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def find_equipment_status_by_id(equipment_status_id: str) -> EquipmentStatus:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.EquipmentStatus WHERE id = '{equipment_status_id}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                equipment_status = EquipmentStatus.create_from_persistence(dict(zip(columns, row)))
            else:
                equipment_status = {}

            return equipment_status
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def find_equipment_status_by_name(equipment_status_name: str) -> EquipmentStatus:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.EquipmentStatus WHERE name = '{equipment_status_name}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                equipment_status = EquipmentStatus.create_from_persistence(dict(zip(columns, row)))
            else:
                equipment_status = {}

            return equipment_status
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def create_equipment_status(equipment_status: EquipmentStatus) -> None:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.EquipmentStatus (id, name, description, created_at, updated_at) VALUES ('{equipment_status.id}', '{equipment_status.name}', '{equipment_status.description}', CAST('{equipment_status.created_at}' AS DATETIME2), CAST('{equipment_status.updated_at}' AS DATETIME2))"
            )
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def update_equipment_status(equipment_status: EquipmentStatus) -> None:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.EquipmentStatus SET name = '{equipment_status.name}', description = '{equipment_status.description}', updated_at = CAST('{str(equipment_status.updated_at)}' AS DATETIME2) WHERE id = '{equipment_status.id}'"
            )
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def delete_equipment_status(equipment_status_id: str) -> None:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.EquipmentStatus WHERE id = '{equipment_status_id}'"
            )
        except Exception as e:
            database_client.close_connection()
            raise e
