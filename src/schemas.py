from typing import Optional

from molten import schema, Field


date_format = (
    r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})"
    r"[T ](?P<hour>\d{1,2}):(?P<minute>\d{1,2})"
    r"(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?"
    r"(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?$"
)


@schema
class RoomType:
    id: Optional[int] = Field(response_only=True)
    name: str = Field(min_length=1, max_length=60)


@schema
class MeetingType:
    id: Optional[int] = Field(response_only=True)
    title: str = Field(min_length=1)
    start: str = Field(pattern=date_format)
    end: str = Field(pattern=date_format)
    owner: str = Field()
    room_id: int
