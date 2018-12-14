from typing import Optional
from molten import schema, Field

from validators import DateValidator


@schema
class RoomType:
    id: Optional[int] = Field(response_only=True)
    name: str = Field(min_length=1, max_length=60)


@schema
class MeetingType:
    id: Optional[int] = Field(response_only=True)
    title: str = Field(min_length=1)
    date_start: str = Field(validator=DateValidator())
    date_end: str = Field(validator=DateValidator())
    owner: str = Field()
    room_id: int
