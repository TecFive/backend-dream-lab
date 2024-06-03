from datetime import datetime, timedelta

from app.db.repositories.admin.admin_repository import AdminRepository
from app.services.equipments.equipment_service import EquipmentService
from app.services.reservationStatuses.reservation_status_service import ReservationStatusService
from app.services.rooms.room_service import RoomService


class AdminService:
    reservation_status_service: ReservationStatusService
    room_service: RoomService
    equipment_service: EquipmentService
    admin_repository: AdminRepository

    def __init__(self):
        self.reservation_status_service = ReservationStatusService()
        self.room_service = RoomService()
        self.equipment_service = EquipmentService()
        self.admin_repository = AdminRepository()

    async def get_reservations_between_dates(self, start_date: datetime, end_date: datetime):
        filter_params = "WHERE start_date >= '" + str(start_date) + "' AND end_date <= '" + str(end_date) + "'"
        reservations = self.admin_repository.get_all_reservations(filter_params)

        return reservations

    async def get_daily_reservations(self):
        today = datetime.utcnow()
        today_temp = today + timedelta(days=1)

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
        today_temp = today + timedelta(days=7)

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

    async def get_weekly_reserved_rooms(self):
        today = datetime.utcnow()
        today_temp = today + timedelta(days=7)

        filter_params = f"WHERE r.start_date >= CAST('{today_temp}' AS DATETIME2) AND r.end_date <= CAST('{today}' AS DATETIME2)"
        reservations = self.admin_repository.get_all_reservations(filter_params)

        room_stats = {}
        all_rooms = self.room_service.get_all_rooms()
        for room in all_rooms:
            room_stats[room.name] = 0

        for reservation in reservations:
            room_stats[reservation.room.name] += 1

        return room_stats

    async def get_weekly_reserved_equipment(self):
        today = datetime.utcnow()
        today_temp = today + timedelta(days=7)

        filter_params = f"WHERE r.start_date >= CAST('{today_temp}' AS DATETIME2) AND r.end_date <= CAST('{today}' AS DATETIME2)"
        reservations = self.admin_repository.get_all_reservations(filter_params)

        equipment_stats = {}
        all_equipment = self.equipment_service.get_equipments()
        for equipment in all_equipment:
            equipment_stats[equipment.name] = 0

        for reservation in reservations:
            for equipment in reservation.reserved_equipment:
                equipment_stats[equipment.name] += 1

        return equipment_stats
    
    async def get_monthly_reserved_rooms(self):
        # Get the current date
        current_date = datetime.now()

        # Calculate the start date of the current month
        start_date = current_date.replace(day=1)

        # Calculate the end date of the current month
        # First, get the start of the next month
        if current_date.month == 12:
            next_month_start = current_date.replace(year=current_date.year + 1, month=1, day=1)
        else:
            next_month_start = current_date.replace(month=current_date.month + 1, day=1)

        # The end date of the current month is one day before the start of the next month
        end_date = next_month_start - timedelta(days=1)

        filter_params = f"WHERE r.start_date >= CAST('{start_date}' AS DATETIME2) AND r.start_date <= CAST('{end_date}' AS DATETIME2)"
        reservations = self.admin_repository.get_all_reservations(filter_params)

        room_stats = {}
        all_rooms = self.room_service.get_all_rooms()
        for room in all_rooms:
            room_stats[room.name] = 0

        for reservation in reservations:
            room_stats[reservation.room.name] += 1

        return room_stats
