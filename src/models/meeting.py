from orator import Model


class Meeting(Model):

    __visible__ = ["id", "title", "start", "end", "owner", "room_id"]
    __fillable__ = ["title", "start", "end", "owner", "room_id"]
