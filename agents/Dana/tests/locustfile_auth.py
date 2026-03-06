from locust import HttpUser, task, between
import uuid

class AuthUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.email = f"load+{uuid.uuid4().hex[:8]}@example.com"
        self.password = "LoadP@ssw0rd!"

    @task(3)
    def signup_then_login(self):
        # Signup
        res = self.client.post("/signup", json={"email": self.email, "password": self.password})
        if res.status_code not in (200, 201):
            return
        # Login
        res = self.client.post("/login", json={"email": self.email, "password": self.password})
        if res.status_code != 200:
            return
        token = None
        try:
            token = res.json().get("access_token") or res.json().get("token")
        except Exception:
            pass
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            # Hit profile read
            self.client.get("/profile", headers=headers)

    @task(1)
    def login_only(self):
        # Login attempt with random email to exercise 401 paths
        self.client.post("/login", json={"email": f"no+{uuid.uuid4().hex[:6]}@example.com", "password": "x"})
