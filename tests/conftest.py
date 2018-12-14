import pytest

from app import app
from faker import Faker
from random import randint
from molten import testing
from models.room import Room
from models.meeting import Meeting

fake = Faker()


@pytest.fixture(scope="session")
def client():
    return testing.TestClient(app)


@pytest.fixture()
def number():
    return randint(0, 10000)


@pytest.fixture()
def room():

    room_data = {"name": fake.name()}
    room = Room.create(**room_data)

    yield room.serialize()
    room.delete()


@pytest.fixture()
def meeting(room):

    meeting_data = {
        "title": fake.text(60),
        "date_start": fake.future_datetime().isoformat(),
        "date_end": fake.future_datetime(end_date="+10m").isoformat(),
        "owner": fake.name(),
        "room_id": room.get("id"),
    }
    meeting = Meeting.create(**meeting_data)

    yield meeting.serialize()
    meeting.delete()
