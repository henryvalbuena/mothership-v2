from flask import Flask, jsonify
from flask_cors import CORS

from src.database.models import db, migrate
from src.views.lattes import profile
from src.auth.auth import AuthError


def create_app(config_name: str) -> Flask:
    """Create Flask app corresponding to the config name
    Args:
        config_name: configuration name
    Return:
        app: Flask instance
    """

    app = Flask(__name__)
    app.register_blueprint(profile)
    config_module = f"src.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def running():
        """Check if the server is running or not"""
        return jsonify({"status": "running"})

    @app.errorhandler(404)
    @app.errorhandler(405)
    def _handle_api_error(err):
        "Necessary when using blueprints"
        app.logger.error(str(err))
        return jsonify({"error": err.code, "message": err.description, "success": False}), err.code

    return app


@profile.errorhandler(400)
@profile.errorhandler(401)
@profile.errorhandler(409)
@profile.errorhandler(422)
@profile.errorhandler(500)
@profile.errorhandler(502)
def _json_error_handler(error):
    "API error handler"
    return (
        jsonify({"success": False, "error": error.code, "message": error.description}),
        error.code,
    )


@profile.errorhandler(AuthError)
def _auth_error_handler(error):
    """Authentication error custom handler AuthError"""
    return (
        jsonify({"success": False, "error": error.code, "message": error.description}),
        error.code,
    )
