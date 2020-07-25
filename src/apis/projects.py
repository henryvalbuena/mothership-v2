"""This is where Projects api definition of routes lives"""
import json

from flask import Blueprint, jsonify, abort, request, current_app as context
from sqlalchemy.exc import OperationalError

from src.database.project import Project

projects_bp = Blueprint("projects_bp", __name__)


@projects_bp.route("/api/project")
def get_projects():
    """Return projects from database"""
    try:
        projects = Project.query.all()
        projects = [_.to_json for _ in projects]
        return jsonify(projects)
    except OperationalError as err:
        context.logger.error(err)
        abort(502)
    except Exception as err:
        context.logger.error(err)
        abort(500)


@projects_bp.route("/api/project/<int:project_id>")
def get_project(project_id):
    """Return a project from database"""
    try:
        project = Project.query.filter(Project.id == project_id).one()
        return jsonify(project.to_json)
    except Exception as err:
        context.logger.error(err)
        abort(500)


@projects_bp.route("/api/project", methods=["POST"])
def create_project():
    """Create a project on database"""
    try:
        payload = {
            "title": request.json["title"],
            "meta": json.dumps(request.json["meta"]),
            "description": request.json["description"],
            "image": request.json["image"],
            "git_repo": request.json["git_repo"],
            "demo_link": request.json["demo_link"],
        }
        project = Project(**payload)
        project.insert()
        return jsonify(project.to_json)
    except Exception as err:
        context.logger.error(err)
        abort(500)


@projects_bp.route("/api/project/<int:project_id>", methods=["PATCH"])
def update_project(project_id):
    """Update a project on database"""
    try:
        project = Project.query.filter(Project.id == project_id).one()
        updated_project = {
            "title": request.json["title"],
            "meta": json.dumps(request.json["meta"]),
            "description": request.json["description"],
            "image": request.json["image"],
            "git_repo": request.json["git_repo"],
            "demo_link": request.json["demo_link"],
        }
        project.update(**updated_project)
        return jsonify(project.to_json)
    except Exception as err:
        context.logger.error(err)
        abort(500)


@projects_bp.route("/api/project/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    """Delete a project from database"""
    try:
        project = Project.query.filter(Project.id == project_id).one()
        project.delete()
        return jsonify({"success": True, "project_id": project_id})
    except Exception as err:
        context.logger.error(err)
        abort(500)
