from fastapi import APIRouter
from app.core.config import Settings
from app.db.client import get_conn


config = Settings()

router = APIRouter()


@router.get("/my-reservations")
async def get_my_reservations():
    connection = get_conn()
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT * FROM reservacion WHERE id_usuario = 'asdf'"
    )

    result = cursor.fetchall()
    connection.close()

    return result
