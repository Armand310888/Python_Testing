import json

from server import load_clubs, load_competitions


def test_load_clubs_returns_clubs_from_json(mocker):   
    expected_clubs = [
        {
            'name': 'Test Club 1',
            'email': 'testclub1@example.com',
            'points': '15',
        },
        {
            'name': 'Test Club 2',
            'email': 'testclub2@example.com',
            'points': '15',
        },
        {
            'name': 'Test Club 3',
            'email': 'testclub3@example.com',
            'points': '15',
        },
    ]

    json_data = {
        'clubs': expected_clubs
    }

    json_content = json.dumps(json_data)

    mocked_open = mocker.mock_open(read_data=json_content)

    mocker.patch('builtins.open', mocked_open)

    result = load_clubs()

    assert result == expected_clubs
    mocked_open.assert_called_once_with('clubs.json')


def test_load_competitions_returns_competitions_from_json(mocker):   
    expected_competitions = [
        {
            'name': 'Test Competition 1',
            'date': '2100-04-01 10:00:00',
            'numberOfPlaces': '15',
        },
        {
            'name': 'Test Competition 2',
            'date': '2100-05-01 10:00:00',
            'numberOfPlaces': '15',
        },
        {
            'name': 'Test Competition 3',
            'date': '2100-06-01 10:00:00',
            'numberOfPlaces': '15',
        },
    ]

    json_data = {
        'competitions': expected_competitions
    }

    json_content = json.dumps(json_data)

    mocked_open = mocker.mock_open(read_data=json_content)

    mocker.patch('builtins.open', mocked_open)

    result = load_competitions()

    assert result == expected_competitions
    mocked_open.assert_called_once_with('competitions.json')
