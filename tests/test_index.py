import pytest

from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_without_login(client):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200

def test_access_points_board_unlogged(client):
    response = client.get(
        "/displayPoints/notLogged", follow_redirects=True
    )
    data = response.data.decode()
    assert data.find("Welcome to the GUDLFT Clubs points") == 189
    