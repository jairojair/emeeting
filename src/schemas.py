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
    start: str = Field(validator=DateValidator())
    end: str = Field(validator=DateValidator())
    owner: str = Field()
    room_id: int
