import pytest

from app import app
from faker import Faker
from molten import testing
from models.room import Room

fake = Faker()


@pytest.fixture(scope="session")
def client():
    return testing.TestClient(app)


@pytest.fixture()
def room():

    room_data = {"name": fake.name()}
    room = Room.create(**room_data)

    yield room.serialize()
    room.delete()
