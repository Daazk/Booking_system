from pydantic import BaseModel, ConfigDict, Field, AwareDatetime, model_validator
from datetime import datetime, timezone


class BookingCreate(BaseModel):

    room_id: int
    organizer_name: str = Field(min_length=1, max_length=64)
    start_time: AwareDatetime
    end_time: AwareDatetime

    @model_validator(mode="after")
    def check_times(self):
        if self.start_time < datetime.now(timezone.utc):
            raise ValueError("start_time cannot be in the past")

        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")

        return self


class BookingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    organizer_name: str
    start_time: datetime
    end_time: datetime
