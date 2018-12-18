import pytest
from faker import Faker

fake = Faker()

"""
Get rooms or room.
"""


def test_get_all_rooms(client):

    response = client.get("/v1/rooms/")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_try_get_not_found_room(client):

    response = client.get("/v1/rooms/100")
    assert response.status_code == 404
    assert response.json() == {"errors": "Room id not found"}


def test_get_wrong_room_id_type(client):

    response = client.get("/v1/rooms/kong")
    assert response.status_code == 400
    assert response.json() == {"errors": {"id": "invalid int value"}}


"""
Create room.
"""


def test_create_room_without_data(client):

    response = client.post("/v1/rooms/")
    assert response.status_code == 415


def test_create_room_with_wrong_data(client):

    room = {"": ""}

    response = client.post("/v1/rooms/", json=room)
    assert response.status_code == 400
    assert response.json() == {"errors": {"name": "this field is required"}}


def test_create_room_with_empty_string(client):

    room = {"name": ""}

    response = client.post("/v1/rooms/", json=room)
    assert response.status_code == 400
    assert response.json() == {"errors": {"name": "length must be >= 1"}}


def test_create_room_with_max_length(client):

    room = {"name": fake.text(200)}

    response = client.post("/v1/rooms/", json=room)
    assert response.status_code == 400
    assert response.json() == {"errors": {"name": "length must be <= 60"}}


def test_create_room_with_wrong_type(client):

    room = {"name": 100}

    response = client.post("/v1/rooms/", json=room)
    assert response.status_code == 400
    assert response.json() == {"errors": {"name": "unexpected type int"}}


def test_create_room_already_exists(client, room):

    expected = {"errors": "Conflict, This room name already exists in database."}

    response = client.post("/v1/rooms/", json=room)
    location = response.headers.get("Content-Location")

    response = client.post("/v1/rooms/", json=room)
    assert response.status_code == 409
    assert response.json() == expected


def test_create_and_delete_room(client):

    room = {"name": fake.name()}

    response = client.post("/v1/rooms/", json=room)
    assert response.status_code == 201
    assert response.json() == {"message": "Room created successfully."}

    # Delete room
    location = response.headers.get("Content-Location")
    response = client.delete(location)
    assert response.status_code == 200


def test_delete_room_not_found(client, number):

    response = client.delete(f"/v1/rooms/{number}")
    assert response.status_code == 404
    assert response.json() == {"errors": "Room id not found"}


"""
Update room.
"""


def test_update_room(client, room):

    id = room.get("id")
    new_room = {"name": fake.name()}

    # Update
    response = client.put(f"/v1/rooms/{id}", json=new_room)
    assert response.status_code == 200

    response = client.get(f"/v1/rooms/{id}")
    assert response.json().get("name") == new_room.get("name")
