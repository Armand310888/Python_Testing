from flask import url_for


class TestBook:

    def test_book_displays_booking_page_if_club_and_competition_exist(
        self,
        client,
        competitions,
        clubs,
        app,
        captured_templates,
    ):

        competition = competitions[0]
        club = clubs[0]

        with app.test_request_context():
            url = url_for(
                'book',
                competition=competition['name'],
                club=club['name'],
            )

        response = client.get(url)

        assert len(captured_templates) == 1

        template, context = captured_templates[0]

        assert response.status_code == 200
        assert template.name == 'booking.html'
        assert context['competition'] == competition
        assert context['club'] == club

    def test_book_displays_error_if_club_does_not_exist(
        self,
        client,
        competitions,
        app,
        captured_templates,
    ):

        competition = competitions[0]
        club = {
            'name': 'Unknown Club',
            'email': 'unknownclub@example.com',
        }

        with app.test_request_context():
            url = url_for(
                'book',
                competition=competition['name'],
                club=club['name'],
            )

        response = client.get(url)

        assert len(captured_templates) == 1

        template, _ = captured_templates[0]
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert template.name == 'index.html'
        assert 'Club not found.' in html

    def test_book_displays_error_if_competition_does_not_exist(
        self,
        client,
        clubs,
        app,
        captured_templates,
    ):

        competition = {
            'name': 'Unknown Competition',
            'date': '2100-03-01 10:00:00',
            'numberOfPlaces': '10',
        }
        club = clubs[0]

        with app.test_request_context():
            url = url_for(
                'book',
                competition=competition['name'],
                club=club['name'],
            )
        response = client.get(url)

        assert len(captured_templates) == 1

        template, context = captured_templates[0]
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert 'Something went wrong-please try again' in html
        assert context['club'] == club
