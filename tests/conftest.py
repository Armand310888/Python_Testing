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
        },
        {
            "name": "Test - Future Competition 2 - Available",
            "date": "2100-02-01 10:00:00",
            "numberOfPlaces": "15",
        }
    ]


@pytest.fixture
def app(clubs, competitions, bookings):
    return create_app(
        config={"TESTING": True},
        competitions=competitions,
        clubs=clubs,
        bookings=bookings,
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


@pytest.fixture
def bookings():
    return [
        {
            "club": "Test Club",
            "competition": "Test - Future Competition - Available",
            "places": 7,
        },
        {
            "club": "Test Club 2",
            "competition": "Test - Future Competition - Available",
            "places": 2,
        },
        {
            "club": "Test Club",
            "competition": "Test - Future Competition - Full",
            "places": 3,
        },
    ]
