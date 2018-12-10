import logging

from molten import Route, HTTP_200

from models.meeting import Meeting

log = logging.getLogger(__name__)


def get_meetings():
    """
    Return all meetings.
    """

    meetings = Meeting.all()

    return HTTP_200, meetings.serialize()


routes = [Route("/", get_meetings, "GET")]
