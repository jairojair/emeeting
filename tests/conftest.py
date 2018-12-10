import pytest

from app import app
from molten import testing


@pytest.fixture(scope="session")
def client():
    return testing.TestClient(app)
