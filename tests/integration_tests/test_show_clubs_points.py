from server import create_app


def test_show_clubs_points_displays_clubs_and_points(client, clubs):
    response = client.get('/clubs')

    html = response.get_data(as_text=True)

    assert response.status_code == 200

    for club in clubs:
        assert club['name'] in html
        assert club['points'] in html


def test_show_clubs_points_displays_message_if_no_clubs(client, competitions):

    app = create_app(
        competitions=competitions,
        clubs=[],
        bookings=[],
    )

    client = app.test_client()

    response = client.get('/clubs')

    html = response.get_data(as_text=True)

    assert response.status_code == 200

    assert 'No clubs available yet.' in html
