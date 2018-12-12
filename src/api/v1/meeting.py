import logging

from molten import Route, HTTP_200, HTTP_201, HTTP_400, HTTP_404, HTTPError, dump_schema

from schemas import MeetingType
from models.meeting import Meeting
from models.room import Room

log = logging.getLogger(__name__)


def get_meetings():
    """
    Return all meetings.
    """

    meetings = Meeting.all()

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


routes = [
    Route("/", get_meetings, "GET"),
    Route("/", create_meeting, "POST"),
    Route("/{id}", get_meeting_by_id, "GET"),
    Route("/{id}", update_meeting, "PUT"),
    Route("/{id}", delete_meeting, "DELETE"),
]
