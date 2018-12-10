import logging

from molten import Route, HTTP_200, HTTP_404, HTTPError

from models.meeting import Meeting

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


routes = [Route("/", get_meetings, "GET"), Route("/{id}", get_meeting_by_id, "GET")]
