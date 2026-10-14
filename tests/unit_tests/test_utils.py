
from datetime import datetime, timedelta

from server import (
    find_club,
    find_competition,
    get_future_competitions,
    update_competition_places,
    update_club_points,
)


def test_find_club_by_name():
    clubs = [
        {"name": "Simply Lift", "email": "simply@test.com"},
        {"name": "Iron Temple", "email": "iron@test.com"},
    ]

    result = find_club("Iron Temple", "name", clubs)

    assert result is clubs[1]


def test_find_club_by_email():
    clubs = [
        {"name": "Simply Lift", "email": "simply@test.com"},
        {"name": "Iron Temple", "email": "iron@test.com"},
    ]

    result = find_club("simply@test.com", "email", clubs)

    assert result is clubs[0]


def test_find_club_not_found():
    clubs = [{"name": "Simply Lift", "email": "simply@test.com"}]

    assert find_club("Unknown", "name", clubs) is None
    assert find_club(None, "email", clubs) is None
    assert find_club("Simply Lift", "name", []) is None


def test_find_competition_found():
    competitions = [
        {"name": "Spring Festival"},
        {"name": "Fall Classic"},
    ]

    result = find_competition("Fall Classic", competitions)

    assert result is competitions[1]


def test_find_competition_not_found():
    competitions = [{"name": "Spring Festival"}]

    assert find_competition("Unknown", competitions) is None
    assert find_competition(None, competitions) is None
    assert find_competition("Spring Festival", []) is None


def test_get_future_competitions():
    past_date = datetime.now() - timedelta(days=10)
    future_date = datetime.now() + timedelta(days=10)

    competitions = [
        {
            "name": "Past",
            "date": past_date.strftime("%Y-%m-%d %H:%M:%S"),
        },
        {
            "name": "Future",
            "date": future_date.strftime("%Y-%m-%d %H:%M:%S"),
        },
    ]

    result = get_future_competitions(competitions)

    assert result == [competitions[1]]


def test_get_future_competitions_no_future():
    past_date = datetime.now() - timedelta(days=10)
    competitions = [{
        "name": "Past",
        "date": past_date.strftime("%Y-%m-%d %H:%M:%S"),
    }]

    assert get_future_competitions(competitions) == []
    assert get_future_competitions([]) == []


def test_update_competition_places():
    competition = {"number_of_places": "20"}

    result = update_competition_places(competition, 5)

    assert competition["number_of_places"] == 15
    assert isinstance(competition["number_of_places"], int)
    assert result is None


def test_update_club_points():
    club = {"points": "15"}

    result = update_club_points(club, 5)

    assert club["points"] == 10
    assert isinstance(club["points"], int)
    assert result is None
