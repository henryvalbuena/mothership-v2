import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db, setup_db, Drink
from auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

"""
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
"""
# db_drop_and_create_all()
try:
    Drink.query.all()
except Exception:
    db.create_all()

## ROUTES
"""
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@app.route("/api/drinks")
def get_drinks():
    try:
        drinks = [_.long() for _ in Drink.query.all()]

        return jsonify({"drinks": drinks})
    except:
        # If there's a database error.
        abort(500)


"""
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@app.route("/api/drinks-detail")
@requires_auth(permission="get:drinks-detail")
def get_drinks_detail(jwt):
    try:
        drinks = [_.long() for _ in Drink.query.all()]

        return jsonify({"success": True, "drinks": drinks})
    except:
        # If there's a database error.
        abort(500)


"""
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
"""


@app.route("/api/drinks", methods=["POST"])
@requires_auth(permission="post:drinks")
def create_drinks(jwt):
    try:
        drink = Drink(
            title=request.json["title"], ingredients=json.dumps(request.json["ingredients"])
        )
        drink.insert()

        return jsonify({"success": True, "drinks": [drink.long()]})
    except:
        # If the payload is malformed.
        abort(400)


"""
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
"""


@app.route("/api/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth(permission="patch:drinks")
def update_drink(jwt, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).first()
        if "title" in request.json:
            drink.title = request.json["title"]
        if "ingredients" in request.json:
            drink.ingredients = json.dumps(request.json["ingredients"])
        drink.update()

        return jsonify({"success": True, "drinks": [drink.long()]})
    except:
        # If the payload is malformed.
        abort(400)


"""
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
"""


@app.route("/api/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth(permission="delete:drinks")
def remove_drink(jwt, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).first()
        drink.delete()

        return jsonify({"success": True, "delete": drink_id})
    except:
        # If the id does not match any drink in the database.
        abort(400)


## Error Handling
"""
Example error handling for unprocessable entity
"""


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


"""
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

"""


@app.errorhandler(401)
def unprocessable(error):
    return jsonify({"success": False, "error": 401, "message": "Unauthorized"}), 401


"""
@TODO implement error handler for 404
    error handler should conform to general task above 
"""


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({"success": False, "error": 404, "message": "Not found"}), 404


"""
@TODO implement error handler for AuthError
    error handler should conform to general task above 
"""


@app.errorhandler(AuthError)
def unprocessable(error):
    return (
        jsonify(
            {"success": False, "error": error.status_code, "message": error.error,}
        ),
        error.status_code,
    )


@app.errorhandler(500)
def unprocessable(error):
    return jsonify({"success": False, "error": 500, "message": "Server error"}), 500


@app.errorhandler(400)
def unprocessable(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400
