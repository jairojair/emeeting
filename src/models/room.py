from orator import Model
from exceptions import ConflictError, NotFoundError


class Room(Model):

    __visible__ = ["id", "name"]
    __fillable__ = ["name"]

    @staticmethod
    def validate(name):
        """
        validate data.
        """

        if Room.where("name", name).get():
            raise ConflictError("Conflict, This room name already exists in database.")

    @staticmethod
    def find_or_fail(id):
        """
        Find a room by id
        """

        room = Room.find(id)

        if not room:
            raise NotFoundError("Room id not found")

        return room
