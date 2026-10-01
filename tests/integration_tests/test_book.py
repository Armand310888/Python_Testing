from flask import url_for


class TestBook:

    def test_book_displays_booking_page_if_club_and_competition_exist(
        self,
        client,
        competitions,
        clubs,
        app,
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

        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert competition['name'] in html
        assert competition['numberOfPlaces'] in html
        assert club['name'] in html
