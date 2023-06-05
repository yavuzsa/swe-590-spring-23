import time
from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def visit_page(self):
        self.client.get(url="/")

        
    @task
    def visit_page(self):
        self.client.post("/dev", {"days": 1, "hours": 1, "operation": "minutes" })