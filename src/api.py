from flask import Flask, jsonify
from flask_cors import CORS

from src.database.persistence import db, migrate
from src.apis.lattes import lattes_bp
from src.apis.projects import projects_bp
from src.auth.auth import AuthError


def create_app(config_name: str) -> Flask:
    """Create Flask app corresponding to the config name
    Args:
        config_name: configuration name
    Return:
        app: Flask instance
    """

    app = Flask(__name__)
    app.register_blueprint(lattes_bp)
    app.register_blueprint(projects_bp)
    config_module = f"src.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def running():
        """Check if the server is running or not"""
        return jsonify({"status": "running"})

    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(409)
    @app.errorhandler(422)
    @app.errorhandler(500)
    @app.errorhandler(502)
    @app.errorhandler(AuthError)
    def _handle_api_error(err):
        "Necessary when using blueprints"
        app.logger.error(str(err))
        return jsonify({"error": err.code, "message": err.description, "success": False}), err.code

    return app
