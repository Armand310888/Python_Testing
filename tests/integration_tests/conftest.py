from flask import template_rendered
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
        {
            "name": "Test Club 2",
            "email": "testclub2@example.com",
            "points": "2",
        },
    ]


@pytest.fixture
def competitions():
    return [
        {
            "name": "Test - Future Competition - Available",
            "date": "2100-01-01 10:00:00",
            "numberOfPlaces": "15",
        },
        {
            "name": "Test - Past Competition",
            "date": "2000-01-01 10:00:00",
            "numberOfPlaces": "15",
        },
        {
            "name": "Test - Future Competition - Full",
            "date": "2100-02-01 10:00:00",
            "numberOfPlaces": "0",
        }
    ]


@pytest.fixture
def app(clubs, competitions):
    return create_app(
        config={"TESTING": True},
        competitions=competitions,
        clubs=clubs
    )


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    with template_rendered.connected_to(record, app):
        yield recorded
