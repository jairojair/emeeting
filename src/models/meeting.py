import re
import pendulum

from orator import Model
from orator.orm import scope

from models.room import Room


class Meeting(Model):

    __visible__ = ["id", "title", "date_start", "date_end", "owner", "room_id"]
    __fillable__ = ["title", "date_start", "date_end", "owner", "room_id"]

    def validate(self, meetingData):

        data = meetingData

        # check if room exist.

        room = Room.find(data.room_id)

        if not room:
            raise Exception("The room id not found.")

        # Check if date end is bigger than date start.

        if not pendulum.parse(data.date_end) > pendulum.parse(data.date_start):
            raise Exception("The date end need be bigger than date start.")

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
        Describe
        """

        if date is None:
            return

        date_filter_format = r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$"

        if not re.match(date_filter_format, date):
            raise Exception("The date filter format must be yyyy-mm-dd")

        return query.where("date_start", "like", f"%{date}%")
