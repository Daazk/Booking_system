from datetime import date


from fastapi import HTTPException, status

from app.models import Booking
from app.repositories.bookings import BookingRepository, BookingOverlapError
from app.repositories.rooms import RoomRepository
from app.schemas.bookings import BookingCreate


class BookingService:
    def __init__(self, booking_repo: BookingRepository, room_repo: RoomRepository):
        self.booking_repo = booking_repo
        self.room_repo = room_repo

    def create_booking(self, data: BookingCreate) -> Booking:
        room = self.room_repo.get_by_id(data.room_id)

        if room is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Room not found")

        if self.booking_repo.has_overlap(data.room_id, data.start_time, data.end_time):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Room is already booked for this slot",
            )

        try:
            return self.booking_repo.create(data)

        except BookingOverlapError:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Room is already booked for this slot",
            )

    def get_bookings(
        self, room_id: int | None = None, day: date | None = None
    ) -> list[Booking]:
        return self.booking_repo.get_list(room_id, day)

    def delete_booking(self, booking_id):
        booking = self.booking_repo.get_by_id(booking_id=booking_id)

        if booking is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Booking not found",
            )

        self.booking_repo.delete(booking)
