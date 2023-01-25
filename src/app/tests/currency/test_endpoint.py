
def test_convert(client):
    """
    GIVEN
    WHEN convert endpoint is called with GET method and valid params
    THEN response with status 200
    """
    response = client.get(
        "/convert",
        params={'amount': 100, 'from_currency': 'USD', 'to_currency': 'EUR'}
    )
    assert response.status_code == 200
