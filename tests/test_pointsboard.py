import pytest

from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_access_points_board_unlogged(client):
    response = client.get(
        "/displayPoints/notLogged", follow_redirects=True
    )
    data = response.data.decode()
    assert data.find("Welcome") == 189
    
def test_access_points_board_logged(client):
    response = client.get(
        "/displayPoints/Iron%20Temple", follow_redirects=True
    )
    data = response.data.decode()
    assert data.find("Welcome") == 189
