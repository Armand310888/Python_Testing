import pytest

from server import (
    get_booking,
    get_places_booked_for_competition,
    update_booking,
)


@pytest.fixture
def club():
    return {
        "name": "Test Club",
        "email": "testclub@example.com",
        "points": "15",
    }


@pytest.fixture
def competition():
    return {
        "name": "Test Competition",
        "date": "2100-01-01 10:00:00",
        "numberOfPlaces": "15",
    }


def test_get_booking_returns_matching_booking(
    club,
    competition,
):

    expected_booking = {
            "club": "Test Club",
            "competition": "Test Competition",
            "places": 8,
    }

    bookings = [expected_booking]

    result = get_booking(
        club,
        competition,
        bookings,
    )

    assert result == expected_booking


def test_get_booking_returns_none_if_competition_does_not_match(
    club,
    competition,
):

    bookings = [
        {
            "club": "Test Club",
            "competition": "Another Test Competition",
            "places": 8,
        }
    ]

    result = get_booking(
        club,
        competition,
        bookings,
    )

    assert result is None


def test_get_booking_returns_none_if_club_does_not_match(
    club,
    competition,
):

    bookings = [
        {
            "club": "Another Test Club",
            "competition": "Test Competition",
            "places": 8,
        }
    ]

    result = get_booking(
        club,
        competition,
        bookings,
    )

    assert result is None


def test_get_places_booked_for_existing_booking(
    club,
    competition,
):

    bookings = [
        {
            "club": "Test Club",
            "competition": "Test Competition",
            "places": 8,
        }
    ]

    result = get_places_booked_for_competition(
        club,
        competition,
        bookings,
    )

    assert result == 8


def test_get_places_returns_zero_if_no_booking(
    club,
    competition,
):

    bookings = []

    result = get_places_booked_for_competition(
        club,
        competition,
        bookings,
    )

    assert result == 0


def test_update_booking_updates_existing_booking(
    club,
    competition,
):
    bookings = [
        {
            "club": "Test Club",
            "competition": "Test Competition",
            "places": 8,
        }
    ]

    places_required = 3

    update_booking(
        club,
        competition,
        places_required,
        bookings
    )

    updated_booking = get_booking(
        club,
        competition,
        bookings,
    )

    assert updated_booking['places'] == 11


def test_update_booking_creates_new_booking_if_does_not_exist(
    club,
    competition,
):
    bookings = []

    places_required = 3

    update_booking(
        club,
        competition,
        places_required,
        bookings
    )

    new_booking = {
        'club': club['name'],
        'competition': competition['name'],
        'places': places_required
    }

    assert new_booking in bookings
