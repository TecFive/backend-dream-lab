from datetime import datetime

from app.db.repositories.admin.admin_repository import AdminRepository


class AdminService:
    admin_repository = AdminRepository()

    def __init__(self):
        self.admin_repository = AdminRepository()

    async def get_reservations_between_dates(self, start_date: datetime, end_date: datetime):
        filter_params = "WHERE start_date >= '" + str(start_date) + "' AND end_date <= '" + str(end_date) + "'"
        reservations = self.admin_repository.get_all_reservations(filter_params)

        return reservations
