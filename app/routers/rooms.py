from fastapi import APIRouter, Depends

from app.dependencies import get_room_repo
from app.repositories.rooms import RoomRepository
from app.schemas.rooms import RoomRead

router = APIRouter(prefix="/api/rooms", tags=["Rooms"])


@router.get("", response_model=list[RoomRead])
def get_rooms(room_repo: RoomRepository = Depends(get_room_repo)):
    return room_repo.get_all()
