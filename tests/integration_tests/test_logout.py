from urllib.parse import urlparse


def test_logout_redirects_to_index(client):
    response = client.get('/logout')

    assert response.status_code == 302
    assert urlparse(response.location).path == '/'
