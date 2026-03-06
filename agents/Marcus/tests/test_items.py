import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..database import engine
from .. import models

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # recreate tables
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


def test_create_list_get_update_delete_item():
    # create
    res = client.post("/api/v1/items", json={"title": "Test Item", "description": "Desc"})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Test Item"
    item_id = data["id"]

    # list
    res = client.get("/api/v1/items")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1

    # get
    res = client.get(f"/api/v1/items/{item_id}")
    assert res.status_code == 200

    # update
    res = client.patch(f"/api/v1/items/{item_id}", json={"title": "Updated"})
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Updated"
    assert data["version"] == 2

    # delete
    res = client.delete(f"/api/v1/items/{item_id}")
    assert res.status_code == 200
    res = client.get(f"/api/v1/items/{item_id}")
    assert res.status_code == 404
