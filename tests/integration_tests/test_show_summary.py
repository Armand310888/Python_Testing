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

