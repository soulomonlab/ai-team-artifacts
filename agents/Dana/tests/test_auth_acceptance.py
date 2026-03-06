import os
import requests
import pytest

BASE = os.getenv('TEST_API_BASE', 'https://staging.example.com/v1')

TEST_EMAIL = f"qa+{int(os.times()[4])}@example.com"
TEST_PASSWORD = "P@ssw0rd!QA"


def signup_session():
    url = f"{BASE}/auth/signup"
    payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    resp = requests.post(url, json=payload)
    return resp


def login_session():
    url = f"{BASE}/auth/login"
    payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    resp = requests.post(url, json=payload)
    return resp


def test_signup_and_get_me():
    # Signup
    r = signup_session()
    assert r.status_code == 201, r.text
    body = r.json()
    assert 'access_token' in body
    # Cookie
    assert 'refresh_token' in r.cookies or any('refresh_token' in c for c in r.headers.get('Set-Cookie',''))

    access = body['access_token']
    # Get me
    r2 = requests.get(f"{BASE}/users/me", headers={"Authorization": f"Bearer {access}"})
    assert r2.status_code == 200
    data = r2.json()
    assert 'email' in data and data['email'] == TEST_EMAIL


def test_login_and_refresh_and_logout():
    r = login_session()
    assert r.status_code == 200
    body = r.json()
    assert 'access_token' in body
    access = body['access_token']

    # refresh using cookie
    cookies = r.cookies
    r2 = requests.post(f"{BASE}/auth/refresh", cookies=cookies)
    assert r2.status_code == 200
    b2 = r2.json()
    assert 'access_token' in b2

    # logout
    r3 = requests.post(f"{BASE}/auth/logout", cookies=cookies)
    assert r3.status_code in (200,204)
