import os
import uuid
import requests
import pytest

BASE_URL = os.getenv("BASE_URL")

@pytest.fixture(autouse=True)
def require_base_url():
    if not BASE_URL:
        pytest.skip("BASE_URL not set; skipping E2E tests")

def make_email():
    return f"qa+{uuid.uuid4().hex[:8]}@example.com"

def test_signup_login_update_profile():
    email = make_email()
    password = "P@ssw0rd123!"

    # 1) Signup
    signup_url = f"{BASE_URL}/signup"
    r = requests.post(signup_url, json={"email": email, "password": password})
    assert r.status_code in (200, 201), f"Signup failed: {r.status_code} {r.text}"

    # 2) Login
    login_url = f"{BASE_URL}/login"
    r = requests.post(login_url, json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.status_code} {r.text}"
    data = r.json()

    # Accept common token shapes
    token = data.get("access_token") or data.get("token") or data.get("id_token")
    assert token, f"No token returned in login response: {data}"

    headers = {"Authorization": f"Bearer {token}"}

    # 3) Profile update
    profile_url = f"{BASE_URL}/profile"
    new_display_name = "QA Tester " + uuid.uuid4().hex[:6]
    r = requests.patch(profile_url, json={"display_name": new_display_name}, headers=headers)
    assert r.status_code in (200, 204), f"Profile update failed: {r.status_code} {r.text}"

    # 4) Read back profile (if endpoint exists)
    r = requests.get(profile_url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        assert data.get("display_name") == new_display_name, f"Profile display_name not updated: {data}"
