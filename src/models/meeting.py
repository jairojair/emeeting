import re
import logging
import pendulum

from orator import Model
from orator.orm import scope

from models.room import Room

log = logging.getLogger(__name__)


class ConflictError(Exception):
    pass


class ValidateError(Exception):
    pass


class Meeting(Model):

    __visible__ = ["id", "title", "date_start", "date_end", "owner", "room_id"]
    __fillable__ = ["title", "date_start", "date_end", "owner", "room_id"]

    def validate(self, meetingData):
        """
        Describe
        """

        date_start = meetingData.date_start
        room_id = meetingData.room_id

        self.__check_if_room_exist(room_id)
        self.__check_dates_logic(meetingData.date_end, date_start)
        self.__check_if_room_is_available(room_id, date_start)

    def __check_if_room_exist(self, id):
        """
        check if room exist.
        """

        if not Room.find(id):
            raise ValidateError("The room id not found.")

    def __check_dates_logic(self, end, start):
        """
        Check if date end is bigger than date start.
        """

        if not pendulum.parse(end) > pendulum.parse(start):
            raise ValidateError("The date end need be bigger than date start.")

    def __check_if_room_is_available(self, room_id, date):
        """
        """

        meeting_date_to_string = pendulum.parse(date).to_date_string()

        meetings = Meeting.by_room_id(room_id).by_date(meeting_date_to_string).get()

        self.__check_in_period(pendulum.parse(date), meetings)

    def __check_in_period(self, date_meeting, meetings):
        """
        """

        for meeting in meetings:

            start = pendulum.parse(meeting.date_start)
            end = pendulum.parse(meeting.date_end)

            period = end - start

            if date_meeting in period:
                raise ConflictError("Conflict, the room isn't available in this time.")

    @scope
    def by_room_id(self, query, id):
        """
        Filter meetings by room id.
        """

        try:

            if id is None:
                return

            id = int(id)
            return query.where("room_id", id)

        except ValueError:
            raise Exception("The room_id need be a integer. Exemple: room_id: 100")

    @scope
    def by_date(self, query, date):
        """
        Filter meetings by date.
        """

        if date is None:
            return

        date_filter_format = r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$"

        if not re.match(date_filter_format, date):
            raise Exception("The date filter format must be yyyy-mm-dd")

        return query.where("date_start", "like", f"%{date}%")
