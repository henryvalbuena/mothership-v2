import json

from flask import Blueprint, jsonify, abort, request, current_app as context
from sqlalchemy.exc import DataError, IntegrityError, OperationalError
from sqlalchemy.orm.exc import NoResultFound

from src.database.models import Latte
from src.auth.auth import requires_auth
from src.helpers.tools import validate_none_word_input
from src.helpers.errors import InvalidUserInput


profile = Blueprint("profile", __name__)


@profile.route("/api/latte")
def get_lattes():
    """Return lattes from database"""
    try:
        lattes = [_.long() for _ in Latte.query.all()]
        return jsonify({"lattes": lattes})
    except OperationalError as err:
        context.logger.error(err)
        abort(502)
    except Exception as err:
        context.logger.error(err)
        abort(500)


@profile.route("/api/latte/<int:latte_id>")
def get_latte(latte_id):
    """Return a latte from database"""
    try:
        latte = Latte.query.filter(Latte.id == latte_id).one()
        return jsonify({"lattes": latte.long()})
    except NoResultFound as err:
        context.logger.error(err)
        abort(404)
    except OperationalError as err:
        context.logger.error(err)
        abort(502)
    except Exception as err:
        context.logger.error(err)
        abort(500)


@profile.route("/api/latte", methods=["POST"])
@requires_auth(permission="post:latte")
def create_lattes(jwt):
    """Create new latte"""
    try:
        ingredients = json.dumps(request.json["ingredients"])
        rawTitle = request.json["title"]
        validTitle = validate_none_word_input(rawTitle)
        latte = Latte(title=validTitle, ingredients=ingredients,)
        latte.insert()

        return jsonify({"success": True, "lattes": [latte.long()]}), 201
    except (KeyError, InvalidUserInput, DataError) as err:
        context.logger.error(err)
        abort(400)
    except IntegrityError as err:
        context.logger.error(err)
        abort(409)
    except OperationalError as err:
        context.logger.error(err)
        abort(502)
    except Exception as err:
        context.logger.error(err)
        abort(500)


@profile.route("/api/latte/<int:latte_id>", methods=["PATCH"])
@requires_auth(permission="patch:latte")
def update_drink(jwt, latte_id):
    """Update latte information"""
    try:
        if "title" not in request.json and "ingredients" not in request.json:
            raise KeyError

        latte = Latte.query.filter(Latte.id == latte_id).one()
        if "title" in request.json:
            validTitle = validate_none_word_input(request.json["title"])
            latte.title = validTitle
        if "ingredients" in request.json:
            validIng = json.dumps(request.json["ingredients"])
            latte.ingredients = validIng
        latte.update()

        return jsonify({"success": True, "lattes": [latte.long()]})
    except (KeyError, InvalidUserInput, DataError) as err:
        context.logger.error(err)
        abort(400)
    except NoResultFound as err:
        context.logger.error(err)
        abort(404)
    except OperationalError as err:
        context.logger.error(err)
        abort(502)
    except Exception as err:
        context.logger.error(err)
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
        context.logger.error(err)
        abort(404)
    except OperationalError as err:
        context.logger.error(err)
        abort(502)
    except Exception as err:
        context.logger.error(err)
        abort(500)
