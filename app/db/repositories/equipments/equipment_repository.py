from typing import List

from app.core.config import Settings
from app.db.client import database_client
from app.db.models.equipments.equipment import Equipment

config = Settings()


class EquipmentRepository:
    cursor = database_client.get_conn()

    def get_all_equipments(self) -> List[Equipment]:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment"
            )

            rows = self.cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in self.cursor.description]
                equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipments = []

            return equipments
        except Exception as e:
            database_client.close_connection()
            raise e

    def get_equipment_by_status(self, equipment_status: str) -> List[Equipment]:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE status = '{equipment_status}'"
            )

            rows = self.cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in self.cursor.description]
                equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipments = []

            return equipments
        except Exception as e:
            database_client.close_connection()
            raise e

    def get_equipment_by_reservation_id(self, reservation_id: str) -> List[Equipment]:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE reservation_id = '{reservation_id}'"
            )

            rows = self.cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in self.cursor.description]
                equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipments = []

            return equipments
        except Exception as e:
            database_client.close_connection()
            raise e

    def find_equipment_by_id(self, equipment_id: str) -> Equipment:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE id = '{equipment_id}'"
            )

            row = self.cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in self.cursor.description]
                equipment = Equipment.create_from_persistence(dict(zip(columns, row)))
            else:
                equipment = {}

            return equipment
        except Exception as e:
            database_client.close_connection()
            raise e

    def find_equipment_by_name(self, equipment_name: str) -> Equipment:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE name = '{equipment_name}'"
            )

            row = self.cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in self.cursor.description]
                equipment = Equipment.create_from_persistence(dict(zip(columns, row)))
            else:
                equipment = {}
            return equipment
        except Exception as e:
            database_client.close_connection()
            raise e

    def create_equipment(self, equipment: Equipment) -> None:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Equipment (id, name, description, status, reservation_id, created_at, updated_at) "
                f"VALUES ('{equipment.id}', '{equipment.name}', '{equipment.description}', '{equipment.status}', '{equipment.reservation_id}', CAST('{equipment.created_at}' AS DATETIME2), CAST('{equipment.updated_at}' AS DATETIME2))"
            )
        except Exception as e:
            database_client.close_connection()
            raise e

    def update_equipment(self, equipment: Equipment) -> None:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
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
        except Exception as e:
            raise e

    def delete_equipment(self, equipment_id: str) -> None:
        try:
            self.cursor = database_client.get_conn()

            self.cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Equipment WHERE id = '{equipment_id}'"
            )
        except Exception as e:
            database_client.close_connection()
            raise e
