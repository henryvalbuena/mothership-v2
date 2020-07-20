"""Testing module for latte api endpoints"""
from unittest.mock import patch

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound

from tests.conftest import (
    DummyLatte,
    DuplicatedLatte,
    OperationalErrLatte,
    invalid_payload,
    dummy_latte_instance,
    dummy_payload,
    wrong_payload,
    valid_payload,
    token,
)


def test_server_running(app):
    """Test if the flask server runs"""
    with app.test_client() as client:
        res = client.get("/")
    json_data = res.get_json()
    assert "running" in json_data["status"]


@patch("src.views.lattes.Latte", dummy_latte_instance)
def test_api_latte_get(app):
    """Test GET /api/latte endpoint"""
    with app.test_client() as client:
        res = client.get("/api/latte")
    json_data = res.get_json()
    assert len(json_data["lattes"]) == 1
    assert json_data["lattes"][0]["title"] == "test"
    assert json_data["lattes"][0]["id"] == 1
    assert "testing" in json_data["lattes"][0]["ingredients"]


@patch("src.views.lattes.Latte", dummy_latte_instance)
def test_api_latte_get_id(app):
    """Test GET /api/latte/id endpoint"""
    with app.test_client() as client:
        res = client.get("/api/latte/1")
    json_data = res.get_json()
    assert json_data["lattes"]["title"] == "test"
    assert json_data["lattes"]["id"] == 1
    assert "testing" in json_data["lattes"]["ingredients"]


def test_401_api_latte_post(app):
    """Test POST /api/latte endpoint without auth token"""
    with app.test_client() as client:
        res = client.post("/api/latte", json=wrong_payload,)
    json_data = res.get_json()
    assert json_data["error"] == 401
    assert json_data["success"] is False
    assert "Missing mandatory headers" in json_data["message"]


@patch("src.views.lattes.Latte", DummyLatte)
def test_201_api_latte_post(app):
    """Test POST /api/latte endpoint with auth token"""
    with app.test_client() as client:
        res = client.post(
            "/api/latte",
            json=valid_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert res.status_code == 201
    assert json_data["success"] is True


@patch("src.views.lattes.Latte", DummyLatte)
def test_400_api_latte_post(app):
    """Test POST /api/latte endpoint with auth token bad payload"""
    with app.test_client() as client:
        res = client.post(
            "/api/latte",
            json=wrong_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 400
    assert json_data["success"] is False


@patch("src.views.lattes.Latte", DuplicatedLatte)
def test_409_api_latte_post(app):
    """Test POST /api/latte endpoint duplicate payload"""
    with app.test_client() as client:
        res = client.post(
            "/api/latte",
            json=valid_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 409
    assert json_data["success"] is False


@patch("src.views.lattes.Latte", dummy_latte_instance)
def test_200_api_latte_patch(app):
    """Test PATCH /api/latte/1 endpoint"""
    with app.test_client() as client:
        res = client.patch(
            "/api/latte/1",
            json=valid_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert res.status_code == 200
    assert json_data["success"] is True


@patch("src.views.lattes.Latte", DummyLatte(**dummy_payload, ex=NoResultFound()))
def test_404_api_latte_patch(app):
    """Test PATCH /api/latte/1 endpoint not found latte"""
    with app.test_client() as client:
        res = client.patch(
            "/api/latte/2",
            json=valid_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 404
    assert json_data["success"] is False


@patch("src.views.lattes.Latte", DummyLatte(**dummy_payload))
def test_400_api_latte_patch(app):
    """Test PATCH /api/latte endpoint with auth token bad payload"""
    with app.test_client() as client:
        res = client.patch(
            "/api/latte/1",
            json=wrong_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 400
    assert json_data["success"] is False


@patch("src.views.lattes.Latte", dummy_latte_instance)
def test_200_api_latte_delete(app):
    """Test DELETE /api/latte/1 endpoint"""
    with app.test_client() as client:
        res = client.delete(
            "/api/latte/1", headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert res.status_code == 200
    assert json_data["success"] is True


@patch("src.views.lattes.Latte", DummyLatte(**dummy_payload, ex=NoResultFound()))
def test_404_api_latte_delete(app):
    """Test DELETE /api/latte/1 endpoint not found"""
    with app.test_client() as client:
        res = client.delete(
            "/api/latte/2", headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 404
    assert json_data["success"] is False


def test_500_api_latte(app):
    """Test 500 for all methods endpoint"""
    with app.test_client() as client:
        res = client.get("/api/latte")
    json_data = res.get_json()
    assert json_data["error"] == 500
    assert json_data["success"] is False

    with app.test_client() as client:
        res = client.get("/api/latte/1")
    json_data = res.get_json()
    assert json_data["error"] == 500
    assert json_data["success"] is False

    with app.test_client() as client:
        res = client.post("/api/latte", headers={"Authorization": f"Bearer {token}"},)
    json_data = res.get_json()
    assert json_data["error"] == 500
    assert json_data["success"] is False

    with app.test_client() as client:
        res = client.patch(
            "/api/latte/1", headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 500
    assert json_data["success"] is False

    with app.test_client() as client:
        res = client.delete(
            "/api/latte/1", headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 500
    assert json_data["success"] is False


@patch(
    "src.views.lattes.Latte",
    DummyLatte(**dummy_payload, ex=OperationalError("err", "err", "err")),
)
def test_502_api_latte_get_delete_patch(app):
    """Test 502 for gets, patch, and delete methods endpoint"""
    with app.test_client() as client:
        res = client.get("/api/latte")
    json_data = res.get_json()
    assert json_data["error"] == 502
    assert json_data["success"] is False

    with app.test_client() as client:
        res = client.get("/api/latte/1")
    json_data = res.get_json()
    assert json_data["error"] == 502
    assert json_data["success"] is False

    with app.test_client() as client:
        res = client.patch(
            "/api/latte/1", headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 502
    assert json_data["success"] is False

    with app.test_client() as client:
        res = client.delete(
            "/api/latte/1", headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 502
    assert json_data["success"] is False


@patch("src.views.lattes.Latte", OperationalErrLatte)
def test_502_api_latte_post(app):
    """Test 502 for post method endpoint"""
    with app.test_client() as client:
        res = client.post(
            "/api/latte",
            json=dummy_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 502
    assert json_data["success"] is False


def test_invalid_user_input_post(app):
    """Test 400 for post method with invalid user input"""
    with app.test_client() as client:
        res = client.post(
            "/api/latte",
            json=invalid_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
    json_data = res.get_json()
    assert json_data["error"] == 400
    assert json_data["success"] is False


def test_method_not_allowed_api_latte(app):
    """Test 405 for /api/latte endpoint"""
    with app.test_client() as client:
        res = client.patch("/api/latte",)
    json_data = res.get_json()
    assert json_data["error"] == 405
    assert json_data["success"] is False


def test_method_not_allowed_api_latte_id(app):
    """Test 405 for /api/latte/1 endpoint"""
    with app.test_client() as client:
        res = client.post("/api/latte/1",)
    json_data = res.get_json()
    assert json_data["error"] == 405
    assert json_data["success"] is False


def test_method_not_allowed_put(app):
    """Test 405 for /api/latte/1 and /api/latte endpoints"""
    with app.test_client() as client:
        res = client.put("/api/latte/1",)
    json_data = res.get_json()
    assert json_data["error"] == 405
    assert json_data["success"] is False

    with app.test_client() as client:
        res = client.put("/api/latte",)
    json_data = res.get_json()
    assert json_data["error"] == 405
    assert json_data["success"] is False
