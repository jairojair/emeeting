from orator import Model


class Room(Model):

    __visible__ = ["id", "name"]
    __fillable__ = ["name"]
