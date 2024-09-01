from locust import HttpUser, between, task

# サンプルコード
# class MyUser(HttpUser):
#     wait_time = between(1, 5)

#     @task(weight=1)
#     def test_httpbin_get(self):
#         self.client.get("/get")

#     @task(weight=1)
#     def test_httpbin_post(self):
#         self.client.post("/post", json={"key": "value"})


class recommendedMovieUser(HttpUser):
    wait_time = between(1, 5)
    USER_ID = "U:114521"
    K = 20
    ENDPOINT = f"/temp/recommended-movies/{USER_ID}"
    REQUEST_HEADER = {"content-type": "application/json", "accept": "application/json"}

    @task(weight=1)
    def test_deterministic(self) -> None:
        inference_type = "deterministic"
        self.client.get(
            url=self.ENDPOINT,
            params={"inference_type": inference_type, "k": self.K},
            headers=self.REQUEST_HEADER,
        )

    @task(weight=1)
    def test_stochastic_plackett_luce(self) -> None:
        inference_type = "stochastic_plackett_luce"
        self.client.get(
            url=self.ENDPOINT,
            params={"inference_type": inference_type, "k": self.K},
            headers=self.REQUEST_HEADER,
        )

    @task(weight=1)
    def test_stochastic_plackett_luce_cached(self) -> None:
        inference_type = "stochastic_plackett_luce_cached"
        self.client.get(
            url=self.ENDPOINT,
            params={"inference_type": inference_type, "k": self.K},
            headers=self.REQUEST_HEADER,
        )

    @task(weight=1)
    def test_stochastic_gumbel_softmax_trick(self) -> None:
        inference_type = "stochastic_gumbel_softmax_trick"
        self.client.get(
            url=self.ENDPOINT,
            params={"inference_type": inference_type, "k": self.K},
            headers=self.REQUEST_HEADER,
        )

    @task(weight=1)
    def test_stochastic_epsilon_greedy(self) -> None:
        inference_type = "stochastic_epsilon_greedy"
        self.client.get(
            url=self.ENDPOINT,
            params={"inference_type": inference_type, "k": self.K},
            headers=self.REQUEST_HEADER,
        )
