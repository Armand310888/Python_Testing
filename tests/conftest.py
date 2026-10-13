from flask import template_rendered
import json
from pathlib import Path
import pytest

from server import create_app

DATA_DIR = Path(__file__).resolve().parent / 'data/functional/'


@pytest.fixture
def clubs():
    with (
        open(DATA_DIR / 'clubs.json', encoding='utf-8')
        as clubs_file
    ):
        return json.load(clubs_file)


@pytest.fixture
def competitions():
    with (
        open(DATA_DIR / 'competitions.json', encoding='utf-8')
        as competitions_file
    ):
        return json.load(competitions_file)


@pytest.fixture
def bookings():
    with (
        open(DATA_DIR / 'bookings.json', encoding='utf-8')
        as bookings_file
    ):
        return json.load(bookings_file)


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
