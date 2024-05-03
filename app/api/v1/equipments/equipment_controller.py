from fastapi import APIRouter
from app.core.config import Settings
from app.dtos.equipments.create_equipment_dto import CreateEquipmentDto
from app.dtos.equipments.update_equipment_dto import UpdateEquipmentDto
from app.services.equipments.equipment_service import EquipmentService

config = Settings()

router = APIRouter()
equipmentService = EquipmentService()


@router.get("/")
async def get_all_equipments():
    try:
        equipments = equipmentService.get_equipments()

        return {"data": equipments}
    except Exception as e:
        return {"error": str(e)}


@router.get("/id/{equipment_id}")
async def find_equipment_by_id(equipment_id: str):
    try:
        equipment = equipmentService.find_equipment_by_id(equipment_id)

        return {"data": equipment}
    except Exception as e:
        return {"error": str(e)}


@router.get("/status/{equipment_status}")
async def get_equipments_by_status(equipment_status: str):
    try:
        equipments = equipmentService.get_equipments_by_status(equipment_status)

        return {"data": equipments}
    except Exception as e:
        return {"error": str(e)}


@router.get("/reservation/{reservation_id}")
async def get_equipments_by_reservation_id(reservation_id: str):
    try:
        equipment = equipmentService.get_equipments_by_reservation_id(reservation_id)

        return {"data": equipment}
    except Exception as e:
        return {"error": str(e)}


@router.get("/name/{equipment_name}")
async def find_equipment_by_name(equipment_name: str):
    try:
        equipment = equipmentService.find_equipment_by_name(equipment_name)

        return {"data": equipment}
    except Exception as e:
        return {"error": str(e)}


@router.post("/")
async def create_equipment(equipment_data: CreateEquipmentDto):
    try:
        equipment = equipmentService.create_equipment(equipment_data)

        return {"data": equipment}
    except Exception as e:
        return {"error": str(e)}


@router.put("/")
async def update_equipment(equipment_data: UpdateEquipmentDto):
    try:
        equipment = equipmentService.update_equipment(equipment_data)

        return {"data": equipment}
    except Exception as e:
        return {"error": str(e)}


@router.put("/update/image/{equipment_id}")
async def add_image_to_equipment(equipment_id: str, image_url: str):
    try:
        equipmentService.add_image_to_equipment(equipment_id, image_url)

        return {"data": "Image added to equipment successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.delete("/{equipment_id}")
async def delete_equipment(equipment_id: str):
    try:
        equipmentService.delete_equipment(equipment_id)

        return {"data": "Equipment deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
