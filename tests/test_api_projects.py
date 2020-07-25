"""Testing module for latte api endpoints"""
import json
from unittest.mock import MagicMock, patch

from sqlalchemy.exc import OperationalError

from tests.conftest import DummyProject, dummy_project_instance, project_payload_good


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


@patch("src.apis.projects.Project", DummyProject)
def test_api_project_post(app):
    """Test api POST /api/project endpoint"""
    with app.test_client() as client:
        res = client.post("/api/project", json=project_payload_good)
    json_data = res.get_json()

    assert json_data["title"] == "test"
    assert json_data["meta"] == '["meta", "testing"]'
    assert json.loads(json_data["meta"]) == ["meta", "testing"]
    assert json_data["description"] == "some testing"
    assert json_data["image"] == "image.png"
    assert json_data["git_repo"] == "github.com"
    assert json_data["demo_link"] == "heroku.com"


@patch("src.apis.projects.Project", dummy_project_instance)
def test_api_project_patch(app):
    """Test api PATCH /api/project/1 endpoint"""
    with app.test_client() as client:
        res = client.patch("/api/project/1", json=project_payload_good)
    json_data = res.get_json()

    assert json_data["title"] == "test"
    assert json_data["meta"] == '["meta", "testing"]'
    assert json.loads(json_data["meta"]) == ["meta", "testing"]
    assert json_data["description"] == "some testing"
    assert json_data["image"] == "image.png"
    assert json_data["git_repo"] == "github.com"
    assert json_data["demo_link"] == "heroku.com"


@patch("src.apis.projects.Project", dummy_project_instance)
def test_api_project_delete(app):
    """Test api DELETE /api/project/1 endpoint"""
    with app.test_client() as client:
        res = client.delete("/api/project/1")
    json_data = res.get_json()

    assert json_data["success"] is True
    assert json_data["project_id"] == 1


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
    assert (
        json_data["message"]
        == "The proxy server received an invalid response from an upstream server."
    )
