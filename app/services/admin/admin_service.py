from datetime import datetime, timedelta

from app.db.repositories.admin.admin_repository import AdminRepository
from app.services.reservationStatuses.reservation_status_service import ReservationStatusService


class AdminService:
    admin_repository = AdminRepository()
    reservation_status_service = ReservationStatusService()

    def __init__(self):
        self.admin_repository = AdminRepository()

    async def get_reservations_between_dates(self, start_date: datetime, end_date: datetime):
        filter_params = "WHERE start_date >= '" + str(start_date) + "' AND end_date <= '" + str(end_date) + "'"
        reservations = self.admin_repository.get_all_reservations(filter_params)

        return reservations

    async def get_daily_reservations(self):
        today = datetime.utcnow()
        today_temp = today - timedelta(days=1)

        approved_status = self.reservation_status_service.get_reservation_status_by_name("Approved")
        pending_status = self.reservation_status_service.get_reservation_status_by_name("Pending")
        completed_status = self.reservation_status_service.get_reservation_status_by_name("Completed")

        approved_filter_params = f"WHERE r.start_date >= CAST('{today_temp}' AS DATETIME2) AND r.end_date <= CAST('{today}' AS DATETIME2) AND r.status='{approved_status.id}'"
        pending_filter_params = f"WHERE r.start_date >= CAST('{today_temp}' AS DATETIME2) AND r.end_date <= CAST('{today}' AS DATETIME2) AND r.status='{pending_status.id}'"
        completed_filter_params = f"WHERE r.start_date >= CAST('{today_temp}' AS DATETIME2) AND r.end_date <= CAST('{today}' AS DATETIME2) AND r.status='{completed_status.id}'"

        approved_reservations = self.admin_repository.get_all_reservations(approved_filter_params)
        pending_reservations = self.admin_repository.get_all_reservations(pending_filter_params)
        completed_reservations = self.admin_repository.get_all_reservations(completed_filter_params)

        return {
            "approved": len(approved_reservations),
            "pending": len(pending_reservations),
            "completed": len(completed_reservations)
        }

    async def get_weekly_reservations(self):
        today = datetime.utcnow()
        today_temp = today - timedelta(days=7)

        approved_status = self.reservation_status_service.get_reservation_status_by_name("Approved")
        pending_status = self.reservation_status_service.get_reservation_status_by_name("Pending")
        completed_status = self.reservation_status_service.get_reservation_status_by_name("Completed")

        approved_filter_params = f"WHERE r.start_date >= CAST('{today_temp}' AS DATETIME2) AND r.end_date <= CAST('{today}' AS DATETIME2) AND r.status='{approved_status.id}'"
        pending_filter_params = f"WHERE r.start_date >= CAST('{today_temp}' AS DATETIME2) AND r.end_date <= CAST('{today}' AS DATETIME2) AND r.status='{pending_status.id}'"
        completed_filter_params = f"WHERE r.start_date >= CAST('{today_temp}' AS DATETIME2) AND r.end_date <= CAST('{today}' AS DATETIME2) AND r.status='{completed_status.id}'"

        approved_reservations = self.admin_repository.get_all_reservations(approved_filter_params)
        pending_reservations = self.admin_repository.get_all_reservations(pending_filter_params)
        completed_reservations = self.admin_repository.get_all_reservations(completed_filter_params)

        return {
            "approved": len(approved_reservations),
            "pending": len(pending_reservations),
            "completed": len(completed_reservations)
        }

    async def get_all_time_reservations(self):
        approved_status = self.reservation_status_service.get_reservation_status_by_name("Approved")
        pending_status = self.reservation_status_service.get_reservation_status_by_name("Pending")
        completed_status = self.reservation_status_service.get_reservation_status_by_name("Completed")

        approved_filter_params = f"WHERE r.status='{approved_status.id}'"
        pending_filter_params = f"WHERE r.status='{pending_status.id}'"
        completed_filter_params = f"WHERE r.status='{completed_status.id}'"

        approved_reservations = self.admin_repository.get_all_reservations(approved_filter_params)
        pending_reservations = self.admin_repository.get_all_reservations(pending_filter_params)
        completed_reservations = self.admin_repository.get_all_reservations(completed_filter_params)

        return {
            "approved": len(approved_reservations),
            "pending": len(pending_reservations),
            "completed": len(completed_reservations)
        }
