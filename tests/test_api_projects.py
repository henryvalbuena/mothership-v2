"""Testing module for latte api endpoints"""
import json
from unittest.mock import MagicMock, patch

from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import NoResultFound

from tests.auth0_token import project_token
from tests.conftest import (
    DummyProject,
    dummy_project_instance,
    invalid_payload,
    project_payload_good,
)

project_token = project_token()


@patch("src.apis.projects.Project", dummy_project_instance)
def test_api_project_get(app):
    """Test api GET /api/project endpoint"""
    with app.test_client() as client:
        res = client.get("/api/project")
    json_data = res.get_json()[0]

    assert json_data["title"] == "test"
    assert json_data["meta"] == '["meta", "testing"]'
    assert json.loads(json_data["meta"]) == ["meta", "testing"]
    assert json_data["description"] == "some testing"
    assert json_data["image"] == "image.png"
    assert json_data["git_repo"] == "github.com"
    assert json_data["demo_link"] == "heroku.com"
    assert res.status_code == 200


@patch("src.apis.projects.Project", DummyProject)
def test_api_project_post(app):
    """Test api POST /api/project endpoint"""
    with app.test_client() as client:
        res = client.post(
            "/api/project",
            json=project_payload_good,
            headers={"Authorization": f"Bearer {project_token}"},
        )
    json_data = res.get_json()

    assert json_data["title"] == "test"
    assert json_data["meta"] == '["meta", "testing"]'
    assert json.loads(json_data["meta"]) == ["meta", "testing"]
    assert json_data["description"] == "some testing"
    assert json_data["image"] == "image.png"
    assert json_data["git_repo"] == "github.com"
    assert json_data["demo_link"] == "heroku.com"
    assert res.status_code == 201


@patch("src.apis.projects.Project", dummy_project_instance)
def test_api_project_patch(app):
    """Test api PATCH /api/project/1 endpoint"""
    with app.test_client() as client:
        res = client.patch(
            "/api/project/1",
            json=project_payload_good,
            headers={"Authorization": f"Bearer {project_token}"},
        )
    json_data = res.get_json()

    assert json_data["title"] == "test"
    assert json_data["meta"] == '["meta", "testing"]'
    assert json.loads(json_data["meta"]) == ["meta", "testing"]
    assert json_data["description"] == "some testing"
    assert json_data["image"] == "image.png"
    assert json_data["git_repo"] == "github.com"
    assert json_data["demo_link"] == "heroku.com"
    assert res.status_code == 200


@patch("src.apis.projects.Project", MagicMock())
def test_api_project_delete(app):
    """Test api DELETE /api/project/1 endpoint"""
    with app.test_client() as client:
        res = client.delete("/api/project/1", headers={"Authorization": f"Bearer {project_token}"},)
    json_data = res.get_json()

    assert json_data["success"] is True
    assert json_data["project_id"] == 1
    assert res.status_code == 200


@patch("src.apis.projects.Project", dummy_project_instance)
def test_api_project_get_by_id(app):
    """Test api GET /api/project/1 endpoint"""
    with app.test_client() as client:
        res = client.get("/api/project/1")
    json_data = res.get_json()

    assert json_data["title"] == "test"
    assert json_data["meta"] == '["meta", "testing"]'
    assert json.loads(json_data["meta"]) == ["meta", "testing"]
    assert json_data["description"] == "some testing"
    assert json_data["image"] == "image.png"
    assert json_data["git_repo"] == "github.com"
    assert json_data["demo_link"] == "heroku.com"
    assert res.status_code == 200


@patch(
    "src.apis.projects.Project",
    MagicMock(**{"query.all.side_effect": OperationalError("err", "err", "err")}),
)
def test_api_project_get_db_error(app):
    """Test api GET /api/project endpoint db error"""
    with app.test_client() as client:
        res = client.get("/api/project")
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 502
    assert "invalid response from an upstream server" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(**{"query.all.side_effect": Exception}),
)
def test_api_project_get_exception(app):
    """Test api GET /api/project endpoint exception"""
    with app.test_client() as client:
        res = client.get("/api/project")
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 500
    assert "The server encountered an internal error" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(**{"query.filter.side_effect": NoResultFound}),
)
def test_api_project_get__id_not_found(app):
    """Test api GET /api/project/1 endpoint not found"""
    with app.test_client() as client:
        res = client.get("/api/project/1")
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 404
    assert "The requested URL was not found on the server" in json_data["message"]


@patch(
    "src.apis.projects.Project",
    MagicMock(**{"query.filter.side_effect": OperationalError("err", "err", "err")}),
)
def test_api_project_get_by_id_db_error(app):
    """Test api GET /api/project/1 endpoint db error"""
    with app.test_client() as client:
        res = client.get("/api/project/1")
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 502
    assert "invalid response from an upstream server" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(**{"query.filter.side_effect": Exception}),
)
def test_api_project_get_by_id_exception(app):
    """Test api GET /api/project/1 endpoint exception"""
    with app.test_client() as client:
        res = client.get("/api/project/1")
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 500
    assert "The server encountered an internal error" in json_data["message"]


def test_api_project_get_id_not_int(app):
    """Test api GET /api/project/wrong endpoint not found"""
    with app.test_client() as client:
        res = client.get("/api/project/wrong")
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 404
    assert "The requested URL was not found on the server" in json_data["message"]


def test_api_project_post_bad_payload(app):
    """Test api POST /api/project endpoint bad payload"""
    with app.test_client() as client:
        res = client.post(
            "/api/project",
            json=invalid_payload,
            headers={"Authorization": f"Bearer {project_token}"},
        )
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 400
    assert "sent a request that this server could not understand" in json_data["message"]


def test_api_project_post_incomplete_payload(app):
    """Test api POST /api/project endpoint incomplete payload"""
    with app.test_client() as client:
        res = client.post(
            "/api/project",
            json={"title": "some", "image": "file.png"},
            headers={"Authorization": f"Bearer {project_token}"},
        )
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 400
    assert "sent a request that this server could not understand" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(side_effect=IntegrityError("err", "err", "err")),
)
def test_api_project_post_duplicated(app):
    """Test api POST /api/project endpoint duplicated"""
    with app.test_client() as client:
        res = client.post(
            "/api/project",
            json=project_payload_good,
            headers={"Authorization": f"Bearer {project_token}"},
        )
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 409
    assert "A conflict happened while processing the request" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(side_effect=OperationalError("err", "err", "err")),
)
def test_api_project_post_db_error(app):
    """Test api POST /api/project endpoint db error"""
    with app.test_client() as client:
        res = client.post(
            "/api/project",
            json=project_payload_good,
            headers={"Authorization": f"Bearer {project_token}"},
        )
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 502
    assert "invalid response from an upstream server" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(side_effect=Exception),
)
def test_api_project_post_exception(app):
    """Test api POST /api/project endpoint exception"""
    with app.test_client() as client:
        res = client.post(
            "/api/project",
            json=project_payload_good,
            headers={"Authorization": f"Bearer {project_token}"},
        )
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 500
    assert "The server encountered an internal error" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(),
)
def test_api_project_patch_incomplete_payload(app):
    """Test api PATCH /api/project endpoint incomplete payload"""
    with app.test_client() as client:
        res = client.patch(
            "/api/project/1",
            json={"title": "some", "image": "file.png"},
            headers={"Authorization": f"Bearer {project_token}"},
        )
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 400
    assert "sent a request that this server could not understand" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(**{"query.filter.side_effect": NoResultFound}),
)
def test_api_project_patch_id_not_found(app):
    """Test api PATCH /api/project/wrong endpoint not found"""
    with app.test_client() as client:
        res = client.patch("/api/project/2", headers={"Authorization": f"Bearer {project_token}"},)
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 404
    assert "The requested URL was not found on the server" in json_data["message"]


def test_api_project_patch_id_not_int(app):
    """Test api PATCH /api/project/wrong endpoint not found"""
    with app.test_client() as client:
        res = client.patch(
            "/api/project/derp", headers={"Authorization": f"Bearer {project_token}"},
        )
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 404
    assert "The requested URL was not found on the server" in json_data["message"]


@patch(
    "src.apis.projects.Project",
    MagicMock(**{"query.filter.side_effect": OperationalError("err", "err", "err")}),
)
def test_api_project_patch_db_error(app):
    """Test api PATCH /api/project endpoint db error"""
    with app.test_client() as client:
        res = client.patch(
            "/api/project/1",
            json=project_payload_good,
            headers={"Authorization": f"Bearer {project_token}"},
        )
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 502
    assert "invalid response from an upstream server" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(**{"query.filter.side_effect": Exception}),
)
def test_api_project_patch_by_id_exception(app):
    """Test api PATCH /api/project/1 endpoint exception"""
    with app.test_client() as client:
        res = client.patch("/api/project/1", headers={"Authorization": f"Bearer {project_token}"},)
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 500
    assert "The server encountered an internal error" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(**{"query.filter.side_effect": NoResultFound}),
)
def test_api_project_delete_by_id_not_found(app):
    """Test api DELETE /api/project/1 endpoint exception"""
    with app.test_client() as client:
        res = client.delete("/api/project/2", headers={"Authorization": f"Bearer {project_token}"},)
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 404
    assert "The requested URL was not found on the server" in json_data["message"]


@patch(
    "src.apis.projects.Project", MagicMock(**{"query.filter.side_effect": Exception}),
)
def test_api_project_delete_by_id_exception(app):
    """Test api DELETE /api/project/1 endpoint exception"""
    with app.test_client() as client:
        res = client.delete("/api/project/1", headers={"Authorization": f"Bearer {project_token}"},)
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 500
    assert "The server encountered an internal error" in json_data["message"]


@patch(
    "src.apis.projects.Project",
    MagicMock(**{"query.filter.side_effect": OperationalError("err", "err", "err")}),
)
def test_api_project_delete_by_id_db_error(app):
    """Test api DELETE /api/project/1 endpoint db error"""
    with app.test_client() as client:
        res = client.delete("/api/project/1", headers={"Authorization": f"Bearer {project_token}"},)
    json_data = res.get_json()

    assert json_data["success"] is False
    assert json_data["error"] == 502
    assert "invalid response from an upstream server" in json_data["message"]
