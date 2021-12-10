import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def index_call(self):
        res = self.client.get("http://127.0.0.1:5000/")
        print("INDEX CALL")
        print(res.status_code)


    @task(1)
    def login_call(self):
        res = self.client.post(
        "http://127.0.0.1:5000/showSummary", data=dict(email="john@simplylift.co")
        )
        print("LOGIN CALL")
        print(res.status_code)

    @task(1)
    def points_call(self):
        res = self.client.get(
            "http://127.0.0.1:5000/displayPoints/Iron%20Temple"
        )
        print("POINTS CALL")
        print(res.status_code)

    @task(1)
    def competition_call(self):
        res = self.client.get(
            "http://127.0.0.1:5000/book/Spring%20Festival/Iron%20Temple"
        )
        print("COMPETITION CALL")
        print(res.status_code)

    @task(1)
    def purchase_call(self):
        competition = "Spring Festival"
        club = "Strong One"
        res = self.client.post(
            "http://127.0.0.1:5000/purchasePlaces", data=dict(competition=competition, club=club, places=1)
        )
        print("BOOKING CALL")
        print(res.status_code)

    @task(1)
    def logout_call(self):
        res = self.client.get(
        "http://127.0.0.1:5000/logout"
        )
        print("LOGOUT CALL")
        print(res.status_code)
        