import json
from flask import Blueprint, jsonify, abort, request, current_app as context
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import NoResultFound

from src.database.models import Latte
from src.auth.auth import requires_auth


profile = Blueprint("profile", __name__)


@profile.route("/api/latte")
def get_lattes():
    """Return lattes from database"""
    try:
        lattes = [_.long() for _ in Latte.query.all()]
        return jsonify({"lattes": lattes})
    except OperationalError as err:
        context.logger.warning(err)
        abort(502)
    except Exception as err:
        context.logger.warning(err)
        abort(500)


@profile.route("/api/latte/<int:latte_id>")
def get_latte(latte_id):
    """Return a latte from database"""
    try:
        latte = Latte.query.filter(Latte.id == latte_id).one()
        return jsonify({"lattes": latte.long()})
    except NoResultFound as err:
        context.logger.warning(err)
        abort(404)
    except OperationalError as err:
        context.logger.warning(err)
        abort(502)
    except Exception as err:
        context.logger.warning(err)
        abort(500)


@profile.route("/api/latte", methods=["POST"])
@requires_auth(permission="post:latte")
def create_lattes(jwt):
    """Create new latte"""
    try:
        latte = Latte(
            title=request.json["title"],
            ingredients=json.dumps(request.json["ingredients"]),
        )
        latte.insert()

        return jsonify({"success": True, "lattes": [latte.long()]})
    except KeyError as err:
        context.logger.warning(err)
        abort(400)
    except IntegrityError as err:
        context.logger.warning(err)
        abort(409)
    except OperationalError as err:
        context.logger.warning(err)
        abort(502)
    except Exception as err:
        context.logger.warning(err)
        abort(500)


@profile.route("/api/latte/<int:latte_id>", methods=["PATCH"])
@requires_auth(permission="patch:latte")
def update_drink(jwt, latte_id):
    """Update latte information"""
    try:
        latte = Latte.query.filter(Latte.id == latte_id).one()
        if "title" in request.json:
            latte.title = request.json["title"]
        if "ingredients" in request.json:
            latte.ingredients = json.dumps(request.json["ingredients"])
        latte.update()

        return jsonify({"success": True, "lattes": [latte.long()]})
    except KeyError as err:
        context.logger.warning(err)
        abort(400)
    except NoResultFound as err:
        context.logger.warning(err)
        abort(404)
    except OperationalError as err:
        context.logger.warning(err)
        abort(502)
    except Exception as err:
        context.logger.warning(err)
        abort(500)


@profile.route("/api/latte/<int:latte_id>", methods=["DELETE"])
@requires_auth(permission="delete:latte")
def remove_drink(jwt, latte_id):
    """Remove latte based on its id"""
    try:
        latte = Latte.query.filter(Latte.id == latte_id).one()
        latte.delete()

        return jsonify({"success": True, "delete": latte_id})
    except NoResultFound as err:
        context.logger.warning(err)
        abort(404)
    except OperationalError as err:
        context.logger.warning(err)
        abort(502)
    except Exception as err:
        context.logger.warning(err)
        abort(500)
