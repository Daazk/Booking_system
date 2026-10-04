from pydantic import BaseModel, ConfigDict


class RoomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    capacity: int
