from datetime import datetime
import bson

from app.db.models.equipmentStatuses.equipment_status import EquipmentStatus
from app.db.repositories.equipmentStatuses.equipment_status_repository import EquipmentStatusRepository
from app.dtos.equipmentStatuses.create_equipment_status_dto import CreateEquipmentStatusDto
from app.dtos.equipmentStatuses.update_equipment_status_dto import UpdateEquipmentStatusDto


class EquipmentStatusService:
    equipment_status_repository: EquipmentStatusRepository

    def __init__(self):
        self.equipment_status_repository = EquipmentStatusRepository()

    def get_all_equipment_statuses(self):
        statuses = self.equipment_status_repository.get_all_equipment_statuses()

        return statuses

    def find_equipment_status_by_id(self, equipment_status_id: str):
        status = self.equipment_status_repository.find_equipment_status_by_id(equipment_status_id)

        return status

    def find_equipment_status_by_name(self, equipment_status_name: str):
        status = self.equipment_status_repository.find_equipment_status_by_name(equipment_status_name)

        return status

    def create_equipment_status(self, equipment_status_dto: CreateEquipmentStatusDto):
        equipment_status = EquipmentStatus(
            id=str(bson.ObjectId()),
            name=equipment_status_dto.name,
            description=equipment_status_dto.description,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        self.equipment_status_repository.create_equipment_status(equipment_status)

    def update_equipment_status(self, equipment_status_dto: UpdateEquipmentStatusDto):
        equipment_status = self.equipment_status_repository.find_equipment_status_by_id(equipment_status_dto.id)
        if equipment_status is None:
            raise ValueError("Equipment status not found")

        equipment_status.name = equipment_status_dto.name
        equipment_status.description = equipment_status_dto.description
        equipment_status.updated_at = datetime.now().isoformat()

        self.equipment_status_repository.update_equipment_status(equipment_status)

    def delete_equipment_status(self, equipment_status_id: str):
        equipment_status_found = self.find_equipment_status_by_id(equipment_status_id)
        if equipment_status_found is None:
            raise ValueError("Equipment status not found")

        self.equipment_status_repository.delete_equipment_status(equipment_status_id)
