from typing import Optional

from molten import schema, Field


@schema
class RoomType:
    id: Optional[int] = Field(response_only=True)
    name: str = Field(min_length=1, max_length=60)


@schema
class MeetingType:
    id: Optional[int] = Field(response_only=True)
    title: str = Field(min_length=1)
    start: str = Field()
    end: str = Field()
    owner: str = Field()
    room_id: int
