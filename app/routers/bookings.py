from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.dependencies import get_booking_service
from app.schemas.bookings import BookingCreate, BookingRead
from app.services.bookings import BookingService

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(
    data: BookingCreate,
    service: BookingService = Depends(get_booking_service),
):
    return service.create_booking(data)


@router.get("", response_model=list[BookingRead])
def get_bookings(
    room_id: int | None = None,
    day: date | None = Query(None, alias="date"),
    service: BookingService = Depends(get_booking_service),
):
    return service.get_bookings(room_id, day)


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    service: BookingService = Depends(get_booking_service),
):

    service.delete_booking(booking_id)
