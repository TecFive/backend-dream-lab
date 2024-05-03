from fastapi import APIRouter, UploadFile, File

from app.core.config import Settings
from app.dtos.rooms.create_room_dto import CreateRoomDto
from app.dtos.rooms.update_room_dto import UpdateRoomDto
from app.services.rooms.room_service import RoomService

config = Settings()

router = APIRouter()
roomService = RoomService()


@router.get("/")
async def get_all_rooms():
    try:
        rooms = roomService.get_all_rooms()

        return {"data": rooms}
    except Exception as e:
        return {"error": str(e)}


@router.get("/id/{room_id}")
async def find_room_by_id(room_id: str):
    try:
        room = roomService.find_room_by_id(room_id)

        return {"data": room}
    except Exception as e:
        return {"error": str(e)}


@router.get("/name/{room_name}")
async def find_room_by_name(room_name: str):
    try:
        room = roomService.find_room_by_name(room_name)

        return {"data": room}
    except Exception as e:
        return {"error": str(e)}


@router.post("/")
async def create_room(create_room_dto: CreateRoomDto):
    try:
        roomService.create_room(create_room_dto)

        return {"data": "Room created successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.put("/")
async def update_room(update_room_dto: UpdateRoomDto):
    try:
        roomService.update_room(update_room_dto)

        return {"data": "Room updated successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.put("/update/image/{room_id}")
async def add_image_to_room(room_id: str, image_url: str):
    try:
        roomService.add_image_to_room(room_id, image_url)

        return {"data": "Image added to room successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.delete("/{room_id}")
async def delete_room(room_id: str):
    try:
        roomService.delete_room(room_id)

        return {"data": "Room deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
