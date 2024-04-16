from fastapi import APIRouter

from app.core.config import Settings
from app.dtos.equipmentStatuses.create_equipment_status_dto import CreateEquipmentStatusDto
from app.dtos.equipmentStatuses.update_equipment_status_dto import UpdateEquipmentStatusDto
from app.services.equipmentStatuses.equipment_status_service import EquipmentStatusService

config = Settings()
router = APIRouter()
equipmentStatusService = EquipmentStatusService()


@router.get("/")
async def get_all_equipment_statuses():
    try:
        equipment_statuses = equipmentStatusService.get_all_equipment_statuses()

        return {"data": equipment_statuses}
    except Exception as e:
        return {"error": str(e)}


@router.get("/id/{equipment_status_id}")
async def find_equipment_status_by_id(equipment_status_id: str):
    try:
        equipment_status = equipmentStatusService.find_equipment_status_by_id(equipment_status_id)

        return {"data": equipment_status}
    except Exception as e:
        return {"error": str(e)}


@router.get("/name/{equipment_status_name}")
async def find_equipment_status_by_name(equipment_status_name: str):
    try:
        equipment_status = equipmentStatusService.find_equipment_status_by_name(equipment_status_name)

        return {"data": equipment_status}
    except Exception as e:
        return {"error": str(e)}


@router.post("/")
async def create_equipment_status(equipment_status_data: CreateEquipmentStatusDto):
    try:
        return await equipmentStatusService.create_equipment_status(equipment_status_data)
    except Exception as e:
        return {"error": str(e)}


@router.put("/")
async def update_equipment_status(equipment_status_data: UpdateEquipmentStatusDto):
    try:
        return await equipmentStatusService.update_equipment_status(equipment_status_data)
    except Exception as e:
        return {"error": str(e)}


@router.delete("/{equipment_status_id}")
async def delete_equipment_status(equipment_status_id: str):
    try:
        return await equipmentStatusService.delete_equipment_status(equipment_status_id)
    except Exception as e:
        return {"error": str(e)}
