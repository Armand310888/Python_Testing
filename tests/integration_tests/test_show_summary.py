from flask import url_for


class TestShowSummary:

    def test_known_email_identifies_club(self, client):
        response = client.post(
            "/showSummary",
            data={"email": "testclub@example.com"},
        )

        assert response.status_code == 200
        assert (
            "Welcome, testclub@example.com"
            in response.get_data(as_text=True)
        )

    def test_unknown_email_does_not_display_club_summary(self, client):
        response = client.post(
            "/showSummary",
            data={"email": "unknowclub@example.com"},
        )

        assert response.status_code == 200
        assert (
            "Welcome to the GUDLFT Registration Portal!"
            in response.get_data(as_text=True)
        )

    def test_display_only_future_competitions(self, client):
        response = client.post(
            "/showSummary",
            data={"email": "testclub@example.com"},
        )

        assert (
            "Test - Future Competition - Available"
            in response.get_data(as_text=True)
        )
        assert (
            "Test - Future Competition - Full"
            in response.get_data(as_text=True)
        )
        assert (
            "Test - Past Competition"
            not in response.get_data(as_text=True)
        )

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
