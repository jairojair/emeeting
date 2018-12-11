import logging

from molten import Route, HTTPError, HTTP_200, HTTP_201, HTTP_404, HTTP_409

from schemas import RoomType
from models.room import Room

log = logging.getLogger(__name__)


def get_rooms():
    """
    Return all rooms.
    """

    rooms = Room.all()

    return HTTP_200, rooms.serialize()


def get_room_by_id(id: int):
    """
    Get room by id.
    """

    room = _find_room(id)

    return room.serialize()


def create_room(roomData: RoomType):
    """
    Create a new room.
    """

    name = roomData.name

    if Room.where("name", name).get():

        msg = "Conflict, This room name already exists in database."
        raise HTTPError(HTTP_409, {"errors": msg})

    room = Room.create(name=name)

    headers = {"Content-Location": f"/v1/rooms/{room.id}"}

    return HTTP_201, {"message": "Room created successfully."}, headers


def update_room(id: int, roomData: RoomType):
    """
    Update a room by id
    """

    room = _find_room(id)
    room.name = roomData.name
    room.save()

    return HTTP_200, {"message": "Room update successfully."}


def delete_room(id: int):
    """
    Delete a room by id.
    """

    room = _find_room(id)
    room.delete()

    return HTTP_200, {"message": "Room deleted successfully."}


"""
Privates functions
"""


def _find_room(id):
    """
    Find a room by id
    """

    room = Room.find(id)

    if not room:
        raise HTTPError(HTTP_404, {"errors": "Room id not found"})

    return room


routes = [
    Route("/", get_rooms, "GET"),
    Route("/", create_room, "POST"),
    Route("/{id}", get_room_by_id, "GET"),
    Route("/{id}", update_room, "PUT"),
    Route("/{id}", delete_room, "DELETE"),
]
