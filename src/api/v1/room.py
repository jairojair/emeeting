import logging

from molten import Route, HTTP_200, HTTP_201, HTTP_404, HTTP_409, HTTPError
from exceptions import ConflictError, NotFoundError

from schemas import RoomType
from models.room import Room

log = logging.getLogger(__name__)


def get_rooms():
    """
    Return all rooms.
    """

    rooms = Room.all()

    log.info("Get all rooms.")

    return HTTP_200, rooms.serialize()


def get_room_by_id(id: int):
    """
    Get room by id.
    """

    try:

        room = Room.find_or_fail(id)

        log.info(f"Get room by id: {id}")
        return HTTP_200, room.serialize()

    except NotFoundError as error:

        log.error(f"NotFoundError: {error}")
        raise HTTPError(HTTP_404, {"errors": str(error)})


def create_room(roomData: RoomType):
    """
    Create a new room.
    """

    try:

        name = roomData.name
        Room.validate(name)
        room = Room.create(name=name)

        headers = {"Content-Location": f"/v1/rooms/{room.id}"}
        msg = "Room created successfully."
        log.info(f"{msg} with id: {room.id}")

        return HTTP_201, {"message": msg}, headers

    except ConflictError as error:
        raise HTTPError(HTTP_409, {"errors": str(error)})


def update_room(id: int, roomData: RoomType):
    """
    Update a room by id
    """

    try:

        room = Room.find_or_fail(id)

        room.name = roomData.name
        room.save()

        msg = "Room update successfully."

        log.info(f"{msg} with id: {id}")
        return HTTP_200, {"message": msg}

    except NotFoundError as error:

        log.error(f"NotFoundError: {error}")
        raise HTTPError(HTTP_404, {"errors": str(error)})


def delete_room(id: int):
    """
    Delete a room by id.
    """

    try:

        room = Room.find_or_fail(id)
        room.delete()

        msg = "Room deleted successfully."

        log.info(f"{msg} with id: {id}")
        return HTTP_200, {"message": msg}

    except NotFoundError as error:

        log.error(f"NotFoundError: {error}")
        raise HTTPError(HTTP_404, {"errors": str(error)})


routes = [
    Route("/", get_rooms, "GET"),
    Route("/", create_room, "POST"),
    Route("/{id}", get_room_by_id, "GET"),
    Route("/{id}", update_room, "PUT"),
    Route("/{id}", delete_room, "DELETE"),
]
