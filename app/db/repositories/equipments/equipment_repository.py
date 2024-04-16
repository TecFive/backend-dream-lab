from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.equipments.equipment import Equipment

config = Settings()
database_client = DatabaseClient()


class EquipmentRepository:
    @staticmethod
    def get_all_equipments() -> List[Equipment]:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.Equipments"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
        else:
            equipments = []

        database_client.close_connection()

        return equipments

    @staticmethod
    def get_equipment_by_status(equipment_status: str) -> List[Equipment]:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.Equipments WHERE status = '{equipment_status}'"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
        else:
            equipments = []

        database_client.close_connection()

        return equipments

    @staticmethod
    def get_equipment_by_reservation_id(reservation_id: str) -> List[Equipment]:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.Equipments WHERE reservation_id = '{reservation_id}'"
        )

        rows = cursor.fetchall()
        if rows is not None:
            columns = [column[0] for column in cursor.description]
            equipments = [Equipment.create_from_persistence(dict(zip(columns, row))) for row in rows]
        else:
            equipments = []

        database_client.close_connection()

        return equipments

    @staticmethod
    def find_equipment_by_id(equipment_id: str) -> Equipment:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.Equipments WHERE id = '{equipment_id}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            equipment = Equipment.create_from_persistence(dict(zip(columns, row)))
        else:
            equipment = {}

        database_client.close_connection()

        return equipment

    @staticmethod
    def find_equipment_by_name(equipment_name: str) -> Equipment:
        cursor = database_client.get_conn()

        cursor.execute(
            f"SELECT * FROM {config.ENVIRONMENT}.Equipments WHERE name = '{equipment_name}'"
        )

        row = cursor.fetchone()
        if row is not None:
            columns = [column[0] for column in cursor.description]
            equipment = Equipment.create_from_persistence(dict(zip(columns, row)))
        else:
            equipment = {}

        database_client.close_connection()

        return equipment

    @staticmethod
    def create_equipment(equipment: Equipment) -> None:
        cursor = database_client.get_conn()

        cursor.execute(
            f"INSERT INTO {config.ENVIRONMENT}.Equipments (name, type, description, status) "
            f"VALUES ('{equipment.name}', '{equipment.type}', '{equipment.description}', '{equipment.status}')"
        )

        database_client.commit()
        database_client.close_connection()

    @staticmethod
    def update_equipment(equipment: Equipment) -> None:
        cursor = database_client.get_conn()

        cursor.execute(
            f"UPDATE {config.ENVIRONMENT}.Equipments SET name = '{equipment.name}', type = '{equipment.type}', "
            f"description = '{equipment.description}', status = '{equipment.status}' WHERE id = '{equipment.id}'"
        )

        database_client.commit()
        database_client.close_connection()

    @staticmethod
    def delete_equipment(equipment_id: str) -> None:
        cursor = database_client.get_conn()

        cursor.execute(
            f"DELETE FROM {config.ENVIRONMENT}.Equipments WHERE id = '{equipment_id}'"
        )

        database_client.commit()
        database_client.close_connection()
