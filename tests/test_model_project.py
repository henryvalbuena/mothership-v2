"""Tests for Latte persistance model"""
from sqlalchemy.orm.exc import NoResultFound

from src.database.project import Project

import pytest


def test_project_creation(db_testing):
    """Test creating a project"""
    with db_testing.app_context():
        project = Project(
            title="test",
            meta='["some", "thing"]',
            description="some testing",
            image="file.png",
            git_repo="github.com",
            demo_link="heroku.com",
        )
        project.insert()
    size = Project.query.all()
    project = Project.query.filter(Project.id == 1).one().to_json
    title = project["title"]
    description = project["description"]
    meta = project["meta"]
    image = project["image"]
    git_repo = project["git_repo"]
    demo_link = project["demo_link"]

    assert len(size) > 0
    assert title == "test"
    assert "some testing" in description
    assert ["some", "thing"] == meta
    assert "file.png" in image
    assert "github.com" in git_repo
    assert "heroku.com" in demo_link


def test_project_update(db_testing):
    """Test updating a project"""
    with db_testing.app_context():
        old_project = Project(
            title="test2",
            meta='["some", "thing"]',
            description="some testing",
            image="file.png",
            git_repo="github.com",
            demo_link="heroku.com",
        )
        old_project.insert()
    size = Project.query.all()
    project = Project.query.filter(Project.id == 1).one().to_json
    title = project["title"]
    description = project["description"]
    meta = project["meta"]
    image = project["image"]
    git_repo = project["git_repo"]
    demo_link = project["demo_link"]

    assert len(size) > 0
    assert title == "test"
    assert "some testing" in description
    assert ["some", "thing"] == meta
    assert "file.png" in image
    assert "github.com" in git_repo
    assert "heroku.com" in demo_link

    with db_testing.app_context():
        project_to_update = Project.query.filter(Project.id == 1).one()
        updated_project = project_to_update.to_json
        updated_project["title"] = "updated test"
        del updated_project["id"]
        project_to_update.update(**updated_project)
    size = Project.query.all()
    project = Project.query.filter(Project.id == 1).one().to_json
    title = project["title"]
    description = project["description"]
    meta = project["meta"]
    image = project["image"]
    git_repo = project["git_repo"]
    demo_link = project["demo_link"]

    assert len(size) > 0
    assert title == "updated test"
    assert "some testing" in description
    assert ["some", "thing"] == meta
    assert "file.png" in image
    assert "github.com" in git_repo
    assert "heroku.com" in demo_link


def test_project_delete(db_testing):
    """Test deleting a project"""
    with db_testing.app_context():
        project = Project(
            title="test delete",
            meta='["some", "thing"]',
            description="some testing",
            image="file.png",
            git_repo="github.com",
            demo_link="heroku.com",
        )
        project.insert()
        project_json = project.to_json

        assert project_json["title"] == "test delete"

        project_id = project_json["id"]

        project = Project.query.get(project_id).delete()

    with pytest.raises(NoResultFound) as err:
        Project.query.filter(Project.id == project_id).one()

    assert str(err.value) == "No row was found for one()"
