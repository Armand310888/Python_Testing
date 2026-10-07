class TestIndex:

    def test_index_displays_index_page(
        self,
        client,
        captured_templates,
    ):
        response = client.get('/')

        assert len(captured_templates) == 1

        template, _ = captured_templates[0]
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert template.name == 'index.html'
        assert 'Welcome to the GUDLFT Registration Portal!' in html
