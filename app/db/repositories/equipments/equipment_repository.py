from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.equipments.equipment import Equipment

config = Settings()


class EquipmentRepository:
    database_client: DatabaseClient = DatabaseClient()

    def get_all_equipments(self) -> List[Equipment]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipments = []

            self.database_client.close()

            return equipments
        except Exception as e:
            raise e

    def get_equipment_by_status(self, equipment_status: str) -> List[Equipment]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE status = '{equipment_status}'"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipments = []

            self.database_client.close()

            return equipments
        except Exception as e:
            raise e

    def get_equipment_by_reservation_id(self, reservation_id: str) -> List[Equipment]:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE reservation_id = '{reservation_id}'"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipments = []

            self.database_client.close()

            return equipments
        except Exception as e:
            raise e

    def find_equipment_by_id(self, equipment_id: str) -> Equipment:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE id = '{equipment_id}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                equipment = Equipment.create_from_persistence(dict(zip(columns, row)))
            else:
                equipment = {}

            self.database_client.close()

            return equipment
        except Exception as e:
            raise e

    def find_equipment_by_name(self, equipment_name: str) -> Equipment:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE name = '{equipment_name}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                equipment = Equipment.create_from_persistence(dict(zip(columns, row)))
            else:
                equipment = {}

            self.database_client.close()

            return equipment
        except Exception as e:
            raise e

    def create_equipment(self, equipment: Equipment) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Equipment (id, name, description, status, reservation_id, created_at, updated_at) "
                f"VALUES ('{equipment.id}', '{equipment.name}', '{equipment.description}', '{equipment.status}', '{equipment.reservation_id}', CAST('{equipment.created_at}' AS DATETIME2), CAST('{equipment.updated_at}' AS DATETIME2))"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def update_equipment(self, equipment: Equipment) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Equipment SET name = ?, description = ?, status = ?, image = ?, updated_at = CAST(? AS DATETIME2) WHERE id = ?",
                (
                    equipment.name,
                    equipment.description,
                    equipment.status,
                    equipment.image,
                    equipment.updated_at,
                    equipment.id
                )
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def delete_equipment(self, equipment_id: str) -> None:
        try:
            cursor = self.database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Equipment WHERE id = '{equipment_id}'"
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e
