import re
import logging
import pendulum
from typing import Optional

from molten import (
    Route,
    HTTP_200,
    HTTP_201,
    HTTP_400,
    HTTP_404,
    HTTPError,
    dump_schema,
    QueryParam,
)

from schemas import MeetingType
from models.meeting import Meeting
from models.room import Room

log = logging.getLogger(__name__)


def get_meetings(room_id: Optional[QueryParam], date: Optional[QueryParam]):
    """
    Return all meetings.
    """

    log.info(f"Get all meetings")

    meetings = Meeting.all()

    if room_id:

        log.info(f"Meetings filter by room id: {room_id}")

        meetings = _filter_by_room_id(meetings, room_id)

    if date:

        log.info(f"Meetings filter by date: {date}")

        meetings = _filter_by_date(meetings, date)

    return HTTP_200, meetings.serialize()


def get_meeting_by_id(id: int):
    """
    Get meeting by id.
    """
    meeting = _find_meeting(id)

    return meeting.serialize()


def create_meeting(meetingData: MeetingType):
    """
    Create a new meeting.
    """

    _check_if_room_exist(meetingData.room_id)

    date_start = meetingData.date_start
    date_end = meetingData.date_end

    _check_date_is_bigger_than(date_end, date_start)

    meeting = Meeting.create(**dump_schema(meetingData))

    headers = {"Content-Location": f"/v1/meetings/{meeting.id}"}

    msg = "Meeting created successfully."
    log.info(f"{msg} with id: {meeting.id}")

    return HTTP_201, {"message": f"{msg}"}, headers


def update_meeting(id: int, meetingData: MeetingType):
    """
    Update a meeting by id
    """

    meeting = _find_meeting(id)
    meeting.update(**dump_schema(meetingData))
    meeting.save()

    return HTTP_200, {"message": "Meeting update successfully."}


def delete_meeting(id: int):
    """
    Delete a meeting by id.
    """

    meeting = _find_meeting(id)
    meeting.delete()

    return HTTP_200, {"message": "Meeting deleted successfully."}


"""
Privates functions
"""


def _find_meeting(id):
    """
    Find a meeting by id
    """

    meeting = Meeting.find(id)

    if not meeting:
        raise HTTPError(HTTP_404, {"errors": "Meeting id not found"})

    return meeting


def _check_if_room_exist(id):
    """
    check if room exist.
    """

    room = Room.find(id)

    if not room:
        raise HTTPError(HTTP_400, {"errors": "The room id don't exist."})


def _check_date_is_bigger_than(end, start):
    """
    Check if date end is bigger than date start.
    """

    log.info(f"END: {end}")
    log.info(f"Start: {start}")

    if not pendulum.parse(end) > pendulum.parse(start):
        msg = "The date end need be bigger than date start."
        raise HTTPError(HTTP_400, {"errors": msg})


def _filter_by_room_id(meetings, room_id):
    """
    Filter meetings by room id.
    """

    try:

        id = int(room_id)

    except ValueError:
        msg = "The room_id need be a integer. Exemple: room_id: 100"
        raise HTTPError(HTTP_400, {"errors": msg})

    return meetings.where("room_id", id)


def _filter_by_date(meetings, date):
    """
    Filter meetings by date.
    """

    date_filter_format = r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$"

    if not re.match(date_filter_format, date):

        msg = "The date filter format must be yyyy-mm-dd"
        raise HTTPError(HTTP_400, {"errors": msg})

    return meetings.filter(lambda meeting: date in meeting.date_start)


routes = [
    Route("", get_meetings, "GET"),
    Route("/", create_meeting, "POST"),
    Route("/{id}", get_meeting_by_id, "GET"),
    Route("/{id}", update_meeting, "PUT"),
    Route("/{id}", delete_meeting, "DELETE"),
]
