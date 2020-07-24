"""Testing module for latte api endpoints"""


def test_api_project_get(app):
    """Test api GET /api/project endpoint"""
    with app.test_client() as client:
        res = client.get("/api/project")
    json_data = res.get_json()

    assert json_data["success"] is True


def test_api_project_post(app):
    """Test api POST /api/project endpoint"""
    with app.test_client() as client:
        res = client.post("/api/project")
    json_data = res.get_json()

    assert json_data["success"] is True


def test_api_project_patch(app):
    """Test api PATCH /api/project/1 endpoint"""
    with app.test_client() as client:
        res = client.patch("/api/project/1")
    json_data = res.get_json()

    assert json_data["success"] is True
    assert json_data["project_id"] == 1


def test_api_project_delete(app):
    """Test api DELETE /api/project/1 endpoint"""
    with app.test_client() as client:
        res = client.delete("/api/project/1")
    json_data = res.get_json()

    assert json_data["success"] is True
    assert json_data["project_id"] == 1
