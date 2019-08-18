def test_not_logged(client):
    response = client.get("/")
    print(response.data)


def test_logged(client, auth):
    auth.login("dziecko1", "dziecko1")

    response = client.get("/")
    print(response.data)
