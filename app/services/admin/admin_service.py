import calendar
from datetime import datetime, timedelta

from app.db.models.application.reservations.reservation import Reservation
from app.db.repositories.admin.admin_repository import AdminRepository
from app.services.equipments.equipment_service import EquipmentService
from app.services.reservationStatuses.reservation_status_service import ReservationStatusService
from app.services.reservations.reservation_service import ReservationService
from app.services.rooms.room_service import RoomService


class AdminService:
    reservation_status_service: ReservationStatusService
    room_service: RoomService
    equipment_service: EquipmentService
    reservation_service: ReservationService
    admin_repository: AdminRepository

    def __init__(self):
        self.reservation_status_service = ReservationStatusService()
        self.room_service = RoomService()
        self.equipment_service = EquipmentService()
        self.reservation_service = ReservationService()
        self.admin_repository = AdminRepository()

    @staticmethod
    def get_week_dates(date):
        start_of_week = date - timedelta(days=date.weekday() + 1)
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week

    @staticmethod
    def get_month_dates(date):
        year = date.year
        month = date.month
        _, last_day = calendar.monthrange(year, month)
        start_of_month = datetime(year, month, 1)
        end_of_month = datetime(year, month, last_day)
        return start_of_month, end_of_month

    async def get_reservations_between_dates(self, start_date: datetime, end_date: datetime):
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=0)

        filter_params = "WHERE start_date >= '" + str(start_date) + "' AND end_date <= '" + str(end_date) + "'"
        reservations = self.admin_repository.get_all_reservations(filter_params)

        return reservations

    async def get_daily_reservations(self):
        start_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date.replace(hour=23, minute=59, second=59, microsecond=0)

        approved_status = self.reservation_status_service.get_reservation_status_by_name("Approved")
        pending_status = self.reservation_status_service.get_reservation_status_by_name("Pending")
        completed_status = self.reservation_status_service.get_reservation_status_by_name("Completed")

        approved_filter_params = f"WHERE r.start_date >= CAST('{start_date}' AS DATETIME2) AND r.end_date <= CAST('{end_date}' AS DATETIME2) AND r.status='{approved_status.id}'"
        pending_filter_params = f"WHERE r.start_date >= CAST('{start_date}' AS DATETIME2) AND r.end_date <= CAST('{end_date}' AS DATETIME2) AND r.status='{pending_status.id}'"
        completed_filter_params = f"WHERE r.start_date >= CAST('{start_date}' AS DATETIME2) AND r.end_date <= CAST('{end_date}' AS DATETIME2) AND r.status='{completed_status.id}'"

        approved_reservations = self.admin_repository.get_all_reservations(approved_filter_params)
        pending_reservations = self.admin_repository.get_all_reservations(pending_filter_params)
        completed_reservations = self.admin_repository.get_all_reservations(completed_filter_params)

        return {
            "approved": len(approved_reservations),
            "pending": len(pending_reservations),
            "completed": len(completed_reservations)
        }

    async def get_weekly_reservations(self):
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start, week_end = self.get_week_dates(today)

        approved_status = self.reservation_status_service.get_reservation_status_by_name("Approved")
        pending_status = self.reservation_status_service.get_reservation_status_by_name("Pending")
        completed_status = self.reservation_status_service.get_reservation_status_by_name("Completed")

        approved_filter_params = f"WHERE r.start_date >= CAST('{week_start}' AS DATETIME2) AND r.end_date <= CAST('{week_end}' AS DATETIME2) AND r.status='{approved_status.id}'"
        pending_filter_params = f"WHERE r.start_date >= CAST('{week_start}' AS DATETIME2) AND r.end_date <= CAST('{week_end}' AS DATETIME2) AND r.status='{pending_status.id}'"
        completed_filter_params = f"WHERE r.start_date >= CAST('{week_start}' AS DATETIME2) AND r.end_date <= CAST('{week_end}' AS DATETIME2) AND r.status='{completed_status.id}'"

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

    async def get_reservations_per_month(self):
        year = datetime.utcnow().year
        month = 1

        reservations_per_month = {}

        while month <= 12:
            month_temp = month + 1
            if month_temp == 13:
                month_temp = 1
                year += 1

            filter_params = f"WHERE r.start_date >= CAST('{year}-{month}-01' AS DATETIME2) AND r.end_date <= CAST('{year}-{month_temp}-01' AS DATETIME2)"
            reservations = self.admin_repository.get_all_reservations(filter_params)
            reservations_per_month[month] = len(reservations)

            month += 1

        return reservations_per_month

    async def get_weekly_reserved_rooms(self):
        today = datetime.today()
        week_start, week_end = self.get_week_dates(today)

        filter_params = f"WHERE r.start_date >= CAST('{week_start}' AS DATETIME2) AND r.end_date <= CAST('{week_end}' AS DATETIME2)"
        reservations = self.admin_repository.get_all_reservations(filter_params)

        room_stats = {}
        all_rooms = self.room_service.get_all_rooms()
        for room in all_rooms:
            room_stats[room.name] = 0

        for reservation in reservations:
            room_stats[reservation.room.name] += 1

        return room_stats

    async def get_weekly_reserved_equipment(self):
        today = datetime.today()
        week_start, week_end = self.get_week_dates(today)

        filter_params = f"WHERE r.start_date >= CAST('{week_start}' AS DATETIME2) AND r.end_date <= CAST('{week_end}' AS DATETIME2)"
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
        today = datetime.today()
        month_start, month_end = self.get_month_dates(today)

        filter_params = f"WHERE r.start_date >= CAST('{month_start}' AS DATETIME2) AND r.start_date <= CAST('{month_end}' AS DATETIME2)"
        reservations = self.admin_repository.get_all_reservations(filter_params)

        room_stats = {}
        all_rooms = self.room_service.get_all_rooms()
        for room in all_rooms:
            room_stats[room.name] = 0

        for reservation in reservations:
            room_stats[reservation.room.name] += 1

        return room_stats

    async def get_equipment_stats_per_month(self):
        year = datetime.utcnow().year
        month = 1

        equipment_stats_per_month = {}

        while month <= 12:
            month_temp = month + 1
            if month_temp == 13:
                month_temp = 1
                year += 1

            filter_params = f"WHERE r.start_date >= CAST('{year}-{month}-01' AS DATETIME2) AND r.end_date <= CAST('{year}-{month_temp}-01' AS DATETIME2)"
            reservations = self.admin_repository.get_all_reservations(filter_params)

            equipment_counter = 0
            for reservation in reservations:
                equipment_counter += len(reservation.reserved_equipment)

            equipment_stats_per_month[month] = equipment_counter

            month += 1

        return equipment_stats_per_month

    async def get_equipment_stats_monthly(self):
        year = datetime.today().year
        month = datetime.today().month
        max_day_of_month = calendar.monthrange(year, month)[1]

        equipment_stats = {}
        all_equipment = self.equipment_service.get_equipments()

        for equipment in all_equipment:
            equipment_stats[equipment.name] = 0

        filter_params = f"WHERE r.start_date >= CAST('{year}-{month}-01' AS DATETIME2) AND r.end_date <= CAST('{year}-{month}-{max_day_of_month}' AS DATETIME2)"
        reservations = self.admin_repository.get_all_reservations(filter_params)

        for reservation in reservations:
            for equipment in reservation.reserved_equipment:
                equipment_stats[equipment.name] += 1

        return equipment_stats

    async def update_reservation_status(self, reservation_id: str, status_id: str) -> Reservation:
        reservation = self.reservation_service.update_status(reservation_id, status_id)

        return reservation


