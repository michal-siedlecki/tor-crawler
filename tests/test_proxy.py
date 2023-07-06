def test_privoxy(client, test_privoxy_url):
    response = client.get(test_privoxy_url)
    assert response.status_code == 200
