from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.bookings import BookingRepository
from app.repositories.rooms import RoomRepository
from app.services.bookings import BookingService


def get_room_repo(db: Session = Depends(get_db)) -> RoomRepository:
    return RoomRepository(db)


def get_booking_repo(db: Session = Depends(get_db)) -> BookingRepository:
    return BookingRepository(db)


def get_booking_service(
    booking_repo: BookingRepository = Depends(get_booking_repo),
    room_repo: RoomRepository = Depends(get_room_repo),
) -> BookingService:
    return BookingService(booking_repo, room_repo)
