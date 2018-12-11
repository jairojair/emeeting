import pytest
from faker import Faker

"""
Get meetings or meeting.
"""


def test_get_all_meetings(client):

    response = client.get("/v1/meetings/")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_not_found_meeting(client):

    response = client.get("/v1/meetings/100")

    assert response.status_code == 404
    assert response.json() == {"errors": "Meeting id not found"}


"""
Create meeting.
"""


def test_create_meeting_without_data(client):

    response = client.post("/v1/meetings/")
    assert response.status_code == 415


def test_create_meeting_with_wrong_data(client):

    meeting = {"": ""}

    response = client.post("/v1/meetings/", json=meeting)
    assert response.status_code == 400
    assert response.json() == {
        "errors": {
            "title": "this field is required",
            "end": "this field is required",
            "owner": "this field is required",
            "room_id": "this field is required",
            "start": "this field is required",
        }
    }


def test_create_meeting_invalid_room_id(client, number):

    fake = Faker()

    meeting_data = {
        "title": fake.text(60),
        "start": fake.future_datetime().isoformat(),
        "end": fake.future_datetime(end_date="+10m").isoformat(),
        "owner": fake.name(),
        "room_id": number,
    }

    response = client.post("/v1/meetings/", json=meeting_data)
    assert response.status_code == 400
    assert response.json() == {"errors": "The room id don't exist."}


def test_create_meeting(client, room):

    fake = Faker()

    meeting_data = {
        "title": fake.text(60),
        "start": fake.future_datetime().isoformat(),
        "end": fake.future_datetime(end_date="+10m").isoformat(),
        "owner": fake.name(),
        "room_id": room.get("id"),
    }

    response = client.post("/v1/meetings/", json=meeting_data)
    assert response.status_code == 201
    assert response.json() == {"message": "Meeting created successfully."}


"""
Delete meeting.
"""


def test_delete_not_found_meeting(client, number):

    response = client.delete(f"/v1/meetings/{number}")

    assert response.status_code == 404
    assert response.json() == {"errors": "Meeting id not found"}


def test_delete_meeting(client, meeting):

    id = meeting.get("id")

    response = client.delete(f"/v1/meetings/{id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Meeting deleted successfully."}
