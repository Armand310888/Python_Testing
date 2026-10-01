import pytest

from server import create_app


@pytest.fixture
def clubs():
    return [
        {
            "name": "Test Club",
            "email": "testclub@example.com",
            "points": "15",
        },
    ]


@pytest.fixture
def competitions():
    return [
        {
            "name": "Test - Future Competition",
            "date": "2100-01-01 10:00:00",
            "numberOfPlaces": "15",
        },
        {
            "name": "Test - Past Competition",
            "date": "2000-01-01 10:00:00",
            "numberOfPlaces": "15",
        },
    ]


@pytest.fixture
def client(clubs, competitions):
    app = create_app(
        config={"TESTING": True},
        competitions=competitions,
        clubs=clubs
    )

    return app.test_client()
