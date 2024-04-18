from datetime import datetime
from typing import List
import bson

from app.db.client import database_client
from app.db.models.equipments.equipment import Equipment
from app.db.repositories.equipments.equipment_repository import EquipmentRepository
from app.dtos.equipments.create_equipment_dto import CreateEquipmentDto
from app.dtos.equipments.update_equipment_dto import UpdateEquipmentDto


class EquipmentService:
    equipment_repository: EquipmentRepository

    def __init__(self):
        self.equipment_repository = EquipmentRepository()

    def get_equipments(self) -> List[Equipment]:
        equipments = self.equipment_repository.get_all_equipments()
        database_client.close_connection()

        return equipments

    def get_equipments_by_status(self, equipment_status: str) -> List[Equipment]:
        equipments = self.equipment_repository.get_equipment_by_status(equipment_status)
        database_client.close_connection()

        return equipments

    def get_equipments_by_reservation_id(self, reservation_id: str) -> List[Equipment]:
        equipments = self.equipment_repository.get_equipment_by_reservation_id(reservation_id)
        database_client.close_connection()

        return equipments

    def find_equipment_by_id(self, equipment_id: str) -> Equipment:
        equipment = self.equipment_repository.find_equipment_by_id(equipment_id)
        database_client.close_connection()

        return equipment

    def find_equipment_by_name(self, equipment_name: str) -> Equipment:
        equipment = self.equipment_repository.find_equipment_by_name(equipment_name)
        database_client.close_connection()

        return equipment

    def create_equipment(self, equipment_dto: CreateEquipmentDto) -> Equipment:
        equipment = Equipment(
            id=str(bson.ObjectId()),
            name=equipment_dto.name,
            description=equipment_dto.description,
            status=equipment_dto.status,
            createdAt=datetime.now().isoformat(),
            updatedAt=datetime.now().isoformat(),
        )

        self.equipment_repository.create_equipment(equipment)

        database_client.commit()
        database_client.close_connection()

        return equipment

    def update_equipment(self, equipment_dto: UpdateEquipmentDto) -> Equipment:
        equipment = self.find_equipment_by_id(equipment_dto.id)
        if equipment is None:
            raise ValueError("Equipment not found")

        equipment.name = equipment_dto.name
        equipment.description = equipment_dto.description
        equipment.status = equipment_dto.status
        equipment.reservation_id = equipment_dto.reservation_id
        equipment.updated_at = datetime.now().isoformat()

        self.equipment_repository.update_equipment(equipment)

        database_client.commit()
        database_client.close_connection()

        return equipment

    def delete_equipment(self, equipment_id: str) -> None:
        equipment_found = self.find_equipment_by_id(equipment_id)
        if equipment_found is None:
            raise ValueError("Equipment not found")

        self.equipment_repository.delete_equipment(equipment_id)

        database_client.commit()
        database_client.close_connection()
