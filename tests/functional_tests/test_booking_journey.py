from flask import url_for

from server import (
    get_places_booked_for_competition
)


def test_successful_booking_journey(
    client,
    app,
    clubs,
    competitions,
    captured_templates,
    bookings,
):

    club = clubs[0]
    competition = competitions[0]
    places_required = 5

    # Step 1: connexion
    response = client.get('/')

    assert response.status_code == 200
    assert captured_templates[-1][0].name == 'index.html'

    # Step 2: identification and competitions display
    response = client.post(
        '/showSummary',
        data={'email': club['email']}
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert captured_templates[-1][0].name == 'welcome.html'
    assert captured_templates[-1][1]['club'] == club
    assert 'Test - Future Competition - Available' in html
    assert 'Test - Future Competition - Full' in html
    assert 'Test - Past Competition' not in html

    # Step 3: access booking
    with app.test_request_context():
        url = url_for(
            'book',
            competition=competition['name'],
            club=club['name'],
        )

    response = client.get(url)

    assert response.status_code == 200
    assert captured_templates[-1][0].name == 'booking.html'
    assert captured_templates[-1][1]['competition'] == competition
    assert captured_templates[-1][1]['club'] == club

    # Step 4: purchase places
    expected_club_points_after_booking = (
        int(club['points'])
        - places_required
    )
    expected_competition_places_after_booking = (
        int(competition['numberOfPlaces'])
        - places_required
    )
    expected_booked_places_after_booking = (
        get_places_booked_for_competition(
            club,
            competition,
            bookings,
        )
        + places_required
    )

    response = client.post(
        '/purchasePlaces',
        data={
            'club': club['name'],
            'competition': competition['name'],
            'places': places_required
        }
    )

    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert captured_templates[-1][0].name == 'welcome.html'
    assert captured_templates[-1][1]['club'] == club
    assert (
        club['points']
        == expected_club_points_after_booking
    )
    assert (
        competition['numberOfPlaces']
        == expected_competition_places_after_booking
    )
    assert (
        get_places_booked_for_competition(
            club,
            competition,
            bookings,
        )
        == expected_booked_places_after_booking
    )
    assert 'Great-booking complete!' in html

    # Step 5: logout
    response = client.get('/logout')

    assert response.status_code == 302
    assert response.location == 'http://localhost/'


def test_booking_journey_rejected_for_insufficient_points(
    client,
    app,
    clubs,
    competitions,
    captured_templates,
    bookings,
):

    club = clubs[1]
    competition = competitions[0]
    places_required = 7

    # Step 1: connexion
    response = client.get('/')

    assert response.status_code == 200
    assert captured_templates[-1][0].name == 'index.html'

    # Step 2: identification and competitions display
    response = client.post(
        '/showSummary',
        data={'email': club['email']}
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert captured_templates[-1][0].name == 'welcome.html'
    assert captured_templates[-1][1]['club'] == club
    assert 'Test - Future Competition - Available' in html
    assert 'Test - Future Competition - Full' in html
    assert 'Test - Past Competition' not in html

    # Step 3: access booking
    with app.test_request_context():
        url = url_for(
            'book',
            competition=competition['name'],
            club=club['name'],
        )

    response = client.get(url)

    assert response.status_code == 200
    assert captured_templates[-1][0].name == 'booking.html'
    assert captured_templates[-1][1]['competition'] == competition
    assert captured_templates[-1][1]['club'] == club

    # Step 4: purchase places
    expected_club_points_after_booking = club['points']

    expected_competition_places_after_booking = competition['numberOfPlaces']

    expected_booked_places_after_booking = (
        get_places_booked_for_competition(
            club,
            competition,
            bookings,
        )
    )

    response = client.post(
        '/purchasePlaces',
        data={
            'club': club['name'],
            'competition': competition['name'],
            'places': places_required
        }
    )

    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert captured_templates[-1][0].name == 'welcome.html'
    assert captured_templates[-1][1]['club'] == club
    assert (
        club['points']
        == expected_club_points_after_booking
    )
    assert (
        competition['numberOfPlaces']
        == expected_competition_places_after_booking
    )
    assert (
        get_places_booked_for_competition(
            club,
            competition,
            bookings,
        )
        == expected_booked_places_after_booking
    )
    assert 'Error-Club does not have enough points!' in html
