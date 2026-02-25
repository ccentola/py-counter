import os
import pytest
from fastapi.testclient import TestClient
from app.database import initialize_db
from app.api import app, get_db

TEST_DB = "test_api.db"


@pytest.fixture(autouse=True)
def fresh_db():
    """Give every test a clean, initialized database and override the db dependency."""
    initialize_db(TEST_DB)
    app.dependency_overrides[get_db] = lambda: TEST_DB
    yield
    app.dependency_overrides.clear()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


client = TestClient(app)


# GET / ========================================================================
def test_home_returns_200():
    response = client.get("/")
    assert response.status_code == 200


def test_home_displays_counter_value():
    response = client.get("/")
    assert "0" in response.text


def test_home_contains_increment_button():
    response = client.get("/")
    assert "increment" in response.text.lower()


def test_home_contains_decrement_button():
    response = client.get("/")
    assert "decrement" in response.text.lower()


def test_home_contains_reset_button():
    response = client.get("/")
    assert "reset" in response.text.lower()


# POST /increment ==============================================================
def test_increment_returns_200():
    response = client.post("/increment")
    assert response.status_code == 200


def test_increment_updates_value():
    client.post("/increment")
    response = client.post("/increment")
    assert "2" in response.text


def test_increment_returns_html_fragment():
    response = client.post("/increment")
    assert "text/html" in response.headers["content-type"]


# POST /decrement ==============================================================
def test_decrement_returns_200():
    client.post("/increment")
    response = client.post("/decrement")
    assert response.status_code == 200


def test_decrement_updates_value():
    client.post("/increment")
    client.post("/increment")
    response = client.post("/decrement")
    assert "1" in response.text


def test_decrement_at_zero_returns_error_message():
    response = client.post("/decrement")
    assert "cannot be negative" in response.text.lower()


def test_decrement_at_zero_does_not_change_value():
    client.post("/decrement")
    response = client.get("/")
    assert "0" in response.text


# POST /reset ==================================================================
def test_reset_returns_200():
    response = client.post("/reset")
    assert response.status_code == 200


def test_reset_sets_value_to_zero():
    client.post("/increment")
    client.post("/increment")
    client.post("/increment")
    response = client.post("/reset")
    assert "0" in response.text
