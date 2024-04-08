from app.db.models.reservations.reservation import Reservation
from app.db.repositories.reservations.reservation_repository import ReservationRepository


class ReservationService:
    reservation_repository = ReservationRepository

    def __init__(self):
        self.reservation_repository = ReservationRepository()

    def get_all_reservations(self):
        reservations = self.reservation_repository.get_all_reservations()

        return reservations

    def get_reservations_by_room_id(self, room_id: str):
        reservations = self.reservation_repository.get_reservations_by_room_id(room_id)

        return reservations

    def get_reservations_by_user_id(self, user_id: str):
        reservations = self.reservation_repository.get_reservations_by_user_id(user_id)

        return reservations

    def get_reservation_by_id(self, reservation_id: str):
        reservation = self.reservation_repository.get_reservation_by_id(reservation_id)

        return reservation

    def create_reservation(self, reservation: Reservation):
        self.reservation_repository.create_reservation(reservation)

        return reservation

    def update_reservation(self, reservation: Reservation):
        self.reservation_repository.update_reservation(reservation.id, reservation)

    def delete_reservation(self, reservation_id: str):
        self.reservation_repository.delete_reservation(reservation_id)
