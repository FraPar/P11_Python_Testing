import pytest

from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_summary_with_get_request(client):
    response = client.get("/showSummary", follow_redirects=True)
    assert response.status_code == 405

def test_login_user_invalid_credentials(client):
    email = "email@gmail.com"
    response = client.post(
        "/showSummary", data=dict(email=email), follow_redirects=True
    )
    data = response.data.decode()
    assert data.find("No email founded, please try again!") == 574

def test_login_user_valid_credentials(client):
    email = "john@simplylift.co"
    response = client.post(
        "/showSummary", data=dict(email=email), follow_redirects=True
    )
    data = response.data.decode()
    assert data.find("Welcome") == 202
