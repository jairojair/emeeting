import pytest

"""
Get meetings or meeting.
"""


def test_get_all_meetings(client):

    response = client.get("/v1/meetings/")
    assert response.status_code == 200
    assert type(response.json()) == list
