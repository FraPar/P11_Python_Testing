import pytest

from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_book_page_with_bad_competition(client):
    response = client.get("/book/Error%20Festival/Iron%20Temple", follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("Welcome to the GUDLFT Registration Portal!") == 188

def test_book_page_with_bad_club(client):
    response = client.get("/book/Spring%20Festival/Error%20Temple", follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("Welcome to the GUDLFT Registration Portal!") == 188

def test_book_page_with_good_values(client):
    response = client.get("/book/Spring%20Festival/Iron%20Temple", follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("Places available:") == 231

def test_book_page_with_good_values(client):
    response = client.get("/book/Spring%20Festival/Iron%20Temple", follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("Places available:") == 231

def test_booking_on_get_request(client):
    response = client.get(
        "/purchasePlaces", follow_redirects=True)
    assert response.status_code == 405

def test_booking_on_past_competition(client):
    competition = "Spring Festival"
    club = "Iron Temple"
    response = client.post(
        "/purchasePlaces", data=dict(competition=competition, club=club), follow_redirects=True)
    data = response.data.decode()
    assert data.find("The date of the competition is in the past") == 434

def test_booking_with_negative_places(client):
    competition = "Winter Strong One"
    club = "Iron Temple"
    response = client.post(
        "/purchasePlaces", data=dict(competition=competition, club=club, places=-1 ), follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("Booking not complete!") == 434

def test_booking_with_no_places(client):
    competition = "Winter Strong One"
    club = "Iron Temple"
    response = client.post(
        "/purchasePlaces", data=dict(competition=competition, club=club, places="" ), follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("Please enter a number!") == 434

def test_booking_with_zero_places(client):
    competition = "Winter Strong One"
    club = "Iron Temple"
    response = client.post(
        "/purchasePlaces", data=dict(competition=competition, club=club, places=0 ), follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("Booking not complete!") == 434

def test_booking_with_too_much_places(client):
    competition = "Winter Strong One"
    club = "Iron Temple"
    response = client.post(
        "/purchasePlaces", data=dict(competition=competition, club=club, places=13 ), follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("Booking not complete!") == 434

def test_booking_not_enough_points(client):
    competition = "Winter Strong One"
    club = "Iron Temple"
    response = client.post(
        "/purchasePlaces", data=dict(competition=competition, club=club, places=2 ), follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("Booking not complete!") == 434

def test_booking_not_enough_places(client):
    competition = "Winter Strong One"
    club = "Strong One"
    response = client.post(
        "/purchasePlaces", data=dict(competition=competition, club=club, places=6 ), follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("There is not enough place for that many, sorry!") == 427

def test_booking_valid_updating_points_and_places(client):
    competition = "Winter Strong One"
    club = "Iron Temple"
    response = client.post(
        "/purchasePlaces", data=dict(competition=competition, club=club, places=1 ), follow_redirects=True)
    data = response.data.decode()
    print(data)
    assert response.status_code == 200
    assert data.find("Great-booking complete!") == 434
    assert data.find("Points available: 1") == 494
    assert data.find("Number of Places: 4") == 1183
