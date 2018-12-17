import pytest
import pendulum
from faker import Faker

"""
Get meetings or meeting.
"""


def test_get_all_meetings(client):

    response = client.get("/v1/meetings")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_not_found_meeting(client):

    response = client.get("/v1/meetings/100")

    assert response.status_code == 404
    assert response.json() == {"errors": "Meeting id not found"}


def test_meetings_filtered_by_invalid_room_id(client):

    fake = Faker()

    params = {"room_id": fake.name()}

    response = client.get("/v1/meetings", params=params)

    assert response.status_code == 400
    assert response.json() == {
        "errors": "The room_id need be a integer. Exemple: room_id: 100"
    }


def test_meetings_filtered_by_not_found_room_id_in_db(client, number):

    params = {"room_id": number}

    response = client.get("/v1/meetings", params=params)

    assert response.status_code == 200
    assert response.json() == []


def test_meetings_filtered_by_room_id(client, meeting):

    params = {"room_id": meeting.get("room_id")}

    response = client.get("/v1/meetings", params=params)

    assert response.status_code == 200
    assert response.json()[0].get("id") == meeting.get("id")


def test_meetings_filtered_by_invalid_date_format(client):

    fake = Faker()

    params = {"date": fake.name()}

    response = client.get("/v1/meetings", params=params)

    assert response.status_code == 400
    assert response.json() == {"errors": "The date filter format must be yyyy-mm-dd"}


def test_meetings_filtered_by_date_not_found_in_db(client, number):

    fake = Faker()

    params = {"date": fake.date(pattern="%Y-%m-%d")}

    response = client.get("/v1/meetings", params=params)

    assert response.status_code == 200
    assert response.json() == []


def test_meetings_filtered_by_date(client, meeting):

    date = meeting.get("date_start")
    date = pendulum.parse(date).to_date_string()

    params = {"date": f"{date}"}

    response = client.get("/v1/meetings", params=params)

    assert response.status_code == 200
    assert response.json()[0].get("id") == meeting.get("id")


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
            "date_end": "this field is required",
            "owner": "this field is required",
            "room_id": "this field is required",
            "date_start": "this field is required",
        }
    }


def test_create_meeting_with_wrong_date_format(client, number):

    fake = Faker()

    meeting_data = {
        "title": fake.text(10),
        "date_start": "2018-12-12",
        "date_end": "2018-12-12",
        "owner": fake.name(),
        "room_id": number,
    }

    response = client.post("/v1/meetings/", json=meeting_data)
    assert response.status_code == 400
    assert response.json() == {
        "errors": {
            "date_end": "must match pattern 2008-09-15T13:30:00",
            "date_start": "must match pattern 2008-09-15T13:30:00",
        }
    }


def test_create_meeting_with_date_start_bigger_than_end(client, room):

    fake = Faker()

    meeting_data = {
        "title": fake.text(10),
        "date_start": "2009-09-15T13:30:00",
        "date_end": "2008-09-15T13:30:00",
        "owner": fake.name(),
        "room_id": room.get("id"),
    }

    response = client.post("/v1/meetings/", json=meeting_data)
    assert response.status_code == 400
    assert response.json() == {"errors": "The date end need be bigger than date start."}


def test_create_meeting_invalid_room_id(client, number):

    fake = Faker()

    meeting_data = {
        "title": fake.text(60),
        "date_start": fake.iso8601(),
        "date_end": fake.future_datetime(end_date="+10m").isoformat(),
        "owner": fake.name(),
        "room_id": number,
    }

    response = client.post("/v1/meetings/", json=meeting_data)
    assert response.status_code == 400
    assert response.json() == {"errors": "The room id not found."}


def test_create_meeting(client, room):

    fake = Faker()

    meeting_data = {
        "title": fake.text(60),
        "date_start": fake.iso8601(),
        "date_end": fake.future_datetime(end_date="+10m").isoformat(),
        "owner": fake.name(),
        "room_id": room.get("id"),
    }

    response = client.post("/v1/meetings/", json=meeting_data)
    assert response.status_code == 201
    assert response.json() == {"message": "Meeting created successfully."}


"""
Update meeting.
"""


def test_update_meeting(client, room, meeting):

    id = meeting.get("id")

    fake = Faker()

    meeting_data = {
        "title": fake.text(60),
        "date_start": fake.iso8601(),
        "date_end": fake.future_datetime(end_date="+10m").isoformat(),
        "owner": fake.name(),
        "room_id": room.get("id"),
    }

    # Update
    response = client.put(f"/v1/meetings/{id}", json=meeting_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Meeting update successfully."}

    response = client.get(f"/v1/meetings/{id}")
    assert response.json().get("title") == meeting_data.get("title")


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
