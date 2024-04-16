from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.equipmentStatuses.equipment_status import EquipmentStatus

config = Settings()
database_client = DatabaseClient()


class EquipmentStatusRepository:
    @staticmethod
    def get_all_equipment_statuses() -> List[EquipmentStatus]:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.EquipmentStatuses"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            equipment_statuses = [EquipmentStatus.create_from_persistence(dict(zip(columns, row))) for row in rows]
        else:
            equipment_statuses = []

        database_client.close_connection()

        return equipment_statuses

    @staticmethod
    def find_equipment_status_by_id(equipment_status_id: str) -> EquipmentStatus:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.EquipmentStatuses WHERE id = '{equipment_status_id}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            equipment_status = EquipmentStatus.create_from_persistence(dict(zip(columns, row)))
        else:
            equipment_status = {}

        database_client.close_connection()

        return equipment_status

    @staticmethod
    def find_equipment_status_by_name(equipment_status_name: str) -> EquipmentStatus:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.EquipmentStatuses WHERE name = '{equipment_status_name}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            equipment_status = EquipmentStatus.create_from_persistence(dict(zip(columns, row)))
        else:
            equipment_status = {}

        database_client.close_connection()

        return equipment_status

    @staticmethod
    def create_equipment_status(equipment_status: EquipmentStatus) -> None:
        cursor = database_client.get_conn()

        cursor.execute(
            f"INSERT INTO {config.ENVIRONMENT}.EquipmentStatuses (name, description) VALUES ('{equipment_status.name}', '{equipment_status.description}')"
        )

        database_client.commit()
        database_client.close_connection()

        return equipment_status

    @staticmethod
    def update_equipment_status(equipment_status: EquipmentStatus) -> None:
        cursor = database_client.get_conn()

        cursor.execute(
            f"UPDATE {config.ENVIRONMENT}.EquipmentStatuses SET name = '{equipment_status.name}', description = '{equipment_status.description}' WHERE id = '{equipment_status.id}'"
        )

        database_client.commit()
        database_client.close_connection()

    @staticmethod
    def delete_equipment_status(equipment_status_id: str) -> None:
        cursor = database_client.get_conn()

        cursor.execute(
            f"DELETE FROM {config.ENVIRONMENT}.EquipmentStatuses WHERE id = '{equipment_status_id}'"
        )

        database_client.commit()
        database_client.close_connection()
