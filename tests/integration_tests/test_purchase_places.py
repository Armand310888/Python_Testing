class TestPurchasePlaces:

    def test_purchase_places_succeeds_with_valid_booking(
        self,
        client,
        clubs,
        competitions,
        captured_templates
    ):
        club = clubs[0]
        competition = competitions[0]
        places_required = 5

        expected_club_points_after_booking = (
            int(club['points'])
            - places_required
        )
        expected_competition_places_after_booking = (
            int(competition['numberOfPlaces'])
            - places_required
        )

        response = client.post(
            '/purchasePlaces',
            data={
                'club': club['name'],
                'competition': competition['name'],
                'places': places_required
            }
        )

        assert len(captured_templates) == 1

        template, context = captured_templates[0]
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert context['club'] == club
        assert (
            club['points']
            == expected_club_points_after_booking
        )
        assert (
            competition['numberOfPlaces']
            == expected_competition_places_after_booking
        )
        assert 'Great-booking complete!' in html

    def test_purchase_places_fails_if_not_enough_club_points(
        self,
        client,
        clubs,
        competitions,
        captured_templates,
    ):
        club = clubs[1]
        competition = competitions[0]
        places_required = 5

        expected_club_points_after_booking = (
            club['points']
        )
        expected_competition_places_after_booking = (
            competition['numberOfPlaces']
        )

        response = client.post(
            '/purchasePlaces',
            data={
                'club': club['name'],
                'competition': competition['name'],
                'places': places_required
            }
        )

        assert len(captured_templates) == 1

        template, context = captured_templates[0]
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert context['club'] == club
        assert (
            club['points']
            == expected_club_points_after_booking
        )
        assert (
            competition['numberOfPlaces']
            == expected_competition_places_after_booking
        )
        assert 'Error-Club does not have enough points!' in html

    def test_purchase_places_fail_if_not_enough_competition_places(
        self,
        client,
        clubs,
        competitions,
        captured_templates,
    ):
        club = clubs[0]
        competition = competitions[2]
        places_required = 5

        expected_club_points_after_booking = (
            club['points']
        )
        expected_competition_places_after_booking = (
            competition['numberOfPlaces']
        )

        response = client.post(
            '/purchasePlaces',
            data={
                'club': club['name'],
                'competition': competition['name'],
                'places': places_required
            }
        )

        assert len(captured_templates) == 1

        template, context = captured_templates[0]
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert context['club'] == club
        assert (
            club['points']
            == expected_club_points_after_booking
        )
        assert (
            competition['numberOfPlaces']
            == expected_competition_places_after_booking
        )
        assert (
            'Error-Competition does not have enough available places!' in html
        )
