from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.equipments.equipment import Equipment

config = Settings()
database_client = DatabaseClient()


class EquipmentRepository:
    @staticmethod
    def get_all_equipments() -> List[Equipment]:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipments = []

            return equipments
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def get_equipment_by_status(equipment_status: str) -> List[Equipment]:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE status = '{equipment_status}'"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipments = []

            return equipments
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def get_equipment_by_reservation_id(reservation_id: str) -> List[Equipment]:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE reservation_id = '{reservation_id}'"
            )

            rows = cursor.fetchall()
            if rows is not None:
                columns = [column[0] for column in cursor.description]
                equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
            else:
                equipments = []

            return equipments
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def find_equipment_by_id(equipment_id: str) -> Equipment:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE id = '{equipment_id}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                equipment = Equipment.create_from_persistence(dict(zip(columns, row)))
            else:
                equipment = {}

            return equipment
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def find_equipment_by_name(equipment_name: str) -> Equipment:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"SELECT * FROM {config.ENVIRONMENT}.Equipment WHERE name = '{equipment_name}'"
            )

            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                equipment = Equipment.create_from_persistence(dict(zip(columns, row)))
            else:
                equipment = {}
            return equipment
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def create_equipment(equipment: Equipment) -> None:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"INSERT INTO {config.ENVIRONMENT}.Equipment (id, name, description, status, reservation_id, created_at, updated_at) "
                f"VALUES ('{equipment.id}', '{equipment.name}', '{equipment.description}', '{equipment.status}', '{equipment.reservation_id}', CAST('{equipment.created_at}' AS DATETIME2), CAST('{equipment.updated_at}' AS DATETIME2))"
            )
        except Exception as e:
            database_client.close_connection()
            raise e

    @staticmethod
    def update_equipment(equipment: Equipment) -> None:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"UPDATE {config.ENVIRONMENT}.Equipment SET "
                f"name = '{equipment.name}', "
                f"description = '{equipment.description}', "
                f"status = '{equipment.status}', "
                f"updated_at = CAST('{equipment.updated_at}' AS DATETIME2) "
                f"WHERE id = '{equipment.id}' "
            )
        except Exception as e:
            raise e

    @staticmethod
    def delete_equipment(equipment_id: str) -> None:
        try:
            cursor = database_client.get_conn()

            cursor.execute(
                f"DELETE FROM {config.ENVIRONMENT}.Equipment WHERE id = '{equipment_id}'"
            )
        except Exception as e:
            database_client.close_connection()
            raise e
