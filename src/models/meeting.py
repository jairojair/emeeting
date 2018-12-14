from orator import Model


class Meeting(Model):

    __visible__ = ["id", "title", "date_start", "date_end", "owner", "room_id"]
    __fillable__ = ["title", "date_start", "date_end", "owner", "room_id"]
