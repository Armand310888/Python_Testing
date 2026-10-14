import pytest

from server import (
    get_booking,
    get_places_booked_for_competition,
    update_booking,
    validate_booking,
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
        "number_of_places": "15",
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


def test_validate_booking_rejects_zero_or_negative_places(
    club, competition
):
    bookings = []

    result_zero = validate_booking(
        0, 15, 15, bookings, club, competition
    )
    result_negative = validate_booking(
        -3, 15, 15, bookings, club, competition
    )

    expected = "Error-Number of Places must be positive!"

    assert result_zero == expected
    assert result_negative == expected


def test_validate_booking_rejects_insufficient_points(
    club, competition
):
    result = validate_booking(
        16, 15, 20, [], club, competition
    )

    assert result == "Error-Club does not have enough points!"


def test_validate_booking_rejects_more_than_twelve_places(
    club, competition
):
    bookings = [{
        "club": club["name"],
        "competition": competition["name"],
        "places": 8,
    }]

    result = validate_booking(
        5, 15, 15, bookings, club, competition
    )

    assert result == (
        "Error-Cannot book more than 12 places "
        "for one competition!"
    )


def test_validate_booking_rejects_insufficient_places(
    club, competition
):
    result = validate_booking(
        6, 15, 5, [], club, competition
    )

    assert result == (
        "Error-Competition does not have enough "
        "available places!"
    )


def test_validate_booking_accepts_valid_booking(
    club, competition
):
    result = validate_booking(
        3, 15, 15, [], club, competition
    )

    assert result is None


def test_validate_booking_accepts_twelve_cumulative_places(
    club, competition
):
    bookings = [{
        "club": club["name"],
        "competition": competition["name"],
        "places": 8,
    }]

    result = validate_booking(
        4, 15, 15, bookings, club, competition
    )

    assert result is None
