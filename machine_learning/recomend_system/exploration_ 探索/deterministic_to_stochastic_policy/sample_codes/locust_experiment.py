from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_httpbin(self):
        self.client.get("/get")
