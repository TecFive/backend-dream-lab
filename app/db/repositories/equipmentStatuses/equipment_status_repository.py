from typing import List

from fastapi import HTTPException

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.application.equipmentStatuses.equipment_status import EquipmentStatus
from app.db.models.persistence.equipmentStatuses.equipment_status_persistence import EquipmentStatusPersistence

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
            raise HTTPException(status_code=500, detail=str(e))

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
            raise HTTPException(status_code=500, detail=str(e))

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
            raise HTTPException(status_code=500, detail=str(e))

    def create_equipment_status(self, equipment_status: EquipmentStatus) -> None:
        try:
            equipment_status_persistence = EquipmentStatusPersistence.create_from_application(equipment_status)

            cursor = self.database_client.get_conn()

            cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.EquipmentStatus (id, name, description, created_at, updated_at) VALUES ('{equipment_status_persistence.id}', '{equipment_status_persistence.name}', '{equipment_status_persistence.description}', CAST('{equipment_status_persistence.created_at}' AS DATETIME2), CAST('{equipment_status_persistence.updated_at}' AS DATETIME2))"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_equipment_status(self, equipment_status: EquipmentStatus) -> None:
        try:
            equipment_status_persistence = EquipmentStatusPersistence.create_from_application(equipment_status)

            cursor = self.database_client.get_conn()

            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.EquipmentStatus SET name = '{equipment_status_persistence.name}', description = '{equipment_status_persistence.description}', updated_at = CAST('{str(equipment_status_persistence.updated_at)}' AS DATETIME2) WHERE id = '{equipment_status_persistence.id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_equipment_status(self, equipment_status_id: str) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.EquipmentStatus WHERE id = '{equipment_status_id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
