import logging
from typing import Optional

from molten import (
    Route,
    HTTP_200,
    HTTP_201,
    HTTP_400,
    HTTP_404,
    HTTP_409,
    HTTPError,
    dump_schema,
    QueryParam,
)

from schemas import MeetingType
from models.meeting import Meeting
from models.room import Room

from exceptions import ConflictError, ValidateError, NotFoundError

log = logging.getLogger(__name__)


def get_meetings(room_id: Optional[QueryParam], date: Optional[QueryParam]):
    """
    Return all meetings.
    """

    log.info(f"Get all meetings")

    try:

        meetings = Meeting.by_room_id(room_id).by_date(date).get()
        return HTTP_200, meetings.serialize()

    except Exception as error:
        raise HTTPError(HTTP_400, {"errors": str(error)})


def get_meeting_by_id(id: int):
    """
    Get meeting by id.
    """

    try:

        meeting = Meeting.find_or_fail(id)
        return meeting.serialize()

    except NotFoundError as error:
        raise HTTPError(HTTP_404, {"errors": str(error)})


def create_meeting(meetingData: MeetingType):
    """
    Create a new meeting.
    """

    try:

        meeting = Meeting()
        meeting.validate(meetingData)

        meeting = Meeting.create(**dump_schema(meetingData))

        headers = {"Content-Location": f"/v1/meetings/{meeting.id}"}

        msg = "Meeting created successfully."
        log.info(f"{msg} with id: {meeting.id}")

        return HTTP_201, {"message": f"{msg}"}, headers

    except ValidateError as error:
        raise HTTPError(HTTP_400, {"errors": str(error)})

    except ConflictError as error:
        raise HTTPError(HTTP_409, {"errors": str(error)})


def update_meeting(id: int, meetingData: MeetingType):
    """
    Update a meeting by id
    """

    try:

        meeting = Meeting.find_or_fail(id)
        meeting.validate(meetingData)

        meeting.update(**dump_schema(meetingData))
        meeting.save()

        return HTTP_200, {"message": "Meeting update successfully."}

    except ValidateError as error:
        raise HTTPError(HTTP_400, {"errors": str(error)})

    except NotFoundError as error:
        raise HTTPError(HTTP_404, {"errors": str(error)})

    except ConflictError as error:
        raise HTTPError(HTTP_409, {"errors": str(error)})


def delete_meeting(id: int):
    """
    Delete a meeting by id.
    """

    try:

        meeting = Meeting.find_or_fail(id)
        meeting.delete()

        return HTTP_200, {"message": "Meeting deleted successfully."}

    except NotFoundError as error:
        raise HTTPError(HTTP_404, {"errors": str(error)})


routes = [
    Route("", get_meetings, "GET"),
    Route("/", create_meeting, "POST"),
    Route("/{id}", get_meeting_by_id, "GET"),
    Route("/{id}", update_meeting, "PUT"),
    Route("/{id}", delete_meeting, "DELETE"),
]
