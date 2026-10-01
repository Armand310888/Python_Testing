class TestIndex:

    def test_index_returns_200(self, client):
        response = client.get('/')

        assert response.status_code == 200

    def test_index_displays_welcome_message(self, client):
        response = client.get('/')

        assert (
            "Welcome to the GUDLFT Registration Portal!"
            in response.get_data(as_text=True)
        )
