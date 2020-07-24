import json

from flask import Blueprint, jsonify, abort, request, current_app as context

projects_bp = Blueprint("projects_bp", __name__)


@projects_bp.route("/api/project")
def get_projects():
    """Return projects from database"""
    try:
        return jsonify({"success": True})
    except Exception as err:
        context.logger.error(err)
        abort(500)


@projects_bp.route("/api/project", methods=["POST"])
def create_project():
    """Create a project on database"""
    try:
        return jsonify({"success": True})
    except Exception as err:
        context.logger.error(err)
        abort(500)


@projects_bp.route("/api/project/<int:project_id>", methods=["PATCH"])
def update_project(project_id):
    """Update a project on database"""
    try:
        return jsonify({"success": True, "project_id": project_id})
    except Exception as err:
        context.logger.error(err)
        abort(500)


@projects_bp.route("/api/project/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    """Delete a project from database"""
    try:
        return jsonify({"success": True, "project_id": project_id})
    except Exception as err:
        context.logger.error(err)
        abort(500)
