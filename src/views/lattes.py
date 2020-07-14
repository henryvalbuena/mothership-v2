from flask import Blueprint, jsonify, abort

from src.database.models import Latte
from src.auth.auth import AuthError, requires_auth

profile = Blueprint("profile", __name__)


@profile.route("/api/lattes")
def get_lattes():
    try:
        lattes = [_.long() for _ in Latte.query.all()]

        return jsonify({"lattes": lattes})
    except:
        # If there's a database error.
        abort(500)


"""
@TODO implement endpoint
    GET /lattes-detail
        it should require the 'get:lattes-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "lattes": lattes} where lattes is the list of lattes
        or appropriate status code indicating reason for failure
"""


@profile.route("/api/lattes-detail")
@requires_auth(permission="get:lattes-detail")
def get_lattes_detail(jwt):
    try:
        lattes = [_.long() for _ in Latte.query.all()]

        return jsonify({"success": True, "lattes": lattes})
    except:
        # If there's a database error.
        abort(500)


"""
@TODO implement endpoint
    POST /lattes
        it should create a new row in the lattes table
        it should require the 'post:lattes' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "lattes": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
"""


@profile.route("/api/lattes", methods=["POST"])
@requires_auth(permission="post:lattes")
def create_lattes(jwt):
    try:
        drink = Drink(
            title=request.json["title"],
            ingredients=json.dumps(request.json["ingredients"]),
        )
        drink.insert()

        return jsonify({"success": True, "lattes": [drink.long()]})
    except:
        # If the payload is malformed.
        abort(400)


"""
@TODO implement endpoint
    PATCH /lattes/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:lattes' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "lattes": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
"""


@profile.route("/api/lattes/<int:drink_id>", methods=["PATCH"])
@requires_auth(permission="patch:lattes")
def update_drink(jwt, drink_id):
    try:
        drink = Latte.query.filter(Latte.id == drink_id).first()
        if "title" in request.json:
            drink.title = request.json["title"]
        if "ingredients" in request.json:
            drink.ingredients = json.dumps(request.json["ingredients"])
        drink.update()

        return jsonify({"success": True, "lattes": [drink.long()]})
    except:
        # If the payload is malformed.
        abort(400)


"""
@TODO implement endpoint
    DELETE /lattes/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:lattes' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
"""


@profile.route("/api/lattes/<int:drink_id>", methods=["DELETE"])
@requires_auth(permission="delete:lattes")
def remove_drink(jwt, drink_id):
    try:
        drink = Latte.query.filter(Latte.id == drink_id).first()
        drink.delete()

        return jsonify({"success": True, "delete": drink_id})
    except:
        # If the id does not match any drink in the database.
        abort(400)


## Error Handling
"""
Example error handling for unprocessable entity
"""


@profile.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


"""
@TODO implement error handlers using the @profile.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

"""


@profile.errorhandler(401)
def unprocessable(error):
    return jsonify({"success": False, "error": 401, "message": "Unauthorized"}), 401


"""
@TODO implement error handler for 404
    error handler should conform to general task above 
"""


@profile.errorhandler(404)
def unprocessable(error):
    return jsonify({"success": False, "error": 404, "message": "Not found"}), 404


"""
@TODO implement error handler for AuthError
    error handler should conform to general task above 
"""


@profile.errorhandler(AuthError)
def unprocessable(error):
    return (
        jsonify(
            {"success": False, "error": error.status_code, "message": error.error,}
        ),
        error.status_code,
    )


@profile.errorhandler(500)
def unprocessable(error):
    return jsonify({"success": False, "error": 500, "message": "Server error"}), 500


@profile.errorhandler(400)
def unprocessable(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400
