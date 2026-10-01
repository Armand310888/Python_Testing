from flask import url_for


class TestShowSummary:

    def test_known_email_identifies_club(
        self,
        client,
        captured_templates,
        clubs,
    ):
        club = clubs[0]

        response = client.post(
            '/showSummary',
            data={'email': club['email']},
        )

        assert len(captured_templates) == 1

        template, context = captured_templates[0]

        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert context['club'] == club

    def test_unknown_email_does_not_display_club_summary(
        self,
        client,
        captured_templates,
    ):
        response = client.post(
            "/showSummary",
            data={"email": "unknownclub@example.com"},
        )

        assert len(captured_templates) == 1

        template, _ = captured_templates[0]
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert template.name == 'index.html'
        assert 'Club not found.' in html

    def test_display_only_future_competitions(self, client):
        response = client.post(
            "/showSummary",
            data={"email": "testclub@example.com"},
        )

        html = response.get_data(as_text=True)

        assert 'Test - Future Competition - Available' in html
        assert 'Test - Future Competition - Full' in html
        assert 'Test - Past Competition' not in html

    def test_future_competition_displays_booking_link_if_places_available(
        self,
        client,
        competitions,
        clubs,
        app
    ):

        response = client.post(
            "/showSummary",
            data={"email": "testclub@example.com"},
        )

        competition = competitions[0]
        club = clubs[0]

        with app.test_request_context():
            url = url_for(
                'book',
                competition=competition['name'],
                club=club['name'],
            )

        assert url in response.get_data(as_text=True)

    def test_future_competition_hides_booking_link_if_no_places_available(
            self,
            client,
            competitions,
            clubs,
            app
    ):

        response = client.post(
            "/showSummary",
            data={"email": "testclub@example.com"},
        )

        competition = competitions[2]
        club = clubs[0]

        with app.test_request_context():
            url = url_for(
                'book',
                competition=competition['name'],
                club=club['name'],
            )

        assert url not in response.get_data(as_text=True)
