import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = "coffe-shop-project.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "drinks" # Should be lattes


class AuthError(Exception):
    """AuthError Exception
    A standardized way to communicate auth failure modes
    """

    def __init__(self, description, code):
        self.description = description
        self.code = code


def get_token_auth_header():
    """Retrieve jwt from the request header"""
    if "Authorization" not in request.headers:
        raise AuthError(
            "Missing mandatory headers.", 401,
        )

    auth_header = request.headers["Authorization"]
    header_parts = auth_header.split(" ")

    if len(header_parts) != 2:
        raise AuthError(
            "Missing authorization elements.", 401,
        )
    elif header_parts[0].lower() != "bearer":
        raise AuthError(
            "Unable to find appropiate keywords.", 401,
        )

    return header_parts[1]


def check_permissions(permission, payload):
    """Validate claims"""
    if "permissions" not in payload:
        raise AuthError("Missing mandatory key.", 401)

    if permission not in payload["permissions"]:
        raise AuthError(
            "User don't have access to resource.", 401,
        )
    return True


def verify_decode_jwt(token):
    """Checks if the jwt has been tampered with"""
    # Get auth0 public key
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    # Get data from header
    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception:
        raise AuthError(
            "Malformed header value.", 401,
        )

    # Choose our key
    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError("Authorization malformed.", 401)

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    # Verify
    if rsa_key:
        try:
            # Validate jwt
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError("Token expired.", 401)

        except jwt.JWTClaimsError:
            raise AuthError(
                "Incorrect claims. Please, check the audience and issuer.", 401,
            )
        except Exception:
            raise AuthError(
                "Unable to parse authentication token.", 400,
            )
    raise AuthError(
        "Unable to find the appropriate key.", 400,
    )


def requires_auth(permission=""):
    """Auth decorator for routes"""

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                jwt = get_token_auth_header()
                payload = verify_decode_jwt(jwt)
            except AuthError as err:
                raise AuthError(
                    err.description, err.code,
                )

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
