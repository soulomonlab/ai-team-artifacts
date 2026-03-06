import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from ..encryption import encrypt, decrypt

# These tests are illustrative and use monkeypatch to avoid real HTTP calls

@pytest.mark.asyncio
async def test_encrypt_decrypt():
    s = "secret-token"
    enc = encrypt(s)
    assert enc is not None
    dec = decrypt(enc)
    assert dec == s


@pytest.mark.asyncio
async def test_exchange_code(monkeypatch):
    class FakeResp:
        def __init__(self, json_data, status_code=200):
            self._json = json_data
            self.status_code = status_code

        def json(self):
            return self._json

    async def fake_post(url, data):
        return FakeResp({"access_token": "a1", "expires_in": 3600, "refresh_token": "r1"})

    monkeypatch.setattr("httpx.AsyncClient.post", fake_post)

    # Simulate calling connect route - here we'd call the router function directly
    from ..routers.linkedin import connect
    class DummyDB:
        def __init__(self):
            self.storage = []
        def add(self, obj):
            self.storage.append(obj)
        def commit(self):
            pass
        def refresh(self, obj):
            obj.id = 1

    db = DummyDB()
    resp = await connect(code="fakecode", db=db, request=None, user=type("U", (), {"id": 2}))
    assert resp["status"] == "connected"
    assert resp["id"] == 1
