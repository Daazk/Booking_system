from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Booking
from app.schemas.bookings import BookingCreate


class BookingOverlapError(Exception):
    pass


class BookingRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: BookingCreate) -> Booking:
        booking = Booking(**data.model_dump())
        self.session.add(booking)
        try:
            self.session.commit()

        except IntegrityError as e:
            self.session.rollback()

            if (
                getattr(e.orig.diag, "constraint_name", None) == "bookings_no_overlap"
            ):  # (e.orig.diag) это диагностическая инфа psql
                raise BookingOverlapError from e
            raise

        self.session.refresh(booking)
        return booking

    def get_by_id(self, booking_id: int) -> Booking | None:
        return self.session.get(Booking, booking_id)

    def delete(self, booking: Booking) -> None:
        self.session.delete(booking)
        self.session.commit()

    def has_overlap(
        self, room_id: int, start_time: datetime, end_time: datetime
    ) -> bool:
        stmt = (
            select(Booking.id)
            .where(
                Booking.room_id == room_id,
                Booking.start_time < end_time,
                Booking.end_time > start_time,
            )
            .limit(1)
        )

        return self.session.scalar(stmt) is not None

    def get_list(
        self, room_id: int | None = None, day: date | None = None
    ) -> list[Booking]:
        stmt = select(Booking)

        if room_id is not None:
            stmt = stmt.where(Booking.room_id == room_id)

        if day is not None:
            day_start = datetime.combine(day, time.min, tzinfo=timezone.utc)
            day_end = day_start + timedelta(days=1)
            stmt = stmt.where(
                Booking.start_time >= day_start,
                Booking.start_time < day_end,
            )

        stmt = stmt.order_by(Booking.start_time)
        return list(self.session.scalars(stmt).all())
