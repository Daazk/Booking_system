from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Room


class RoomRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Room]:
        return list(self.session.scalars(select(Room)).all())

    def get_by_id(self, room_id: int) -> Room | None:
        return self.session.get(Room, room_id)
