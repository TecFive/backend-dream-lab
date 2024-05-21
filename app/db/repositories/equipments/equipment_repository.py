from typing import List

from app.core.config import Settings
from app.db.client import DatabaseClient
from app.db.models.application.equipments.equipment import Equipment
from app.db.models.persistence.equipments.equipment import EquipmentPersistence

config = Settings()


class EquipmentRepository:
    database_client: DatabaseClient = DatabaseClient()

    def get_all_equipments(self) -> List[Equipment]:
        try:
            cursor = self.database_client.get_conn()

            query = f"SELECT e.id AS id, e.name AS name, e.description AS description, ES.id AS status_id, ES.name AS status_name, ES.description AS status_description, ES.created_at AS status_created_at, ES.updated_at AS status_updated_at, e.reservation_id AS reservation_id, e.created_at AS created_at, e.updated_at AS updated_at, e.image AS image FROM {config.ENVIRONMENT}.Equipment as e INNER JOIN {config.ENVIRONMENT}.EquipmentStatus ES on ES.id = e.status"
            cursor.execute(query)

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

            query = f"SELECT e.id AS id, e.name AS name, e.description AS description, ES.id AS status_id, ES.name AS status_name, ES.description AS status_description, ES.created_at AS status_created_at, ES.updated_at AS status_updated_at, e.reservation_id AS reservation_id, e.created_at AS created_at, e.updated_at AS updated_at, e.image AS image FROM {config.ENVIRONMENT}.Equipment as e INNER JOIN {config.ENVIRONMENT}.EquipmentStatus ES on ES.id = e.status WHERE e.status = '{equipment_status}'"
            cursor.execute(query)

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

            query = f"SELECT e.id AS id, e.name AS name, e.description AS description, ES.id AS status_id, ES.name AS status_name, ES.description AS status_description, ES.created_at AS status_created_at, ES.updated_at AS status_updated_at, e.reservation_id AS reservation_id, e.created_at AS created_at, e.updated_at AS updated_at, e.image AS image FROM {config.ENVIRONMENT}.Equipment as e INNER JOIN {config.ENVIRONMENT}.EquipmentStatus ES on ES.id = e.status WHERE e.reservation_id = '{reservation_id}'"
            cursor.execute(query)

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

            query = f"SELECT e.id AS id, e.name AS name, e.description AS description, ES.id AS status_id, ES.name AS status_name, ES.description AS status_description, ES.created_at AS status_created_at, ES.updated_at AS status_updated_at, e.reservation_id AS reservation_id, e.created_at AS created_at, e.updated_at AS updated_at, e.image AS image FROM {config.ENVIRONMENT}.Equipment as e INNER JOIN {config.ENVIRONMENT}.EquipmentStatus ES on ES.id = e.status WHERE e.id = '{equipment_id}'"
            cursor.execute(query)

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

            query = f"SELECT e.id AS id, e.name AS name, e.description AS description, ES.id AS status_id, ES.name AS status_name, ES.description AS status_description, ES.created_at AS status_created_at, ES.updated_at AS status_updated_at, e.reservation_id AS reservation_id, e.created_at AS created_at, e.updated_at AS updated_at, e.image AS image FROM {config.ENVIRONMENT}.Equipment as e INNER JOIN {config.ENVIRONMENT}.EquipmentStatus ES on ES.id = e.status WHERE e.name = '{equipment_name}'"
            cursor.execute(query)

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
            equipment_persistence = EquipmentPersistence.create_from_application(equipment)

            cursor = self.database_client.get_conn()

            query = f"INSERT INTO {config.ENVIRONMENT}.Equipment (id, name, description, status, reservation_id, image, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, CAST(? AS DATETIME2), CAST(? AS DATETIME2))"
            cursor.execute(
                query,
                (
                    equipment_persistence.id,
                    equipment_persistence.name,
                    equipment_persistence.description,
                    equipment_persistence.status,
                    equipment_persistence.reservation_id,
                    equipment_persistence.image,
                    equipment_persistence.created_at,
                    equipment_persistence.updated_at
                )
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def update_equipment(self, equipment: Equipment) -> None:
        try:
            equipment_persistence = EquipmentPersistence.create_from_application(equipment)

            cursor = self.database_client.get_conn()

            query = f"UPDATE {config.ENVIRONMENT}.Equipment SET name = ?, description = ?, status = ?, image = ?, updated_at = CAST(? AS DATETIME2) WHERE id = ?"
            cursor.execute(
                query,
                (
                    equipment_persistence.name,
                    equipment_persistence.description,
                    equipment_persistence.status,
                    equipment_persistence.image,
                    equipment_persistence.updated_at,
                    equipment_persistence.id
                )
            )

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e

    def delete_equipment(self, equipment_id: str) -> None:
        try:
            cursor = self.database_client.get_conn()

            query = f"DELETE FROM {config.ENVIRONMENT}.Equipment WHERE id = ?"
            cursor.execute(query, equipment_id)

            self.database_client.commit()
            self.database_client.close()
        except Exception as e:
            raise e
